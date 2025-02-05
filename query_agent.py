from database_setup import Database
from ollama_helper import OllamaAgent
from prompt_manager import PromptManager
import json

class QueryAgent:
    def __init__(self, session_id: str = None):
        self.db = Database()
        self.ollama = OllamaAgent(session_id)
        self.schema = self.db.get_collection_schema()
        self.prompt_manager = PromptManager()

    def extract_query(self,query):
                # system_prompt = f""" Extract the JSON and return only JSON to user.
                # Beware! your response will be a direct input to the system so dont acknowledge or explain.

                # """
                # response = self.ollama.chat(system_prompt, query)
                # return response['message']['content'].strip()
        parsed = query.replace("```json", "").replace("```", "").strip()
        return parsed
    def process_query(self, query: str) -> str:
        try:
            # Get query plan from LLM
            parser_response = self.ollama.chat(
                self.prompt_manager.get_query_parser_prompt(str(self.schema)),
                query
            )
            if "</think>" not in parser_response:
                parser_response = "</think>"+parser_response
            resp = self.extract_query(parser_response.split("</think>")[1])
            
            query_plan = json.loads(resp)
            
            # Execute database query
            results = self.db.execute_query(
                query_plan['collection'],
                query_plan['operation'],
                query_plan['query']
            )
            
            # Format response using LLM
            response = self.ollama.chat(
                self.prompt_manager.get_response_formatter_prompt(),
                f"Template: {query_plan['response_template']}\nData: {str(results)}"
            )
            
            return response
            
        except Exception as e:
            error_response = self.ollama.chat(
                self.prompt_manager.get_error_handler_prompt(),
                str(e)
            )
            return error_response
