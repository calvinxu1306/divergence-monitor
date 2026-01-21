import redis
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
r = redis.Redis(host='localhost', port=6379, db=0)

print("Worker listening...")
while True:
    # Pop text from the queue (blocking)
    _, item = r.brpop("text_queue")
    data = json.loads(item)
    
    # Vectorize
    vector = model.encode(data['text']).tolist()
    
    # Store in a new list for the API to read
    # In a full build, you'd push this to ChromaDB here
    result = {"source": data['source'], "vector": vector}
    r.lpush("processed_vectors", json.dumps(result))