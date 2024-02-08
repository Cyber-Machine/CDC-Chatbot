import json
from typing import Any, Dict, List, Sequence, Tuple

import httpx
from httpx import Timeout
from llama_index.bridge.pydantic import Field
from llama_index.constants import DEFAULT_CONTEXT_WINDOW, DEFAULT_NUM_OUTPUTS
from llama_index.core.llms.types import (
    ChatMessage,
    ChatResponse,
    ChatResponseGen,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
    MessageRole,
)
from llama_index.llms.base import llm_chat_callback, llm_completion_callback
from llama_index.llms.custom import CustomLLM

DEFAULT_REQUEST_TIMEOUT = 30.0
DEFAULT_LLM_MODEL = "truefoundry-public/Mistral-Instruct(7B)"


def get_addtional_kwargs(
    response: Dict[str, Any], exclude: Tuple[str, ...]
) -> Dict[str, Any]:
    return {k: v for k, v in response.items() if k not in exclude}


class TrueFoundry(CustomLLM):
    base_url: str = Field(
        description="Base url the model is hosted under.",
    )
    model: str = Field(
        default=DEFAULT_LLM_MODEL,
        description="The hosted model to use.",
    )
    temperature: float = Field(
        default=0.7,
        description="The temperature to use for sampling.",
        gte=0.0,
        lte=1.0,
    )
    context_window: int = Field(
        default=DEFAULT_CONTEXT_WINDOW,
        description="The maximum number of context tokens for the model.",
        gt=0,
    )

    api_key: str = Field(
        default=None,
        description=("Additional headers to send to the server."),
    )

    stop: List[str] = Field(
        default=["</s>"],
        description="Stopping token for the model",
    )

    request_timeout: float = Field(
        default=DEFAULT_REQUEST_TIMEOUT,
        description="The timeout for making http request to Ollama API server",
    )
    prompt_key: str = Field(
        default="prompt", description="The key to use for the prompt in API calls."
    )

    top_p: float = Field(default=0.7, description="Top p for the model")

    top_k: int = Field(default=50, description="Top_k for the model")

    max_tokens: int = Field(default=125, description="Max tokens for the model")

    repetation_penalty: float = Field(
        default=1.0, description="penalty used for the model"
    )

    is_chat_model: bool = Field(
        default=True, description="If model is chat model or not"
    )

    additional_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional model parameters for the Truefoundry API.",
    )

    @classmethod
    def class_name(cls) -> str:
        return "Truefoundry_llm"

    @property
    def metadata(self) -> LLMMetadata:
        """LLM metadata."""
        return LLMMetadata(
            context_window=self.context_window,
            num_output=DEFAULT_NUM_OUTPUTS,
            model_name=self.model,
            is_chat_model=self.is_chat_model,
        )

    @property
    def _model_kwargs(self) -> Dict[str, Any]:
        base_kwargs = {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "repetition_penalty": self.repetation_penalty,
            "stop": self.stop,
        }
        return {
            **base_kwargs,
            **self.additional_kwargs,
        }

    @llm_chat_callback()
    def chat(self, messages: Sequence[ChatMessage], **kwargs: Any) -> ChatResponse:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": message.role.value,
                    "content": message.content,
                    **message.additional_kwargs,
                }
                for message in messages
            ],
            "options": self._model_kwargs,
            **kwargs,
        }

        with httpx.Client(timeout=Timeout(self.request_timeout)) as client:
            response = client.post(
                url=f"{self.base_url}/openai/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
            response.raise_for_status()
            raw = response.json()
            message = raw["choices"][0]["message"]
            return ChatResponse(
                message=ChatMessage(
                    content=message.get("content"),
                    role=MessageRole(message.get("role")),
                    additional_kwargs=get_addtional_kwargs(
                        message, ("content", "role")
                    ),
                ),
                raw=raw,
                additional_kwargs=get_addtional_kwargs(raw, ("message",)),
            )

    @llm_chat_callback()
    def stream_chat(
        self, messages: Sequence[ChatMessage], **kwargs: Any
    ) -> ChatResponseGen:
        raise NotImplementedError

    @llm_completion_callback()
    def complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponse:
        payload = {
            self.prompt_key: prompt,
            "model": self.model,
            "options": self._model_kwargs,
            **kwargs,
        }

        with httpx.Client(timeout=Timeout(self.request_timeout)) as client:
            response = client.post(
                url=f"{self.base_url}/openai/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            raw = data["choices"][0]
            text = raw.get("response")
            return CompletionResponse(
                text=text,
                raw=raw,
                additional_kwargs=get_addtional_kwargs(raw, ("response",)),
            )

    @llm_completion_callback()
    def stream_complete(
        self, prompt: str, formatted: bool = False, **kwargs: Any
    ) -> CompletionResponseGen:
        raise NotImplementedError
