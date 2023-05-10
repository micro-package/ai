
from llama_index import GithubRepositoryReader
from llama_index.langchain_helpers.text_splitter import TokenTextSplitter
import logging
from langchain.chat_models import ChatOpenAI
import os
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, ServiceContext, Document
import nest_asyncio
nest_asyncio.apply()


os.environ["OPENAI_API_KEY"] = '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'
os.environ["GITHUB_TOKEN"] = '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'
docs = GithubRepositoryReader(
    owner='micro-package', repo="storyteller",
    github_token='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', verbose=True,
    concurrent_requests=10).load_data(branch='master')
logging.info(docs)
index = GPTSimpleVectorIndex.from_documents(docs)

index.save_to_disk('index-github.json')
