import os
from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, Optional, Literal
from dotenv import load_dotenv

from langchain_core.runnables import RunnableConfig

load_dotenv()

class SearchAPI(Enum):
    PERPLEXITY = "perplexity"
    TAVILY = "tavily"
    DUCKDUCKGO = "duckduckgo"
    SEARXNG = "searxng"

class Configuration(BaseModel):
    """The configurable fields for the research assistant."""

    max_web_research_loops: int = Field(
        default=2,
        title="Research Depth",
        description="Number of research iterations to perform"
    )
    # local_llm: str = Field(
    #     default="llama3.2",
    #     title="LLM Model Name",
    #     description="Name of the LLM model to use"
    # )
    llm: Literal["llama3.2", "gemini-2.5-flash-preview-05-20"] = Field(
        default="gemini-2.5-flash-preview-05-20",
        title="LLM Model Name",
        description="Name of the LLM model to use"
    )

    llm_provider: Literal["ollama", "lmstudio", "google-genai"] = Field(
        default="google-genai",
        title="LLM Provider",
        description="Provider for the LLM (Ollama, LMStudio or google-genai)"
    )
    search_api: Literal["perplexity", "tavily", "duckduckgo", "searxng"] = Field(
        default="tavily",
        title="Search API",
        description="Web search API to use"
    )
    fetch_full_page: bool = Field(
        default=True,
        title="Fetch Full Page",
        description="Include the full page content in the search results"
    )
    ollama_base_url: str = Field(
        default="http://localhost:11434/",
        title="Ollama Base URL",
        description="Base URL for Ollama API"
    )
    lmstudio_base_url: str = Field(
        default="http://localhost:1234/v1",
        title="LMStudio Base URL",
        description="Base URL for LMStudio OpenAI-compatible API"
    )
    google_genai_api_key: str = Field(
        default=os.getenv("GEMINI_API_KEY"),
        title="Google GenAI API Key",
        description="API key for Google GenAI"

    )
    strip_thinking_tokens: bool = Field(
        default=True,
        title="Strip Thinking Tokens",
        description="Whether to strip <think> tokens from model responses"
    )
    tavily_api_key: str = Field(
        default=os.getenv("TAVILY_API_KEY"),
        title="Tavily API Key",
        description="API key for Tavily search"
    )

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        
        # Get raw values from environment or config
        raw_values: dict[str, Any] = {
            name: os.environ.get(name.upper(), configurable.get(name))
            for name in cls.model_fields.keys()
        }
        
        # Filter out None values
        values = {k: v for k, v in raw_values.items() if v is not None}
        
        return cls(**values)