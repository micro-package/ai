
from gpt_index.query_engine.transform_query_engine import TransformQueryEngine
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
import logging
from llama_index import download_loader, GPTVectorStoreIndex, ServiceContext, SimpleDirectoryReader
from gpt_index.storage.storage_context import StorageContext
from gpt_index import load_index_from_storage
from llama_index.readers.file.base_parser import BaseParser, Dict, Path
from pathlib import Path

from llama_index.langchain_helpers.agents import LlamaToolkit, create_llama_chat_agent, IndexToolConfig
# define a decompose transform
from llama_index.indices.query.query_transform.base import DecomposeQueryTransform

from llama_index import GPTListIndex, LLMPredictor, ServiceContext
from langchain import OpenAI
from llama_index.indices.composability import ComposableGraph

graph = load_graph_from_storage(
    root_id=root_id,
    service_context=service_context,
    storage_context=storage_context,
)
decompose_transform = DecomposeQueryTransform(
    llm_predictor, verbose=True
)

# define custom retrievers

custom_query_engines = {}
for index in index_set.values():
    query_engine = index.as_query_engine()
    query_engine = TransformQueryEngine(
        query_engine,
        query_transform=decompose_transform,
        transform_extra_info={'index_summary': index.index_struct.summary},
    )
    custom_query_engines[index.index_id] = query_engine
custom_query_engines[graph.root_id] = graph.root_index.as_query_engine(
    response_mode='tree_summarize',
    verbose=True,
)

# tool config
graph_config = IndexToolConfig(
    query_engine=query_engine,
    name=f"Graph Index",
    description="useful for when you want to answer queries that require analyzing storyteller plugin structures and behaviour",
    tool_kwargs={"return_direct": True}
)
index_configs = []
for plugin in plugins:
    query_engine = index_set[plugin].as_query_engine(
        similarity_top_k=3,
    )
    tool_config = IndexToolConfig(
        query_engine=query_engine,
        name=f"Vector Index {plugin}",
        description=f"useful for when you want to answer queries about the storyteller {plugin} plugin structure, behaviour and implementation",
        tool_kwargs={"return_direct": True}
    )
    index_configs.append(tool_config)

    toolkit = LlamaToolkit(
        index_configs=index_configs + [graph_config],
    )

memory = ConversationBufferMemory(memory_key="chat_history")
llm = ChatOpenAI(
    temperature=0, model_name="gpt-4")
agent_chain = create_llama_chat_agent(
    toolkit,
    llm,
    memory=memory,
    verbose=True
)

agent_chain.run(input="Please provide information about all plugin hooks")
