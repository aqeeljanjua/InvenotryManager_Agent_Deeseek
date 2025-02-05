import json
import ollama
from typing import Dict, Any, Tuple
from database_setup import Database

class QueryGeneratorAgent:
    def __init__(self):
        self.model = "llama2:7b"
        self.db = Database()
        self.schema = self.db.get_collection_schema()
        self._build_schema_context()

    def _parse_user_respose(self, query: str) -> Dict[str, Any]:
        system_prompt = """
        Parse the user query and return a JSON object with the following structure:
        {
            "type": "stock"|"supplier"|"contact_supplier"|"unknown",
            "item": "item name",
            "quantity": number (only for contact_supplier), put 0 if not asked
        }
        Return only the JSON object, no explanation and acknowledgement.
        your response will be a direct input to the system.
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ])
            res= response['message']['content'].strip().replace("\n", "")
            return json.loads(res)
        except Exception as e:
            print(f"Error parsing query: {e}")
            return {"type": "unknown", "item": None}
        
    def _build_schema_context(self):
        """Build a context string describing the database schema"""
        self.schema_context = "Database Collections:\n\n"
        for coll_name, info in self.schema.items():
            self.schema_context += f"Collection: {coll_name}\n"
            self.schema_context += f"Fields: {', '.join(info['fields'])}\n"
            self.schema_context += f"Sample document: {str(info['sample'])}\n"
            self.schema_context += f"Total documents: {info['total_documents']}\n\n"
    def extract_query(self,query):
                system_prompt = f""" Extract the JSON and return only JSON to user.
                Beware! your response will be a direct input to the system so dont acknowledge or explain.

                """
                response = ollama.chat(model=self.model, messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ])
                return response['message']['content'].strip()
    def analyze_query(self, query_text: str) -> Dict[str, Any]:
        # system_prompt = f"""
        # Using this database schema:
        # {self.schema_context}
        
        # Analyze the query without any acknowkedgement or exlaination. Return a JSON for example:
        #  {{operation_type: find/update/insert , collections: list of relevant collections
        # ,query_plan: list of steps with exact field names from schema}}
        #  Only share result json. Remember your response will be a direct input to the system.
       
        # """
        sample = {'collection': 'collection name',
                   'operation': 'find/update/insert',
                     'query': 'mongo query'}
        system_prompt = f"""
        Using this database schema:
        {self.schema_context}. 
        Your response will be a direct input to system.
        Generate a MongoDB query dictionary for pymongo db.execute_query('collection', 'operation', query).
        Respond in JSON, example format:
        {sample} 
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query_text}
            ])
            res = self.extract_query(response['message']['content'].strip().replace("\n", ""))
            res =json.loads(res)
            return res
        except Exception as e:
            print(f"Error analyzing query: {e}")
            return {}

    def generate_query_queryplan(self, query_plan: str) -> Dict[str, Any]:
        system_prompt = f"""
        Given users query plan:
        
        Generate a MongoDB query dictionary for pymongo db.execute_query('collection', 'operation', query).
        Respond in JSON format example:
        {{'collection': 'inventory', 'operation': 'find', 'query': {'item_name': {'$exists': 'true'}}}}
        without any acknowledgement and explaination Use exact field names from schema.
        Return only the query dictionary. your response will be a direct input to system
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(query_plan)}
        ]
        
        try:
            response = ollama.chat(model=self.model, messages=messages)
            query_str = response['message']['content'].strip()
            return eval(query_str)
        except Exception as e:
            print(f"Error generating query: {e}")
            return {}

    def generate_response_template(self, query_analysis: Dict[str, Any],results) -> str:
        system_prompt = """
        Generate a Python f-string template for the response based on the query type.
        Return only the template string, no explanation.
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": str(query_analysis)}
            ])
            return response['message']['content'].strip()
        except Exception as e:
            print(f"Error generating template: {e}")
            return ""
