
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

Example 1:
Task: Count the number of employees in each office in MySQL

query: SELECT o.officeCode, COUNT(*) AS num_employees
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
GROUP BY o.officeCode;

Example 2:
Task:  What time do Brazilian customers tend to buy (Dawn, Morning, Afternoon or Night)? in BigQuery

query: SELECT CASE
    WHEN EXTRACT(HOUR FROM order_purchase_timestamp) BETWEEN 0 AND 5 THEN 'Dawn'
    WHEN EXTRACT(HOUR FROM order_purchase_timestamp) BETWEEN 6 AND 11 THEN 'Morning'
    WHEN EXTRACT(HOUR FROM order_purchase_timestamp) BETWEEN 12 AND 17 THEN 'Afternoon'
    ELSE 'Night'
END AS Time_of_day,
COUNT(order_id) as Order_Count
FROM target.orders
JOIN target.customers
ON orders.customer_id = customers.customer_id
WHERE customers.customer_state IN ('AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO')
GROUP BY Time_of_day
ORDER BY Order_Count DESC;

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
