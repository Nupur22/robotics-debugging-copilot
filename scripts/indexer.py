import json
import chromadb
import os

# 1. Initialize the ChromaDB Client
# This finds the 'scripts' folder, then goes up one level to find 'data'
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(current_dir, "..", "data", "chroma_db"))
log_file = os.path.abspath(os.path.join(current_dir, "..", "data", "synthetic_logs.jsonl"))

client = chromadb.PersistentClient(path=db_path)

# 2. Create a collection ( like a table in a database)
# Using the default embedding model that comes with ChromaDB
collection = client.get_or_create_collection(name="robot_logs")

def index_logs():
    log_file = "data/synthetic_logs.jsonl"
    
    if not os.path.exists(log_file):
        print(f"Error: {log_file} not found! Run generator.py first.")
        return

    with open(log_file, 'r') as f:
        lines = f.readlines()

    documents = []
    metadatas = []
    ids = []

    for i, line in enumerate(lines):
        data = json.loads(line)
        # combine the node and the message so the AI can search both
        text_to_index = f"Node: {data['node']} | Error: {data['message']}"
        
        documents.append(text_to_index)
        # store the 'root_cause' in metadata so we can retrieve the answer later
        metadatas.append({"source": data['node'], "fix": data['metadata']['root_cause']})
        ids.append(f"log_{i}")

    # 3. Add data to the collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Successfully indexed {len(documents)} logs into ChromaDB at {db_path}")

if __name__ == "__main__":
    index_logs()
