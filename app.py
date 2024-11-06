import streamlit as st
import pyttsx3
import json
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory,ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from openai import OpenAI
from playsound import playsound
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.chains import ConversationChain
from langchain_community.vectorstores import FAISS
from pypdf import PdfReader
import warnings 
from dotenv import load_dotenv
load_dotenv()
import os
warnings.simplefilter("ignore")

key = os.getenv('key')
print(key)
embed = OpenAIEmbeddings(api_key=key,show_progress_bar=True,skip_empty=True)

st.session_state.data = []
def main() :
    global db,chain,d2,data
    llm =  ChatOpenAI(api_key=key, model="gpt-4",max_tokens=500,temperature=0,top_p=1,stop_sequences='STOP', frequency_penalty=1,presence_penalty=1)
    memory =  ConversationBufferWindowMemory(k=5,memory_key="history")
    st.session_state.chain = ConversationChain(

        llm = llm,
        memory = memory
    )
    data = ''
    reader = PdfReader("Department1.pdf")
    number_of_pages = len(reader.pages)
    for i in range(number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        data+=text

    d1 = data.split("######")
    fp = open("info.json")
    d2 = json.load(fp)
    st.session_state.d2 = d2
    st.session_state.db = FAISS.from_texts(d1,embedding=embed)

    # llm =  ChatOpenAI(api_key=key, model="gpt-4",max_tokens=500,temperature=0,top_p=1,stop_sequences='STOP', frequency_penalty=1,presence_penalty=1)
    # stop sequence means it controls outputs 
    # frequency penalty reduces the repitation of idioms and phrases - Parameters =range(0 -2) ---  Higher penality less repitation
    # presence penality for generating the text balnces coherrent responsives 

    # memory = ConversationBufferWindowMemory(k=5)
    # chain = ConversationChain(

    #     llm = llm,
    #     memory = memory
    # )


q= ''
def prompt_template(q):
    st.session_state.data.append(st.session_state.db.similarity_search(q,k=1)[0].page_content)
    if len(st.session_state.data)>3:
        st.session_state.data.pop(0)
    print(st.session_state.data)
    data = st.session_state.data
    d2 = st.session_state.d2
    template = f'''You are representative of lux hospital as a conversational talk AI agent . Your task is to provide informative reponse for constomers basing on following details and provided data
    The follwoing doctors all works in Lux hospital and you are developed ashok a senior AI enginner at Advait labs 

    Hopital Details 
    Address : Plot No. 116, Lumbini Avenue, Gachibowli, Near IKEA, Hyderabad, 50081.
    Phone: 07969084444,
    Email: care@luxhospitals.com
    Website: www.luxhospitals.com

    Departments
    Proctology 
    Urology 
    General & Laproscopic Surgery
    General & Laproscopic Gynacology
    General & Laparoscopic Surgery

    provided data
    {data}

    Doctors with services in python dictionary items:
    {d2.items()}

    provided data
    {data}

    current conversation
    {{history}}
    Human
    {{input}}

    AI :

    ***THINGS TO REMEMBER ***
    - You dont book or schedule any appoitments if user asks provide hospital website 
    - Just gives info about about hospital and doctors 
    - Provide information of doctors when only used and related queries given 
    - If the AI does not know the answer to a question, it truthfully says it does not know
    - Finally, you have answer only our hospital and its medical services realated queries 
    - while Responpondig dont use special charecters
    - Response should be in less or equal to 20 words

    '''
    return template 
def response(query):
    # st.subheader("Here is your answer ")
    st.session_state.chain.prompt = PromptTemplate(template=prompt_template(query),input_variables=["input","history"])
    with st.spinner(text="Loading"):
        response = st.session_state.chain.invoke(query)
    
        if response :
            st.subheader("Here is your answer ")
            st.write(response["response"])
    # print(response["response"])

if  __name__ == "__main__" :
    print(st.session_state)
    with st.spinner("please wait :"):
        st.title("Welcome to Lux hospitals")
        if 'counter' not in st.session_state:
            st.session_state.counter = 100
            main()
st.subheader("Please enter your query  here :")
q  = st.text_area(placeholder="example who are you ",height = 100,label="here your query")


if st.button("Response"):
        with st.spinner("loading"):
            if q:
                response(q)
                del q
            else :
                st.warning("Please provide query ")
