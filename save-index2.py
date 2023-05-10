from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, ServiceContext, Document
from llama_index.readers.file.base_parser import BaseParser, Dict, Path
import os
from langchain.chat_models import ChatOpenAI
import logging
from llama_index.langchain_helpers.text_splitter import TokenTextSplitter
from llama_index import SimpleDirectoryReader, Document


def flatten(lst):
    """
    Flatten a list that contains other lists
    """
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list


os.environ["OPENAI_API_KEY"] = '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'


text_splitter = TokenTextSplitter(
    separator="\n", chunk_size=3900, chunk_overlap=200)


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

# storytellerPackageJson = SimpleDirectoryReader(
#     '/home/lukasz/workspace/storyteller/packages/storyteller/.dist', ['/home/lukasz/workspace/storyteller/packages/storyteller/.dist/package.json'], exclude=["**/*.spec.ts"], file_extractor=file_extractor).load_data()
# storytellerCommon = SimpleDirectoryReader(
#     '/home/lukasz/workspace/storyteller/packages/storyteller/src/common', recursive=True, exclude=["**/*.spec.ts"], file_extractor=file_extractor).load_data()
# storytellerSrc = SimpleDirectoryReader(
#     '/home/lukasz/workspace/storyteller/packages/storyteller/src/container', recursive=True, exclude=["**/*.spec.ts"], file_extractor=file_extractor).load_data()
axiosPlugin = SimpleDirectoryReader(
    '/home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/axios', recursive=True, exclude=["**/*.spec.ts"], file_extractor=file_extractor).load_data()
# storytellerStorytellerPlugin = SimpleDirectoryReader(
#     '/home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/storyteller', recursive=True, exclude=["**/*.spec.ts"], file_extractor=file_extractor).load_data()
# typeormStorytellerPlugin = SimpleDirectoryReader(
#     '/home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/typeorm', recursive=True, exclude=["**/*.spec.ts"], file_extractor=file_extractor).load_data()
# dynamodbStorytellerPlugin = SimpleDirectoryReader(
#     '/home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/dynamodb', recursive=True, exclude=["**/*.spec.ts"], file_extractor=file_extractor).load_data()
# expressStorytellerPlugin = SimpleDirectoryReader(
#     '/home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/express', recursive=True, exclude=["**/*.spec.ts"], file_extractor=file_extractor).load_data()
# packageJson = SimpleDirectoryReader(
#     '/home/lukasz/workspace/storyteller/repositories/examples/5.1-real-life-scenario', ['/home/lukasz/workspace/storyteller/repositories/examples/5.1-real-life-scenario/package.json', '/home/lukasz/workspace/storyteller/repositories/examples/5.1-real-life-scenario/config.ts'], exclude=["**/*.spec.ts"], file_extractor=file_extractor).load_data()
# testsFramework = SimpleDirectoryReader(
#     '/home/lukasz/workspace/storyteller/repositories/examples/5.1-real-life-scenario/tests/framework', recursive=True, file_extractor=file_extractor).load_data()
# tests = SimpleDirectoryReader(
#     '/home/lukasz/workspace/storyteller/repositories/examples/5.1-real-life-scenario/tests/user-needs-to-know', recursive=True, file_extractor=file_extractor).load_data()
# logging.info('storytellerSrcSize: ' + str(len(storytellerSrc)))
# logging.info('storytellerTestsSize: ' + str(len(tests)))

# axiosPlugin = SimpleDirectoryReader("/home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/axios", input_files=[
#                                     '/home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/axios/index.ts']).load_data()


logging.info(1)
llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0, model_name="gpt-4"))
logging.info(2)
service_context = ServiceContext.from_defaults(
    llm_predictor=llm_predictor, chunk_size_limit=4096)
logging.info(3)
index = GPTSimpleVectorIndex.from_documents([], None, service_context)
logging.info(4)
# logging.info(len(storytellerPackageJson))
# documents = flatten(
#     [
#         axiosPlugin,
#         # storytellerStorytellerPlugin,
#         # typeormStorytellerPlugin,
#         # dynamodbStorytellerPlugin,
#         # storytellerCommon,
#         # storytellerSrc,
#         # testsFramework, tests,
#         # expressStorytellerPlugin,
#         # tests
#     ])
# for document in documents:
for document in axiosPlugin:
    text_chunks = text_splitter.split_text(document.text)
    doc_chunks = [Document(t) for t in text_chunks]
    for doc_chunk in doc_chunks:
        logging.info(doc_chunk.doc_id)
        index.insert(doc_chunk)
index.save_to_disk('./indexes/axiosPlugin.json')


# index.insert(Document('''
# I loaded files to gpt index, some of those files are had to many tokens. All of the files uses specific prefixes and postfixes, those 2 indicates the file.
# For example I have file that is loaded fully in one chunk and here it is this file content.

# -{storyteller}:{file-start}:{filepath=/home/lukasz/workspace/storyteller/packages/storyteller/src/index.ts}:{tokens=279}:{characters:883}:{firstCharacterIndex:0}:{lastCharacterIndex:279}-
# export * from "./container/hook";
# export * from "./container/plugin";
# export * from "./container/value-object";
# export * from "./plugins/axios";
# export * from "./plugins/dynamo";
# export * from "./plugins/express";
# export * from "./plugins/step-functions";
# export * from "./plugins/storyteller";
# export * from "./plugins/typeorm";
# export * from "./plugins/axios/types";
# export * from "./plugins/dynamo/types";
# export * from "./plugins/express/types";
# export * from "./plugins/step-functions/types";
# export * from "./plugins/storyteller/types";
# export * from "./plugins/typeorm/types";
# export * from "./plugins/axios/name";
# export * from "./plugins/dynamo/name";
# export * from "./plugins/express/name";
# export * from "./plugins/step-functions/name";
# export * from "./plugins/storyteller/name";
# export * from "./plugins/typeorm/name";
# export { pipe as compose } from "ts-pipe-compose";

# -{storyteller}:{file-start}:{filepath=/home/lukasz/workspace/storyteller/packages/storyteller/src/index.ts}:{tokens=279}:{characters:883}-

# As you can see there is '{storyteller}:{file-start}' prefix with additional information, the prefix tells that file is finished or not, if you see there that amout of tokens from {tokens=279} is equal to {lastCharacterIndex:279} it will be end of file.
# On the other hand, if this condition is not met, this is not end of the file and you need to look for other part to understand context of questions completely. I want you to from now on to use this knowledge while using index.
# Also keep in mind that filepath in {filepath=/home/lukasz/workspace/storyteller/packages/storyteller/src/index.ts} is a original file path of source file.'''))
# logging.info(5)
# save to disk

# index.insert(Document("""

# """))
