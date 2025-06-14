# 🌐 Flexible Deep Researcher

Flexible Deep Researcher is a web research assistant that uses any local LLM hosted by [Ollama](https://ollama.com/search) or [LMStudio](https://lmstudio.ai/) — and now also supports the [Gemini API](https://aistudio.google.com/) for remote inference. Give it a topic and it will generate a web search query, gather web search results, summarize the results of web search, reflect on the summary to examine knowledge gaps, generate a new search query to address the gaps, and repeat for a user-defined number of cycles. It will provide the user a final markdown summary with all sources used to generate the summary.

![ollama-deep-research](https://github.com/user-attachments/assets/1c6b28f8-6b64-42ba-a491-1ab2875d50ea)

Short summary video:
<video src="https://github.com/user-attachments/assets/02084902-f067-4658-9683-ff312cab7944" controls></video>

## 📺 Video Tutorials

See it in action or build it yourself? Check out these helpful video tutorials:
- [Overview of Local Deep Researcher with R1](https://www.youtube.com/watch?v=sGUjmyfof4Q) - Load and test [DeepSeek R1](https://api-docs.deepseek.com/news/news250120) [distilled models](https://ollama.com/library/deepseek-r1).
- [Building Local Deep Researcher from Scratch](https://www.youtube.com/watch?v=XGuTzHoqlj8) - Overview of how this is built.

## 🚀 Quickstart

Clone the repository:
```shell
git clone https://github.com/langchain-ai/local-deep-researcher.git
cd local-deep-researcher
```
Install uv package manager
Sync dependencies with uv:
```shell
uv sync
```
Then edit the `.env` file to customize the environment variables according to your needs. These environment variables control the model selection, search tools, and other configuration settings. When you run the application, these values will be automatically loaded via `python-dotenv` (because `langgraph.json` point to the "env" file).
```shell
cp .env.example .env
```

### Selecting model using Gemini API (NEW!)

1. Get an API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Update the `.env` `GEMINI_API_KEY`
3. Update the configuration.py file to set `model_name` (default is `gemini-2.5-flash-preview-05-20`)

### Selecting local model with Ollama

1. Download the Ollama app for Mac [here](https://ollama.com/download).
2. Pull a local LLM from [Ollama](https://ollama.com/search). As an [example](https://ollama.com/library/deepseek-r1:8b):
```shell
ollama pull deepseek-r1:8b
```
3. Optionally, update the `.env` file with the following Ollama configuration settings. 
* If set, these values will take precedence over the defaults set in the `Configuration` class in `configuration.py`. 
```shell
LLM_PROVIDER=ollama
OLLAMA_BASE_URL="http://localhost:11434" # Ollama service endpoint, defaults to `http://localhost:11434` 
LOCAL_LLM=model # the model to use, defaults to `llama3.2` if not set
```

### Selecting local model with LMStudio

1. Download and install LMStudio from [here](https://lmstudio.ai/).
2. In LMStudio:
   - Download and load your preferred model (e.g., qwen_qwq-32b)
   - Go to the "Local Server" tab
   - Start the server with the OpenAI-compatible API
   - Note the server URL (default: http://localhost:1234/v1)

3. Optionally, update the `.env` file with the following LMStudio configuration settings. 
* If set, these values will take precedence over the defaults set in the `Configuration` class in `configuration.py`. 
```shell
LLM_PROVIDER=lmstudio
LOCAL_LLM=qwen_qwq-32b  # Use the exact model name as shown in LMStudio
LMSTUDIO_BASE_URL=http://localhost:1234/v1
```

### Selecting search tool

By default, it will use [DuckDuckGo](https://duckduckgo.com/) for web search, which does not require an API key. But you can also use [SearXNG](https://docs.searxng.org/), [Tavily](https://tavily.com/) or [Perplexity](https://www.perplexity.ai/hub/blog/introducing-the-sonar-pro-api) by adding their API keys to the environment file. Optionally, update the `.env` file with the following search tool configuration and API keys. If set, these values will take precedence over the defaults set in the `Configuration` class in `configuration.py`. 
```shell
SEARCH_API=xxx # the search API to use, such as `duckduckgo` (default)
TAVILY_API_KEY=xxx # the tavily API key to use
PERPLEXITY_API_KEY=xxx # the perplexity API key to use
MAX_WEB_RESEARCH_LOOPS=xxx # the maximum number of research loop steps, defaults to `3`
FETCH_FULL_PAGE=xxx # fetch the full page content (with `duckduckgo`), defaults to `false`
```

## 🧠 How it works

Local Deep Researcher is inspired by [IterDRAG](https://arxiv.org/html/2410.04343v1#:~:text=To%20tackle%20this%20issue%2C%20we,used%20to%20generate%20intermediate%20answers.). This approach will decompose a query into sub-queries, retrieve documents for each one, answer the sub-query, and then build on the answer by retrieving docs for the second sub-query. Here, we do similar:
- Given a user-provided topic, use a local LLM (via [Ollama](https://ollama.com/search) or [LMStudio](https://lmstudio.ai/)) or a hosted LLM (via [Gemini API](https://aistudio.google.com/)) to generate a web search query
- Uses a search engine / tool to find relevant sources
- Uses LLM to summarize the findings from web search related to the user-provided research topic
- Then, it uses the LLM to reflect on the summary, identifying knowledge gaps
- It generates a new search query to address the knowledge gaps
- The process repeats, with the summary being iteratively updated with new information from web search
- Runs for a configurable number of iterations (see `configuration` tab)

## 🛠️ Tech Stack

- **LangGraph** – Graph-based state management for LLM workflows
- **LangChain** – Framework for building LLM pipelines and agents
- **Ollama / LMStudio** – Run local LLMs via OpenAI-compatible APIs
- **Google GenAI (Gemini)** – Cloud-based LLM via Gemini API
- **Tavily / Perplexity / DuckDuckGo** – Web search integrations
- **python-dotenv** – Manages environment variables
- **uv** – Fast Python package and environment manager