from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

import json
from types import SimpleNamespace

class ReflectionOutputFormatter(BaseModel):
    '''Discovered knowledge gap based on summary and follow-up question to expand understanding.'''
    knowledge_gap: str
    follow_up_query: str

class QueryOutputFormatter(BaseModel):
    '''A query based on user instruction along with rationale for building that query.'''
    query: str
    rationale: str

# Generate Query
class GoogleQueryGenerator:
    def __init__(self, google_api_key, model, temperature, max_retries):
        llm = ChatGoogleGenerativeAI(
            google_api_key=google_api_key,
            model=model,
            temperature=temperature,
            max_retries=max_retries,
        )
        self.llm_json_mode = llm.with_structured_output(QueryOutputFormatter)
    
    def invoke(self, message_array):
        result = self.llm_json_mode.invoke(message_array)
        return SimpleNamespace(
            content=json.dumps({
                'query': result.query, 
                'rationale': result.rationale
            })
        )

# Summarise sources
class GoogleSummarizer:
    def __init__(self, google_api_key, model, temperature, max_retries):
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=google_api_key,
            model=model,
            temperature=temperature,
            max_retries=max_retries,
        )

    def invoke(self, message_array):
        result = self.llm.invoke(message_array)
        return SimpleNamespace(content=result)

# Reflect on summary
class GoogleReflector:
    def __init__(self, google_api_key, model, temperature, max_retries):
        llm = ChatGoogleGenerativeAI(
            google_api_key=google_api_key,
            model=model,
            temperature=temperature,
            max_retries=max_retries,
        )
        self.llm_json_mode = llm.with_structured_output(ReflectionOutputFormatter)

    def invoke(self, message_array):
        result = self.llm_json_mode.invoke(message_array)
        return SimpleNamespace(
            content=json.dumps({
                'knowledge_gap': result.knowledge_gap, 
                'follow_up_query': result.follow_up_query
            })
        )