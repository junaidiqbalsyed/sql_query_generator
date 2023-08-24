
import abc
import warnings
warnings.filterwarnings('ignore')
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate

class BaseAgent:
    def __init__(self, llm) -> None:
        self.llm = llm

    @abc.abstractmethod
    def parse_output(self, raw_result, parsed_output):
        raise NotImplementedError()

    # function to remove new lines and spaces
    def remove_newlines_and_spaces(self, input_string):
        cleaned_string = input_string.replace('\n', ' ').replace(' ', '')
        return cleaned_string


    def execute_task(self, **kwargs):

        self.task_name = kwargs['task'].replace(' ', '_')
        # convert this to a system message
        template = SystemMessagePromptTemplate.from_template(
            self.prompt_template)

        chat_prompt = ChatPromptTemplate.from_messages([template])

        # provide the input i.e., task
        prompt = chat_prompt.format_prompt(**kwargs).to_messages()

        # get the raw data from the llm
        raw_result = self.llm(prompt, stop=[self.stop_string])

        # parse the llm output
        parsed_result = self.parse_output(raw_result.content)

        return parsed_result

    def write_to_text_file(self, content):
        with open(f"./generated_sql_quey/{self.task_name}.txt", 'w') as file:
            file.write(content)


