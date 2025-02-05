class PromptManager:
    @staticmethod
    def get_query_parser_prompt(schema_context: str) -> str:
        return f"""You are a database query interpreter.
        Given this database schema:
        {schema_context}
        
        Convert the user's natural language query into a structured query plan.
        Return only a JSON object with this structure:
        {{
            "collection": "collection_name",
            "operation": "find/update/insert",
            "query": {{MongoDB query dictionary}},
            "response_template": "Template to format the response"
        }}
        No explanation, just the JSON."""

    @staticmethod
    def get_response_formatter_prompt() -> str:
        return """Format the query results into a natural response.
        Use the provided template and data to create a conversational response.
        Focus on clarity and completeness.
        Return only the formatted response, no explanations ot thinking."""

    @staticmethod
    def get_error_handler_prompt() -> str:
        return """Handle the error condition and generate an appropriate user-friendly message.
        Keep the response concise and helpful.
        Suggest potential fixes if possible.
        Return only the error message, no explanations."""
