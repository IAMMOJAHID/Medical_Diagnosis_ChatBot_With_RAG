from elasticsearch import Elasticsearch

host = "localhost"
port = 8503

# Initialize Elasticsearch client
# es = Elasticsearch([{"host": host, "port": port}])
es = Elasticsearch(" http://localhost:8501")

# Define index name and mapping
index_name = "medical_documents"
mapping = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "content": {"type": "text"}
        }
    }
}

# Create the index with the defined mapping
es.indices.create(index=index_name, body=mapping)

# Sample medical documents
medical_documents = [
    {"title": "Fever", "content": "Fever is often accompanied by symptoms such as chills, sweating, fatigue, and muscle aches."},
    {"title": "Headache", "content": "Common causes of headaches include stress, muscle tension, dehydration, lack of sleep, and certain medical conditions."},
    {"title": "Manali", "content": "Manali is a picturesque town located in the Indian state of Himachal Pradesh, nestled in the foothills of the Himalayas."},

]

# Index each document into Elasticsearch
for i, doc in enumerate(medical_documents):
    es.index(index=index_name, id=i+1, body=doc)
    print(f'This is doc_{i}',doc)