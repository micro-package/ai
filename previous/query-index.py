from llama_index import GPTSimpleVectorIndex, Document
import logging
import os

os.environ["OPENAI_API_KEY"] = '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'
# load from disk
index = GPTSimpleVectorIndex.load_from_disk('index.json')
# logging.info(index.query(
#     "Explain me what are the dependencies of examples-5.1-real-life-scenario package?"))
# logging.info(index.query(
#     "Explain me what tests in examples-5.1-real-life-scenario package are testing?"))
# logging.info(index.query(
#     "What functionalities of application are tested in examples-5.1-real-life-scenario tests?"))
# logging.info(index.query('''I loaded files to gpt index, some of those files are had to many tokens. All of the files uses specific prefixes and postfixes, those 2 indicates the file.
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
# '''))
# logging.info(index.query(
#     'What do you know about "User needs to know what is the *age* for specific *name* / happy path" test scenario? I would like to know detailed information about what is storyteller framework doing during execution. Please include information about all http requests that may happend during test execution. Please ignore assert section of test scenario, also provide all http requests in curl format.'))
# index.insert(Document())
# logging.info(index.query(
#     'Provide accurate explanation on how storyteller hooks are used in axios plugin. Please list all hooks used by axios plugin.'))


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


# askAndStore(
#     'Please tell me how dynamodb is used in "examples-5.1-real-life-scenario" tests')
# askUntilFinished("Storyteller framework is testing framework. It is used for testing application interactions with external resources. Storyteller framework itself requests application endpoints and tracks application interaction between external resources. For example application may perform http request to external API in this case storyteller framework starts http server in order to mock application external resource. When storyteller framework starts it requires running application in order to perform tests.")

# askUntilFinished(
#     'Please tell me on which url and port application tested by tests is running')
# askUntilFinished(
#     'Please describe in details each of http requests performed during "User needs to know how many times asked for *age* for specific *name* / happy path" test. I want you to provide detailed description for each of the requests and documentation in curl format.')
# askUntilFinished(
#     'Please describe in details each of http requests performed during storyteller tests. I want you to provide small description for each of the requests and documentation in curl format.')
# askUntilFinished(
#     'Please list all directories inside examples-5.1-real-life-scenario repository, filepath is stored should be inside each embedding')
# askUntilFinished(
#     "Please show me content of entire file with storyteller plugin implementation. I want to have exactly the same file I loaded to index in the response")
# askUntilFinished(
#     "Please provide me entire content of /home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/axios/index.ts file. Please provide only file content, don't try to figure out missing pieces on your own.")
# logging.info(index.query(
#     "Your response must not contain more than 200 characters. Please provide me only first 200 characters of /home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/axios/index.ts file."))
# logging.info(index.query(
#     """Please provide me content of /home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/axios/index.ts file."""))
# logging.info(index.query(
#     """Please provide me content of /home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/axios/index.ts file after 'import { AXIOS_PLUG } from "./name";' string. Please include imports."""))

# logging.info(index.query(
#     'Please list all plugins'))
# logging.info(index.query(
#     'Please tell me what hooks are runned by storyteller axiosPlugin actions, those actions are defined in axiosPlugin'))
# logging.info(index.query(
#     'Please list all storyteller plugins used in steps in sections of "User needs to know how many times asked for *age* for specific *name* / happy path" test scenario'))
# logging.info(index.query(
#     'All plugins are loaded into framework, by compose function. In order to use plugin, steps executes plugin actions. Those plugins are used in all steps. Steps are used in each test scenario. Plugin actions are used in steps. Please tell what storyteller plugins actions are used in "User needs to know how many times asked for *age* for specific *name* / happy path" steps'))
# logging.info(index.query(
#     'Plugins are loaded to the framework by compose function. Plugins are used in storyteller steps to perform actions. All steps are created by using storyteller plugin createStep action. Steps are used in sections created by storyteller plugin createSection action. Could you list all used plugin actions and steps in separate groups?'))
# prompt = """
# Each plugin must be executed like function with arguments before composing in compose function.
# Each of plugins exposes: name, requiredPlugins, state, actions and hooks.
# Plugin hooks and state are never exposed.
# Plugin actions are defined under actions property and available to use by developer, this is the way to execute plugin functionalities.
# Plugin actions are always exposed.
# TestFramework is created by composing plugins factories with createValueObject at the beggining also with forgeValueObject and storytellerHelper at then end.

# Please show me how testFramework is composed.
# """
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
prompt = """
Steps used in test scenario are loaded into your knowledge base, you need to find steps for each scenario.
Steps are shared in between test scenarios, each test scenario uses existing step.
For example in scenario: "User needs to know what is the *average age* for specific name / happy path" there is step called "arrangeClearAgeNamePairTable".
This step implementation already exists in your knowledge base and is:
"
export const arrangeClearAgeNamePairTable = () =>
  testFramework.createStep({
    name: StepName.arrangeClearAgeNamePairTable,
    handler: async (valueObject) => {
      await valueObject.typeormGetManager({ name: DataSourceName.postgres }).getRepository(AgeNamePair).delete({});
    },
  });
"
Implementation of all used steps exists in your knowledge base.

Please generate end user documentation for "User needs to know what is the *average age* for specific name / happy path" test scenario from application perspective using adverbial of the sentence. Please provide result in json format.
"""
askUntilFinished(prompt)
# In order to build test case, testFramework allows to create scenario this does not affect how plugins work.
# prompt = """Each plugin must be executed like function with parameters before using.
#     TestFramework is loaded by composing plugins into valueObject.
#     Compose function result with storytellerPlugin actions.
#     StorytellerPlugin createStep action exposes every other plugin actions.
#     Plugin expose functions called actions.
#     Each test scenario is created using storytellerPlugin createScenario action.
#     Inside each created scenario there are 3 sections: Arrange, Act, Assert.
#     Each of the sections needs to contain at least 1 step.
#     There may be more steps using storytellerPlugin composeSection action.
#     Each step is provided with access to all previously composed plugin actions.
#     Please list all steps used in "User needs to know what is the *age* for specific *name* / happy path" test scenario."""
# logging.info(prompt)
# logging.info(index.query(prompt))
# logging.info(index.query(
#     """Each plugin must be executed like function with parameters before using.
#     TestFramework is loaded by composing plugins into valueObject.
#     Compose function result with storytellerPlugin actions.
#     StorytellerPlugin createStep action exposes every other plugin actions.
#     Plugin expose functions called actions.
#     Each test scenario is created using storytellerPlugin createScenario action.
#     Inside each created scenario there are 3 sections: Arrange, Act, Assert.
#     Each of the sections needs to have at least 1 step.
#     There may be more steps using storytellerPlugin composeSection action.
#     Each step is provided with access to all previously composed plugin actions.
#     Please list all plugin actions defined in storyteller axiosPlugin."""))
# logging.info(index.query(
#     """Please provide me entire content of /home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/axios/index.ts file. Please provide only file content, don't try to figure out missing pieces on your own. I want all the file content after lines below:

# } from "./types";
# import { AxiosHookName } from "./types";

# export const axiosPlugin = <
#     """))
# logging.info(index.query(
#     """Please provide me entire content of /home/lukasz/workspace/storyteller/packages/storyteller/src/plugins/axios/index.ts file. Please provide only file content, don't try to figure out missing pieces on your own. I want all the file content after lines below:

#   });
#   Object.entries(hooks).forEach(([hookName, hook]) => {
#     plugin.hooks[hookName] = (payload?: any) => {
#     """))
# logging.info(index.query(
#     """Please provide me entire content of /home/lukasz/workspace/storyteller/packages/storyteller/src/container/plugin.ts. Please provide only file content, don't try to figure out missing pieces on your own. I want every content after lines below:

#       const actionResult = action(payload);
#       if (actionResult instanceof Promise) {
#         return actionResult.catch((error) => {
#     """))
# logging.info(index.query(
#     """Please provide me entire content of /home/lukasz/workspace/storyteller/packages/storyteller/src/container/plugin.ts. Please provide only file content, don't try to figure out missing pieces on your own. I want every content after those lines:

# >(
#   valueObject: ValueObject<Status.created, TPrevHookDefinition, TPrevPlugin>,
# ) => ValueObject<Status.
#     """))
# askAndStore(
#     'It does not look like all of the implementation, could you provide more content?')
# askAndStore(
#     "This is not axios plugin implementation, it is missing hooks and entire createPlugin function")
# askAndStore(
#     "This is not axios plugin implementation, it is missing hooks and entire createPlugin function. Could you try again?")
# askUntilFinished(
#     'Please describe me test scenario called "User needs to know how many times asked for *age* for specific *name* / happy path"')

# askUntilFinished(
#     'Please describe all application endpoints used in tests, then explain all write an application in javascript that will make all tests from "examples-5.1-real-life-scenario" passing. Please do not use comments.')

# logging.info(index.query('''Please tell which description is more accurate, I provide you with 2 generated texts prefixed with Number 1, and Number 2. I would like you to compare both texts, content of each text is inside """ """. Explain why decided to pick.
# Number 1 - """Storyteller hooks are a way to add custom logic to the Storyteller framework. They allow developers to define custom functions that can be called at certain points in the Storyteller lifecycle. The Hook interface defines a name and a handler function that will be called when the hook is triggered. The handler function takes a ValueObject as an argument, which contains the status of the Storyteller instance, as well as any additional data that may be needed. The HookDefinition interface defines the name and payload of the hook, which is the data that will be passed to the handler function when the hook is triggered. The PrimaryHookName enum defines the two primary hooks that can be used, beforeHook and afterHook. The PrimaryHookDefinition type defines the type of hook that can be used, either beforeHook or afterHook, and the type of payload that will be passed to the handler function."""
# Number 2 - """Storyteller hooks are a way to add custom logic to the Storyteller framework. They allow developers to define custom functions that can be called at certain points in the Storyteller lifecycle. The hook.ts file defines the interface for creating and using hooks.

# The HookHandler interface defines a function that takes a ValueObject as an argument and returns a Promise of void. This function is the actual hook that will be called at the appropriate time.

# The HookDefinition interface defines the name of the hook and the payload that will be passed to the hook when it is called.

# The Hook interface defines the name of the hook and the handler function that will be called when the hook is triggered.

# The PrimaryHookName enum defines the two primary hooks that can be used in Storyteller: beforeHook and afterHook.

# The PrimaryHookDefinition interface defines the type of hook that can be used for each of the primary hooks.

# When a hook is triggered, the handler function defined in the Hook interface will be called with the payload defined in the HookDefinition interface. The handler function can then perform any custom logic that is needed."""

# '''))
