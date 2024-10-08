import gc
import logging
import os
import threading

from langchain.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_google_genai import ChatGoogleGenerativeAI

from prompts.classification_prompt import classification_prompt


class ClassificationAgent:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-latest",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )
        # Define the File SYstem tools
        self.working_directory = os.path.abspath('./')
        self.toolkit = FileManagementToolkit(root_dir=self.working_directory)
        self.tools = self.toolkit.get_tools()
        self.agent = initialize_agent(self.tools, self.llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                                      verbose=True,
                                      agent_executor_kwards={"handle_parsing_errors": True})

    def __del__(self):
        logging.info("Cleaning up resources for Classification Agent")

    def classify_files(self, file_path, file_name, comparison, similarity):
        """
        Classifiy files depending on results.
        """

        # Write the content to a Markdown file
        report_path = f'{self.working_directory}/data/{file_name}.md'
        with open(report_path, "w") as file:
            file.write(comparison)

        prompt = classification_prompt(self.working_directory, file_path, report_path, similarity)
        logging.info("Calling Tools usage with llm agent")
        self.agent.run(prompt)

        return report_path



def run(state):
    try:
        # Create the agent instance
        task_thread_id = threading.get_ident()
        logging.info(f"Starting classification task on file {state['file_name']}, Thread ID: {task_thread_id}")
        agent = ClassificationAgent()

        # Perform the comparison
        report = agent.classify_files(
            state['file_path'],
            state['file_name'],
            state['result'],
            state['similarity'],
        )
        logging.info(f"Finished classification task on file {state['file_name']}, Thread ID: {task_thread_id}")
    finally:
        # Ensure agent is deleted and garbage collection is triggered
        del agent
        gc.collect()

    # Return the comparison result
    return {"report": report}
