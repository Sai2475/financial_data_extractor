from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def extract(article_text, custom_api_key=None):
    # Resolve API Key
    api_key = custom_api_key if custom_api_key and custom_api_key.strip() else None
    
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")
        
    if not api_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]

    if not api_key:
        raise ValueError(
            "Groq API Key not found! Please enter your API key in the sidebar or set 'GROQ_API_KEY' in Streamlit secrets / .env file."
        )

    llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)

    prompt = '''
    From the below news article, extract revenue and eps in JSON format containing the
    following keys: 'revenue_actual', 'revenue_expected', 'eps_actual', 'eps_expected'. 

    Each value should have a unit such as million or billion.

    Only return the valid JSON. No preamble.

    Article
    =======
    {article}
    '''

    pt = PromptTemplate.from_template(prompt)

    chain = pt | llm
    response = chain.invoke({'article': article_text})
    parser = JsonOutputParser()

    try:
        res = parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context too big. Unable to parse jobs.")

    return res