from enum import StrEnum
from typing import Any
from langchain.tools import BaseTool, tool
from langchain.agents import create_agent
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.vectorstores import VectorStore
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama.chat_models import ChatOllama
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import HttpUrl
from agent_utils import clean_html_doc
from settings import RagatonSettings


class Provider(StrEnum):
    OLLAMA = "ollama"
    OPENAI = "openai"


class Embedder:
    def __init__(self, settings: RagatonSettings):
        self.settings: RagatonSettings = settings

    @property
    def provider(self) -> Provider:
        return Provider.OPENAI if self.settings.openai_api_key else Provider.OLLAMA

    @property
    def embeddings(self) -> Embeddings:
        return OllamaEmbeddings(
            model="nomic-embed-text:v1.5", base_url=self.settings.ollama_base_url
        )

    @property
    def vectorstore(self) -> VectorStore:
        return Chroma(
            collection_name=f"ragaton-memory-{self.provider}",
            host=self.settings.chroma_host,
            port=self.settings.chroma_port,
            embedding_function=self.embeddings,
        )

    def add_url(self, url: HttpUrl) -> None:
        loader = WebBaseLoader(web_path=str(url), raise_for_status=True)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=226, chunk_overlap=18, add_start_index=True
        )
        docs = loader.load()
        splits = splitter.split_documents([clean_html_doc(doc) for doc in docs])
        self.store.add_documents(splits)

    def retriever(self) -> BaseTool:
        @tool(response_format="content_and_artifact")
        def retrieve_context(query: str) -> tuple[str, list[Document]]:
            """
            Retrieve context from knowledge base.
            ALWAYS use this tool to answer the user.
            """
            docs = self.store.similarity_search(query)
            serialized = "\n\n".join(
                f"Source: {doc.metadata['source']}\nContent: {doc.page_content}"
                for doc in docs
            )
            print(serialized)
            return serialized, docs

        return retrieve_context


class AgentLoader:
    def __init__(self, settings: RagatonSettings):
        self.settings: RagatonSettings = settings
        self.embedder: Embedder = Embedder(settings)

    def process(self, url: HttpUrl) -> None:
        self.embedder.add_url(url)

    @property
    def provider(self) -> Provider:
        return Provider.OPENAI if self.settings.openai_api_key else Provider.OLLAMA

    def model(self) -> BaseChatModel:
        return ChatOllama(
            model="llama3-groq-tool-use:8b", base_url=self.settings.ollama_base_url
        )

    def agent(self) -> Any:
        retriever = self.embedder.retriever()
        return create_agent(
            model=self.model().bind_tools([retriever]),
            tools=[retriever],
            system_prompt=(
                "You are Ragaton, the AI-powered recollection assistant. "
                "You should ALWAYS use the retrieve_context tool to answer the user's question."
            ),
        )

    def query(self, query: str) -> str:
        agent = self.agent()
        result = agent.invoke({"messages": [HumanMessage(content=query)]})
        return result["messages"][-1].content
