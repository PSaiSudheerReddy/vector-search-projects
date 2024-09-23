import pymongo
import requests

client = pymongo.MongoClient("mongodb+srv://patilsaisudheer25:*****@cluster0.dfqo0hy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.sample_mflix
collection = db.movies

items= collection.find().limit(5)

#for item in items:
 # print(item)

hf_token = "*******"
embedding_url = 'https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2'

def generate_embedding(text: str) -> list[float]:
  response = requests.post(
    embedding_url,
    headers={"Authorization": f"Bearer {hf_token}"},
    json={"inputs": text})
  if response.status_code != 200:
    raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")
  return response.json()




query = "Comedy characters"

print(generate_embedding(query))

results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),
    "path": "plot_embedding_hf",
    "numCandidates": 100,
    "limit": 4,
    "index": "PotSemanticSearch",
      }}
]);

results_list = list(results)
print("size of list returned.." + str(len(results_list)))

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')
