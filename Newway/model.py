from transformers import pipeline
from elasticsearch import Elasticsearch
import streamlit as st
# from contents import es

# Load the QA (Question Answering) pipeline with the BERT model
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

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
es.indices.create(_index=index_name, _body=mapping)

# Sample medical documents
medical_documents = [
    {"title": "Fever", "content": "Fever is often accompanied by symptoms such as chills, sweating, fatigue, and muscle aches."},
    {"title": "Headache", "content": "Common causes of headaches include stress, muscle tension, dehydration, lack of sleep, and certain medical conditions."},
    {"title": "Manali", "content": "Manali is a picturesque town located in the Indian state of Himachal Pradesh, nestled in the foothills of the Himalayas."},

]

# Index each document into Elasticsearch
for i, doc in enumerate(medical_documents):
    es.index(index=index_name, id=i+1, body=doc)
    # print(f'This is doc_{i}',doc)


def medical_chatbot(query):
    # Retrieve relevant documents from Elasticsearch
    retrieved_documents = es.search(index="medical_documents", body={"query": {"match": {"content": query}}})
    
    # Extract context from retrieved documents
    context = [doc['_source']['content'] for doc in retrieved_documents['hits']['hits']]
    
    # Use the language model to answer the query based on context
    if context:
        answer = qa_pipeline(question=query, context=context)
        return answer['answer']
    else:
        return "Sorry, I couldn't find relevant information for your query."



st.title("Medical Chatbot")
st.write("Ask any medical-related question and get answers!")

# Input field for user query
query = st.text_input("Enter your question here:")

# Button to submit query
if st.button("Ask"):
    # Call the chatbot backend function
    response = medical_chatbot(query)
    st.write("Answer:", response)




# from transformers import GPT2LMHeadModel, GPT2Tokenizer

# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# model = GPT2LMHeadModel.from_pretrained("gpt2", pad_token_id=tokenizer.eos_token_id)

# def medical_chatbot(data):
    
#     user_input =data

#     # Generate response using the model
#     input_ids = tokenizer.encode(user_input, return_tensors='pt')
#     response_ids = model.generate(input_ids, max_length=500, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
#     response_text = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    
#     return response_text






