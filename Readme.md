#### PDF info Extraction using OpenAI and Streamlit ###




##  Overview of Project ##
--------------------------
This Streamlit application allows users to upload a PDF file, process it 
using OpenAI embeddings, store the data in a PostgreSQL database, and perform
queries to extract relevant information from the uploaded document.
--------------------------







## Features ##
----------------------------------
1. required openai api key(add OPENAI_API_KEY in .env file)
1. Upload a PDF file(you can upload pdf file one time only)
2. Extract text and store it in a PostgreSQL database
3. Use OpenAI embeddings to create vector representations of the text
4. Perform similarity-based queries to retrieve relevant information
5. Extract precise answers using OpenAI's gpt-4o-mini model
----------------------------------






###   Requirements  ###
----------------------------
Python
PostgreSQL database with pgvector extension
OpenAI API key
Streamlit
LangChain
PyPDFLoader
----------------------------



## Installation ##
----------------------------
1. Clone this repository:
    git@github.com:sunil-kumar987654433/bluebash-pdf-info-extraction.git

2. Install required dependencies:
    pip install -r requirements.txt


3. Set up your PostgreSQL database with pgvector and create a table:
   
   CREATE EXTENSION IF NOT EXISTS vector;

    CREATE TABLE items (
        id number PRIMARY KEY,
        content TEXT,
        embeding VECTOR
    );


4. Run the Streamlit app:
  streamlit run app.py
----------------------------




###   Usage    ###
----------------------------
1. Enter your OpenAI API key in the sidebar and upload it.
2. Upload a PDF file, which will be processed and stored in the database.
3. Enter a query to search for relevant information from the document.
4. The app will extract the most relevant text and use GPT-4o-mini to provide an answer.
----------------------------



###  Troubleshooting  ###
----------------------------
1. Ensure the OpenAI API key is valid.
2. Confirm that PostgreSQL is running and the table is created correctly.
3. Ensure the pgvector extension is installed and enabled in PostgreSQL.
4. Check that all dependencies are installed.
----------------------------



