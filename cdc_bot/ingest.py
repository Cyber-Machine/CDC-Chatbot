import chromadb
from chromadb.api.client import ClientAPI
from llama_index import ServiceContext, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.storage.storage_context import StorageContext
from llama_index.vector_stores import ChromaVectorStore

from cdc_bot.constants import (
    CHROMA_COLLECTION_NAME,
    DOCS_PATH,
    TRUEFOUNDRY_API_KEY,
    TRUEFOUNDRY_BASE_URL,
    TRUEFOUNDRY_MODEL,
)
from cdc_bot.llm import TrueFoundry


def get_index():
    client = chromadb.HttpClient()
    llm = TrueFoundry(
        base_url=TRUEFOUNDRY_BASE_URL,
        model=TRUEFOUNDRY_MODEL,
        api_key=TRUEFOUNDRY_API_KEY,
    )
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

    try:
        collection = client.get_collection(name=CHROMA_COLLECTION_NAME)
    except ValueError:
        print("Ingesting document")
        return ingest(
            chroma_client=client,
            service_context=service_context,
        )

    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
        service_context=service_context,
    )
    print("Using ingested documents")
    return index


def ingest(chroma_client: ClientAPI, service_context):
    collection = chroma_client.create_collection(CHROMA_COLLECTION_NAME)

    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    documents = SimpleDirectoryReader(DOCS_PATH).load_data()
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, service_context=service_context
    )
    return index
