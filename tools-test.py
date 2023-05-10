
from gpt_index.query_engine.transform_query_engine import TransformQueryEngine
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from gpt_index.langchain_helpers.text_splitter import TokenTextSplitter
import logging
# from llama_index import
from gpt_index.storage.storage_context import StorageContext
from gpt_index import load_index_from_storage, GPTVectorStoreIndex, download_loader,  ServiceContext, SimpleDirectoryReader
from gpt_index.readers.file.base_parser import BaseParser, Dict, Path
from pathlib import Path

from gpt_index.langchain_helpers.agents import LlamaToolkit, create_llama_chat_agent, IndexToolConfig
# define a decompose transform
from gpt_index.indices.query.query_transform.base import DecomposeQueryTransform

from gpt_index import GPTSimpleKeywordTableIndex, LLMPredictor, ServiceContext, Document
from langchain import OpenAI
from gpt_index.indices.composability import ComposableGraph


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


class WithPathParser(BaseParser):
    """Docx parser."""

    def _init_parser(self) -> Dict:
        """Init parser."""
        return {}

    def parse_file(self, file: Path, errors: str = "ignore") -> str:
        """Parse file."""

        data = read_file(file)
        logging.info(file)
        return '//FILEPATH: ' + str(file) + '\n\n' + data


file_extractor = {'.ts': WithPathParser, '.json': WithPathParser}


# directories = [
#     '/home/lukasz/workspace/storyteller/packages/storyteller/src/container']
# index_summaries = ['Storyteller core, implements createPlugin functions and describes plugins interactions after being composed through compose funciton. Uses forgeValueObject function to connect plugins together.']
# directories.extend(map(getPluginPath, plugins))
# index_summaries.extend(map(getPluginSummary, plugins))
ingredients = [
    {
        'type': 'plugin',
        'name': 'axios',
        'dir': "/home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/axios",
        'summary': "Storyteller axios plugin, definition and declaration. Defines actions, hooks, name, requiredPlugins for axios storyteller plugin. It is not related with any other plugins. Axios plugin actions are defined in AxiosActions variable. It does not contain informations about plugins others than storyteller axios plugin. storyteller axios plugin actions",
        'description': "useful for when you want to answer queries about the storyteller axios plugin actions, hooks, name, structure, behaviour and implementation.  It is not useful if you want answer query about any other plugin.",
    },
    {
        'type': 'plugin',
        'name': 'express',
        'dir': "/home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/express",
        'summary': "Storyteller express plugin, definition and declaration. Defines actions, hooks, name, requiredPlugins of express storyteller plugin. It is not related with any other plugins. Express plugin actions are defined in ExpressActions variable. It does not contain informations about plugins others than storyteller express plugin. storyteller express plugin actions",
        'description': "useful for when you want to answer queries about the storyteller express plugin actions, hooks, name, structure, behaviour and implementation.  It is not useful if you want answer query about any other plugin.",
    },
    {
        'type': 'plugin',
        'name': 'storyteller',
        'files': None,
        'dir': "/home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/storyteller",
        'summary': "Storyteller storyteller plugin, definition and declaration. Defines actions, hooks, name, requiredPlugins of storyteller storyteller plugin. It is not related with any other plugins. Storyteller plugin actions are defined in StorytellerActions variable. It does not contain informations about plugins others than storyteller storyteller plugin. storyteller storyteller plugin actions",
        'description': "useful for when you want to answer queries about the storyteller storyteller plugin actions, hooks, name, structure, behaviour and implementation.  It is not useful if you want answer query about any other plugin.",
    },
    {
        'type': 'plugin',
        'name': 'typeorm',
        'files': None,
        'dir': "/home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/typeorm",
        'summary': "Storyteller typeorm plugin, definition and declaration. Defines actions, hooks, name, requiredPlugins for typeorm storyteller plugin. It is not related with any other plugins. Typeorm plugin actions are defined in TypeormActions variable. It does not contain informations about plugins others than storyteller typeorm plugin. storyteller typeorm plugin actions",
        'description': "useful for when you want to answer queries about the storyteller typeorm plugin actions, hooks, name, structure, behaviour and implementation.  It is not useful if you want answer query about any other plugin.",
    },
    {
        'type': 'plugin',
        'name': 'dynamo',
        'files': None,
        'dir': "/home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/dynamo",
        'summary': "Storyteller dynamo plugin, definition and declaration. Defines actions, hooks, name, requiredPlugins for dynamo storyteller plugin. It is not related with any other plugins. Typeorm plugin actions are defined in TypeormActions variable. Dynamo plugin actions are defined in DynamoActions variable. It does not contain informations about plugins others than storyteller dynamo plugin. storyteller dynamo plugin actions",
        'description': "useful for when you want to answer queries about the storyteller dynamo plugin actions, hooks, name, structure, behaviour and implementation.  It is not useful if you want answer query about any other plugin.",
    },
    {
        'type': 'plugin',
        'name': 'step-functions',
        'files': None,
        'dir': "/home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/step-functions",
        'summary': "Storyteller step-functions plugin, definition and declaration. Defines actions, hooks, name, requiredPlugins for step-functions storyteller plugin. It is not related with any other plugins. StepFunctions plugin actions are defined in StepFunctionsActions variable. It does not contain informations about plugins others than storyteller step-functions plugin. storyteller step-functions plugin actions",
        'description': "useful for when you want to answer queries about the storyteller step-functions plugin actions, hooks, name, structure, behaviour and implementation. It is not useful if you want answer query about any other plugin.",
    },
    {
        'type': 'storyteller-container',
        'name': 'storyteller-container',
        'files': None,
        'dir': '/home/lukasz/workspace/storyteller/packages/storyteller/src/container',
        'summary': 'Storyteller core. Allows to create plugins, does not include any plugins on its own. Provides PluginAction interface which is used to defined plugin actions.',
        'description': "useful for when you want to answer queries about plugins interactions and composing, how plugins changes after composing",
    },
    {
        'type': 'framework',
        'name': 'framework',
        'dir': '/home/lukasz/workspace/storyteller/repositories/examples/5.1-real-life-scenario/tests/framework',
        'files': ['framework.ts'],
        'summary': 'Storyteller framework, used for prepareing steps used in test scenarios. Includes file with plugin factories options. Most important it composes plugins into usable framework',
        'description': "useful for when you want to answer queries about which plugins are used and available across tests scenarios",
    },
    {
        'type': 'steps',
        'name': 'steps',
        'dir': '/home/lukasz/workspace/storyteller/repositories/examples/5.1-real-life-scenario/tests/framework',
        'files': ['act.ts', 'arrange.ts'],
        'summary': 'Storyteller steps created using storyteller storyteller plugin createStep action. Steps are used across many test scenarios.',
        'description': "useful when you want to know what exactly is particular step doing. It is not useful while answering queries about plugins",
    },
    {
        'type': 'tests',
        'name': 'tests',
        'dir': '/home/lukasz/workspace/storyteller/repositories/examples/5.1-real-life-scenario/tests/user-needs-to-know',
        'files': None,
        'summary': 'Tests scenarios created using storyteller storyteller plugin action storytellerCreateStory. Each story is builded from steps. Executing tests starts application with http server and mocks third party APIs used by application.',
        'description': "useful when you want to know what is the sequence of steps and steps configuration",
    },
    {
        'type': 'src',
        'name': 'src',
        'dir': '/home/lukasz/workspace/storyteller/repositories/examples/5.1-real-life-scenario/src',
        'files': None,
        'summary': 'Source code of application. This application is tested using test scenarios.',
        'description': "useful when you want to know what tests are testing",
    },
]


def addPath(path):
    def addFilename(filename):
        return f"{path}/{filename}"


text_splitter = TokenTextSplitter(
    separator="\n", chunk_size=3900, chunk_overlap=200)
doc_set = {}
all_docs = []
for ingredient in ingredients:
    files = ingredient.get('files')
    input_files = None if files is None else map(
        addPath(ingredient.get('dir')), files)
    logging.info(str(input_files))
    plugin_docs = SimpleDirectoryReader(
        ingredient.get("dir"), recursive=True, exclude=["**/*.spec.ts"], file_extractor=file_extractor).load_data()
    # insert year metadata into each year
    for d in plugin_docs:
        d.extra_info = {
            "name": f"{ingredient.get('type')}/{ingredient.get('name')}"}
    doc_set[ingredient.get("name")] = plugin_docs
    all_docs.extend(plugin_docs)
# initialize simple vector indices + global vector index
llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0, model_name="gpt-3.5-turbo"))
service_context = ServiceContext.from_defaults(
    llm_predictor=llm_predictor, chunk_size_limit=4096)
index_set: Dict[str, GPTVectorStoreIndex] = {}
for ingredient in ingredients:
    for doc in doc_set[ingredient.get("name")]:
        text_chunks = text_splitter.split_text(doc.text)
        doc_chunks = [Document(t) for t in text_chunks]
        for doc_chunk in doc_chunks:
            logging.info(doc_chunk.doc_id)
            storage_context = StorageContext.from_defaults()
            cur_index = GPTVectorStoreIndex.from_documents(
                [doc_chunk],
                service_context=service_context,
                storage_context=storage_context,
            )
            # TODO remove + str(doc_chunk.doc_id) to get more visibility on used indexes
            index_set[ingredient.get(
                "name") + str(doc_chunk.doc_id)] = cur_index
    storage_context.persist(
        persist_dir=f'./storage/{ingredient.get("type")}/{ingredient.get("name")}')
logging.info(2)
for ingredient in ingredients:
    storage_context = StorageContext.from_defaults(
        persist_dir=f'./storage/{ingredient.get("type")}/{ingredient.get("name")}')
    cur_index = load_index_from_storage(storage_context=storage_context)
    index_set[ingredient.get("name")] = cur_index


# describe each index to help traversal of composed graph


# define an LLMPredictor set number of output tokens
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
storage_context = StorageContext.from_defaults()

# define a list index over the vector indices
# allows us to synthesize information across each index
graph = ComposableGraph.from_indices(
    GPTSimpleKeywordTableIndex,
    [index_set[ingredient.get('name')] for ingredient in ingredients],
    index_summaries=[ingredient.get('summary') for ingredient in ingredients],
    service_context=service_context,
    storage_context=storage_context,
)
query_engine = graph.as_query_engine()


def ask(prompt):
    logging.info(prompt)
    response = query_engine.query(
        prompt,
    )
    logging.info(str(response))
    logging.info(response.get_formatted_sources())


ask("""I made change to "User needs to know what is the *average age* for specific name / happy path" currently assert sections looks like:
```
      assert: testFramework.createStep({
        name: StepName.assert,
        handler: async (valueObject) => {
          const nameToAgeResponses = valueObject.axiosGetResponses({ endpointName: AppEndpointName.averageAgeForName });
          expect(nameToAgeResponses.length).toStrictEqual(1);
          expect(nameToAgeResponses[0].response.data.age).toStrictEqual(
            nameToAgeResponses
              .map((nameToAgeResponse) => nameToAgeResponse.response.data.age)
              .reduce((acc, val) => acc + val, 0) / nameToAgeResponses.length + 1,
          );
        },
      }),
```
Could you provide a change to application source code which will make this new changed test passing?
""")

# root_id = graph.root_id

# # [optional] save to disk
# storage_context.persist(persist_dir=f'./storage/root')

# # [optional] load from disk, so you don't need to build graph from scratch
# # graph = load_graph_from_storage(
# #     root_id=root_id,
# #     service_context=service_context,
# #     storage_context=storage_context,
# # )
# decompose_transform = DecomposeQueryTransform(
#     llm_predictor, verbose=True
# )

# # define custom retrievers

# # custom_query_engines = {}
# # for index in index_set.values():
# #     query_engine = index.as_query_engine()
# #     query_engine = TransformQueryEngine(
# #         query_engine,
# #         query_transform=decompose_transform,
# #         transform_extra_info={'index_summary': index.index_struct.summary},
# #     )
# #     custom_query_engines[index.index_id] = query_engine
# # custom_query_engines[graph.root_id] = graph.root_index.as_query_engine(
# #     response_mode='tree_summarize',
# #     verbose=True,
# # )

# # tool config
# graph_config = IndexToolConfig(
#     query_engine=graph.as_query_engine(),
#     name=f"Graph Index",
#     description="useful for when you want to answer queries that require analyzing storyteller plugin structures and behaviour",
#     tool_kwargs={"return_direct": True}
# )
# index_configs = []
# # for ingredient in ingredients:
# #     query_engine = index_set[ingredient.get("name")].as_query_engine(
# #         similarity_top_k=3,
# #     )
# #     tool_config = IndexToolConfig(
# #         query_engine=query_engine,
# #         name=f"Vector Index {ingredient.get('name')}",
# #         description=ingredient.get("description"),
# #         tool_kwargs={"return_direct": True}
# #     )
# #     index_configs.append(tool_config)

# #     toolkit = LlamaToolkit(
# #         index_configs=index_configs + [graph_config],
# #     )
# toolkit = LlamaToolkit(
#     index_configs=[graph_config],
# )


# memory = ConversationBufferMemory(memory_key="chat_history")
# llm = ChatOpenAI(
#     temperature=0, model_name="gpt-3.5-turbo")
# agent_chain = create_llama_chat_agent(
#     toolkit,
#     llm,
#     memory=memory,
#     verbose=True
# )

# agent_chain.run(
#     input=""")
# # agent_chain.run(
# #     input="Please list all hooks names defined in axios plugin")
# # agent_chain.run(
# #     input="Please list all hooks names defined in express plugins")
# # agent_chain.run(
# #     input="Please list all hooks names defined in typeorm plugins")
