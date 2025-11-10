from enum import StrEnum
import itertools
from typing import Any
from langchain.tools import BaseTool, tool
from langchain.agents import create_agent
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.vectorstores import VectorStore
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama.chat_models import ChatOllama
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import HttpUrl
from requests import HTTPError
from agent_utils import clean_html_doc
from database import NewsArticle
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
        self.vectorstore.add_documents(splits)

    def retriever(self) -> BaseTool:
        @tool(response_format="content_and_artifact")
        def retrieve_context(query: str) -> tuple[str, list[Document]]:
            """
            Retrieve context from knowledge base.
            ALWAYS use this tool to answer the useruser's questioi.
            """
            docs = self.vectorstore.similarity_search(query)
            serialized = "\n\n".join(f"Context: {doc.page_content}" for doc in docs)
            return serialized, docs

        return retrieve_context


class AgentLoader:
    def __init__(self, settings: RagatonSettings):
        self.settings: RagatonSettings = settings
        self.embedder: Embedder = Embedder(settings)

    def process(self, url: HttpUrl) -> None:
        article = NewsArticle.select().where(NewsArticle.url == url).first()

        if article and article.status != 200:
            raise HTTPError(f"HTTP Error {article.status} for URL {url}")

        if not article:
            try:
                self.embedder.add_url(url)
            except HTTPError as e:
                article = NewsArticle(url=url, status=e.response.status_code)
            else:
                article = NewsArticle(url=url)

            article.save()

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

    def query(self, query: str) -> tuple[str, set[str]]:
        agent = self.agent()
        result = agent.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=f"""
                        Use the retrieve_context tool to answer this:
                        <query>{query}</query>
                        """.strip()
                    )
                ]
            }
        )
        responses = [m for m in result["messages"] if isinstance(m, AIMessage)]
        response_text = str(responses[-1].content) if responses else ""
        context = [m.artifact for m in result["messages"] if isinstance(m, ToolMessage)]
        sources = {
            str(source)
            for doc in itertools.chain.from_iterable(context)
            if (source := doc.metadata.get("source"))
        }

        return response_text, sources
