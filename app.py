import streamlit as st
from langchain_community.llms import HuggingFaceHub
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from dotenv import load_dotenv
import os

load_dotenv()

Huggingface_api = os.getenv("Huggingface_api")

def generate_response(txt):
    # Instantiate the LLM model
    repo_id = "Falconsai/text_summarization"
    llm = HuggingFaceHub(repo_id=repo_id, huggingfacehub_api_token=Huggingface_api)
    # Split text
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(txt)
    # Create multiple documents
    docs = [Document(page_content=t) for t in texts]
    # Text summarization
    chain = load_summarize_chain(llm, chain_type='map_reduce')
    return chain.run(docs)

# Page title
st.set_page_config(page_title='🦜🔗 Text Summarization App')
st.title('🦜🔗 Text Summarization App')

# Text input
txt_input = st.text_area('Enter your text', '', height=200)

# Form to accept user's text input for summarization
result = []
with st.form('summarize_form', clear_on_submit=True):
    submitted = st.form_submit_button('Submit')
    if submitted:
        with st.spinner('Summarizing...'):
            response = generate_response(txt_input)
            result.append(response)
            
if len(result):
    st.info(response)