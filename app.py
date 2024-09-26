from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from streamlit_chat import message

import langchain
langchain.verbose = False

load_dotenv()

# Process text from PDF
def process_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    chunks = text_splitter.split_text(text)
    # Convert the chunks into embeddings to form a knowledge base
    try:
        with st.spinner("Generating embeddings..."):
            embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))
            know_base = FAISS.from_texts(chunks, embeddings)
        st.success('Embeddings are created successfully!')
    except Exception as e:
        st.error(f"Error generating embeddings: {str(e)}")
        return None

    return know_base

def display_conversation(history):
    for i in range(len(history["generated"])):
        message(history["past"][i], is_user=True, key=str(i) + "_user")
        message(history["generated"][i], key=str(i))

def main():
    st.title("Chat with your PDF")
    pdf = st.file_uploader("Upload a PDF", type="pdf")

    if pdf is not None:
        try:
            with st.spinner("Processing PDF..."):
                pdf_reader = PdfReader(pdf)
            st.success('PDF processed successfully!')
            
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
            return

        # Create a knowledge base object
        know_base = process_text(text)
        if know_base is None:
            return

        query = st.text_input("Ask me anything", key="input")

        cancel_btn = st.button("Cancel")
        if cancel_btn:
            st.stop()
        
        if query:
            try:
                with st.spinner("Searching for answers..."):
                    docs = know_base.similarity_search(query)

                    llm = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

                    chain = load_qa_chain(llm, chain_type='stuff')

                    with get_openai_callback() as cost:
                        res = chain.invoke(input={
                            'question': query,
                            'input_documents': docs,
                        })
                        print(cost)

                        if "generated" not in st.session_state:
                            st.session_state["generated"] = ["I am ready to help you"]
                        if "past" not in st.session_state:
                            st.session_state["past"] = ["Hey there!"]
                        
                        st.session_state["past"].append(query)
                        response = res['output_text']
                        st.session_state["generated"].append(response)

                        # Display conversation history using Streamlit messages
                        if st.session_state["generated"]:
                            display_conversation(st.session_state)

            except Exception as e:
                st.error(f"Error during query processing: {str(e)}")

if __name__ == '__main__':
    main()