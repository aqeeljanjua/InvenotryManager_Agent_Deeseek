from pymongo import MongoClient
from typing import Dict, Any, List
from datetime import datetime

class Database:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['inventory_management']
        
        # Create collections if they don't exist
        if 'inventory' not in self.db.list_collection_names():
            self.db.create_collection('inventory')
        if 'suppliers' not in self.db.list_collection_names():
            self.db.create_collection('suppliers')
        if 'chat_history' not in self.db.list_collection_names():
            self.db.create_collection('chat_history')
    
    def add_inventory_item(self, item: Dict[str, Any]) -> bool:
        try:
            self.db.inventory.insert_one(item)
            return True
        except Exception as e:
            print(f"Error adding inventory item: {e}")
            return False
    
    def add_supplier(self, supplier: Dict[str, Any]) -> bool:
        try:
            self.db.suppliers.insert_one(supplier)
            return True
        except Exception as e:
            print(f"Error adding supplier: {e}")
            return False
    
    def get_stock_level(self, item_name: str) -> Dict[str, Any]:
        return self.db.inventory.find_one({"item_name": item_name})
    
    def get_supplier_for_item(self, item_id: str) -> Dict[str, Any]:
        return self.db.suppliers.find_one({"item_id": item_id})

    def get_all_inventory(self) -> List[Dict[str, Any]]:
        return list(self.db.inventory.find({}, {'_id': 0}))
    
    def get_all_suppliers(self) -> List[Dict[str, Any]]:
        return list(self.db.suppliers.find({}, {'_id': 0}))

    def save_chat_message(self, session_id: str, role: str, content: str) -> bool:
        try:
            self.db.chat_history.insert_one({
                'session_id': session_id,
                'role': role,
                'content': content,
                'timestamp': datetime.now()
            })
            return True
        except Exception as e:
            print(f"Error saving chat message: {e}")
            return False

    def get_chat_history(self, session_id: str) -> List[Dict[str, Any]]:
        return list(self.db.chat_history.find(
            {'session_id': session_id},
            {'_id': 0}
        ).sort('timestamp', 1))

    def contact_supplier_and_update_stock(self, item_name: str, quantity: int) -> Dict[str, Any]:
        try:
            # Get item details
            item = self.get_stock_level(item_name)
            if not item:
                return {"success": False, "message": "Item not found"}
                
            # Get supplier details
            supplier = self.get_supplier_for_item(item["item_id"])
            if not supplier:
                return {"success": False, "message": "Supplier not found"}
            
            # Update stock level
            new_stock = item["stock_level"] + quantity
            self.db.inventory.update_one(
                {"item_id": item["item_id"]},
                {"$set": {"stock_level": new_stock}}
            )
            
            return {
                "success": True,
                "supplier_name": supplier["supplier_name"],
                "contact_info": supplier["contact_info"],
                "item_name": item["item_name"],
                "quantity_ordered": quantity,
                "new_stock_level": new_stock,
                "message": "Supplier contacted and stock updated successfully"
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}

    def execute_query(self, collection: str, operation: str, query: Dict[str, Any]) -> Any:
        try:
            coll = self.db[collection]
            if operation == "find":
                return list(coll.find(query,{"_id": 0}))
            elif operation == "update":
                return coll.update_one(query.get("filter", {}), query.get("update", {}))
            elif operation == "insert":
                return coll.insert_one(query)
            elif operation == "aggregate":
                return list(coll.aggregate(query))
            else:
                raise ValueError(f"Unsupported operation: {operation}")
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    def get_collection_schema(self) -> Dict[str, Any]:
        """Get schema information for all collections"""
        schema = {}
        try:
            for collection_name in self.db.list_collection_names():
                # Get a sample document from each collection
                sample = self.db[collection_name].find_one()
                if sample:
                    # Remove _id and convert to schema structure
                    sample.pop('_id', None)
                    schema[collection_name] = {
                        'fields': list(sample.keys()),
                        'sample': sample,
                        'total_documents': self.db[collection_name].count_documents({})
                    }
            return schema
        except Exception as e:
            print(f"Error getting schema: {e}")
            return {}
