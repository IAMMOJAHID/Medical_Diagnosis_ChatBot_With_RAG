from transformers import AutoTokenizer, pipeline, AutoModelForSeq2SeqLM
import torch

from langchain.chains import RetrievalQA
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from constants import CHROMA_SETTINGS

from langchain.llms  import HuggingFacePipeline

checkpoint="LaMini-T5-738M"
# checkpoint=None
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
base_model = AutoModelForSeq2SeqLM.from_pretrained(
    checkpoint,
    device_map="auto",
    torch_dtype=torch.float32
)



def llm_pipeline():
    pipe=pipeline(
        'text2text-generation',
        model=base_model,
        tokenizer=tokenizer,
        temperature=0.4, 
        max_length=256,
        do_sample=True,
        top_p=0.95
    )
    local_llm=HuggingFacePipeline(pipeline=pipe)
    return local_llm



def qa_llm():
    llm=llm_pipeline()
    embeddings=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db=Chroma(persist_directory="db", embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
    retriever=db.as_retriever()
    qa=RetrievalQA.from_chain_type(
      llm=llm, 
      chain_type="stuff",
      retriever=retriever,
      return_source_documents=True
    )
    return qa

def process_answer(instruction):
    response=''
    qa=qa_llm()
    generation=qa(instruction)
    answer=generation['result']
    return answer, generation


# if __name__ == "__main__":
#     instruction = "Thanks for this wonderful information!"  # replace this with your query
  
#     answer, generation = process_answer(instruction)
    
#     print("Answer:", answer)
#     print("_______________________________________________________")
#     print("query:", generation['query'])
#     print("_______________________________________________________")
#     print("result", generation["result"])
#     print("_______________________________________________________")
#     print("Source Document", generation['source_documents'])