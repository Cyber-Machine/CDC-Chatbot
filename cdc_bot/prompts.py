from llama_index.llms import ChatMessage, MessageRole
from llama_index.prompts import ChatPromptTemplate

# Text QA Prompt
chat_text_qa_msgs = [
    ChatMessage(
        role=MessageRole.SYSTEM,
        content=(
            "You are an expert Q&A system that is trusted around the world.\n"
            "Always answer the query using the provided context information, "
            "and not prior knowledge.\n"
            "Some rules to follow:\n"
            "1. Never directly reference the given context in your answer.\n"
            "2. Avoid statements like 'Based on the context, ...' or "
            "'The context information ...' or anything along "
            "those lines."
            "3. Always give concise solutions, be brief."
        ),
    ),
    ChatMessage(
        role=MessageRole.USER,
        content=(
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and not prior knowledge, "
            "answer the query.\n"
            "Query: {query_str}\n"
            "Answer: "
        ),
    ),
]
text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)

# Refine Prompt
chat_refine_msgs = [
    ChatMessage(
        role=MessageRole.SYSTEM,
        content=(
            "You are an expert Q&A system that strictly operates in two modes "
            "when refining existing answers:\n"
            "1. **Rewrite** an original answer using the new context.\n"
            "2. **Repeat** the original answer if the new context isn't useful.\n"
            "Never reference the original answer or context directly in your answer.\n"
            "When in doubt, just repeat the original answer."
        ),
    ),
    ChatMessage(
        role=MessageRole.USER,
        content=(
            "New Context: {context_msg}\n"
            "Query: {query_str}\n"
            "Original Answer: {existing_answer}\n"
            "New Answer: "
        ),
    ),
]
refine_template = ChatPromptTemplate(chat_refine_msgs)
