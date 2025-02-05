from query_agent import QueryAgent
from database_setup import Database
import ollama
import uuid

def initialize_sample_data():
    db = Database()
    
    # Add sample inventory items
    db.add_inventory_item({
        "item_id": "1",
        "item_name": "laptop",
        "stock_level": 10
    })
    
    # Add sample supplier
    db.add_supplier({
        "supplier_id": "1",
        "supplier_name": "Tech Supplies Inc",
        "contact_info": "contact@techsupplies.com",
        "item_id": "1"
    })

def main():
    # Check if model exists and pull if needed
    try:
        ollama.pull("deepseek-r1:14b")
    except Exception as e:
        print(f"Error pulling model: {e}")
        return

    # Initialize sample data
    # initialize_sample_data()
    
    # Create a single session ID for the entire chat
    session_id = str(uuid.uuid4())
    print(f"Chat session ID: {session_id}")
    
    # Create query agent with session ID
    agent = QueryAgent(session_id)
    
    print("Inventory Management AI Assistant (using deepseek-r1:14b)")
    print("Type 'exit' to quit")
    
    while True:
        query = input("\nEnter your query: ")
        if query.lower() == 'exit':
            break
            
        response = agent.process_query(query)
        print(response)

if __name__ == "__main__":
    main()
