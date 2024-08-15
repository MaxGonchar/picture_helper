from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(hosts=["http://localhost:9200"])

# Index a document
res = es.index(index="my-index", id=1, body={"title": "Test document"})
print(res)
