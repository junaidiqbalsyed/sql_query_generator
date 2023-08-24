
import os
from api_key import openai_aip_return_key
os.environ["OPENAI_API_KEY"] = openai_aip_return_key()

from root.base import  BaseAgent


class Sql_Query_Generator(BaseAgent):
    def __init__(self, llm) -> None:
        super().__init__(llm)
        self.stop_string = "End of SQL"
        self.prompt_template = """
You're an AI master at planning and breaking down a SQL task.
You will be given a task and the schema of database, please helps us in writing excellenct query for '{sql_language}'

generate the query in '{sql_language}' language

Finally, remember to add 'End of SQL' at the end of your sql query.
Schema : '{schema}'.
Task: '{task}'.
query:
"""

    def parse_output(self, result):
        if self.stop_string in result:
            result = result.split(self.stop_string)[1]

        self.write_to_text_file(result)
        return self.remove_newlines_and_spaces(result)
