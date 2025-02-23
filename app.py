import streamlit as st
import re
from db_connection import cur, conn
from langchain_openai import OpenAIEmbeddings, ChatOpenAI, OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

st.header("extract info from pdf file")
st.write("Developer: sunil.kumar987654433@gmail.com")
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "embeddings_model" not in st.session_state:
    st.session_state.embeddings_model = None
if "query_search_btn" not in st.session_state:
    st.session_state.query_search_btn = False
if "query_result" not in st.session_state:
    st.session_state.query_result = None
if "clear_table_btn" not in st.session_state:
    st.session_state.clear_table_btn = None

st.sidebar.header("API and File Upload")
api_key = st.sidebar.text_input("Enter Openai API token", type="password")


if st.sidebar.button("Upload API Token"):
    try:
        st.session_state.embeddings_model = OpenAIEmbeddings(api_key=api_key)
        st.session_state.api_key = api_key
        st.sidebar.success("API Token Uploaded!")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

st.divider()
upload_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])
col1, col2 = st.columns([1,1])
upload_file_btn = False
with col1:
    if st.sidebar.button("Upload File"):
        upload_file_btn = True

with col2:
    if st.sidebar.button("clear data from database"):
        st.session_state.clear_table_btn = True
    if st.session_state.clear_table_btn:
        cur.execute("delete from items")
        conn.commit()
        
if upload_file_btn and st.session_state.embeddings_model and upload_file:
    with open("temp.pdf", "wb") as f:
        f.write(upload_file.getbuffer())

    loader = PyPDFLoader("temp.pdf")
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=170)
    texts = text_splitter.split_documents(pages)

    doc_vector = st.session_state.embeddings_model.embed_documents([i.page_content for i in texts])

    try:
        for i in range(len(doc_vector)):
            content = texts[i].page_content
            embedding = doc_vector[i]
            cur.execute("INSERT INTO items(content, embeding) VALUES(%s, %s)", (content, embedding))
        conn.commit()
        st.sidebar.success("File uploaded and processed successfully!")
    except Exception as e:
        conn.rollback()
        st.sidebar.error(f"Database error: {e}")


if st.session_state.embeddings_model:
    cur.execute("SELECT id FROM items")
    records = cur.fetchall()
    st.write(f" Records found in database: {len(records)}")
    
    if len(records) > 0:

        query_input = st.text_input("Enter your query:", key="query_input_key")


        if st.button("Query Search"):
            st.session_state.query_search_btn = True

        if st.session_state.query_search_btn and query_input.strip():
            st.write("Processing query...")
            try:
                output = st.session_state.embeddings_model.embed_query(query_input)
                cur.execute("SELECT id, content FROM items ORDER BY embeding <-> %s::vector LIMIT 1", (output,))
                result = cur.fetchone()

                if result:
                    cleaned_text = re.sub(r'\s+', ' ', result[1].strip())
                    llm = ChatOpenAI(model_name="gpt-4o-mini", api_key=api_key)
                    prompt = [
                        ("system", "You are an AI that extracts only required information from text."),
                        ("user", f"Extract the answer from the following text:\n{cleaned_text}")
                    ]
                    prompt_template = ChatPromptTemplate(prompt)
                    
                    cleaned_text = prompt_template.format(user_query=cleaned_text)
                    
                    
                    chain = llm.invoke(cleaned_text)
                    st.session_state.query_result = chain.content
                    st.session_state.query_search_btn = False
                else:
                    st.session_state.query_result = "No matching records found."
            except Exception as e:
                st.session_state.query_result = f"error: {e}"

        if st.session_state.query_result:
            st.subheader("Extracted Information:")
            st.write(st.session_state.query_result)
    else:
        st.write("please upload the pdf file because database is empty")
else:
    st.error("Please enter first api token of openai")