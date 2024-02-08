import os
from pathlib import Path

PROJECT_ROOT_PATH: Path = Path(__file__).parents[1]

DOCS_PATH: Path = PROJECT_ROOT_PATH / "data"

CHROMA_COLLECTION_NAME = "cdcdocs"

TRUEFOUNDRY_API_KEY = os.getenv("TRUEFOUNDRY_API_KEY")

TRUEFOUNDRY_BASE_URL = "https://llm-gateway.truefoundry.com"

TRUEFOUNDRY_MODEL = "truefoundry-public/Mistral-Instruct(7B)"

CHROMA_HOST = os.getenv("CHROMA_HOST") or "localhost"

CHROMA_PORT = os.getenv("CHROMA_PORT") or "8001"
