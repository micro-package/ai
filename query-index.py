from llama_index import GPTSimpleVectorIndex, Document
import logging
import os

os.environ["OPENAI_API_KEY"] = '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'
# load from disk
index = GPTSimpleVectorIndex.load_from_disk('./indexes/axiosPlugin.json')


def askAndStore(prompt):
    result = index.query(prompt)
    logging.info(result)
    index.insert(Document("[QUESTION]: " + prompt +
                          "\n[RESPONSE]: " + result.response))
    return result


def askUntilFinished(prompt, originalPrompt=None):
    extendedPrompt = prompt + \
        ' If you finished this response please add "[FINISHED]" at the end of response.'
    result = askAndStore(extendedPrompt)
    if "[FINISHED]" not in result.response:
        askUntilFinished(
            'It looks like you didnt finished last response. I asked you "' + originalPrompt if originalPrompt is not None else extendedPrompt+'" could you continue from last line you finished? If you finished please respond with just "[FINISHED]" otherwise continue your response from last line', extendedPrompt)

# prompt = """
# TestFramework is created by composing plugins factories with createValueObject at the beggining also with forgeValueObject and storytellerHelper at then end.
# Each of plugin factories is provided with configuration before being composed.
# Each of plugins contains always exposed actions, those actions are allows user to interact with plugin.
# All composed plugins actions are available in valueObject.
# Each plugin expose functions called actions.
# Keep in mind that "forgeValueObject", "createValueObject" and "storytellerHelper" are not a plugins.

# Please list all plugin testFramework is composed with.
# Please list all valueObject actions.
# """
# prompt = """
# Please generate end user documentation for "User needs to know what is the *average age* for specific name / happy path" test scenario.
# Test case utilizes storyteller framework with expressPlugin, axiosPlugin and other plugins.
# Keep in mind that test case uses some (not all) steps created by storytellerPlugin.
# """
# prompt = """
# Steps used in test scenario are loaded into your knowledge base, you need to find steps for each scenario.
# Steps are shared in between test scenarios, each test scenario uses existing step.
# For example in scenario: "User needs to know what is the *average age* for specific name / happy path" there is step called "arrangeClearAgeNamePairTable".
# This step implementation already exists in your knowledge base and is:
# "
# export const arrangeClearAgeNamePairTable = () =>
#   testFramework.createStep({
#     name: StepName.arrangeClearAgeNamePairTable,
#     handler: async (valueObject) => {
#       await valueObject.typeormGetManager({ name: DataSourceName.postgres }).getRepository(AgeNamePair).delete({});
#     },
#   });
# "
# Implementation of all used steps exists in your knowledge base.


# Please generate end user documentation for "User needs to know what is the *average age* for specific name / happy path" test scenario from application perspective using adverbial of the sentence. Please provide result in json format.
# """
prompt = """

Show me the axios plugin hooks implementation?
"""
askUntilFinished(prompt)
