import chromadb
import os

# Connect to the database we just built
db_path = os.path.join(os.getcwd(), "data/chroma_db")
client = chromadb.PersistentClient(path=db_path)
collection = client.get_collection(name="robot_failures")

# Simulate a user question
query = "The lidar sensor is not working"

# Ask the database to find the top 2 matches
results = collection.query(
    query_texts=[query],
    n_results=2
)

print(f"\n🔍 Searching for: '{query}'")
for i in range(len(results['documents'][0])):
    print(f"\nMatch {i+1}:")
    print(f"📄 Log: {results['documents'][0][i]}")
    print(f"💡 Fix: {results['metadatas'][0][i]['fix']}")
