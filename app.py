import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import PyPDF2 as pdf
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text
def input_setup(uploaded_file): #converting pdf to text
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text
input_prompt= """You are extremely skilled Application Tracking System with a deep understanding of all the relevant technologies. Considering the highly competitive job market and the job description (jd), assign the percentage matching the description, the missing key words and profile summary. 
resume:{text}
description:{jd}
Generate response in one string:
{{
\n"Job Description Match": "XX%"\n 
\n "Missing Keywords"=""\n
\n "Profile Summary":""\n
 }}
 """
st.title("Smart Application Tracking System")
jd=st.text_area("Job Description: ")
uploaded_file=st.file_uploader("Upload your Resume", type="pdf", help="Please upload pdf")

submit=st.button("Submit")
if submit:
    if uploaded_file is not None:
        text=input_setup(uploaded_file)
        input_prompt = input_prompt.format(text=text, jd=jd)
        response1= get_response(input_prompt)
        f=response1.replace("{","").replace("}","")
        f=f.replace('"Job Description Match":', "**Job Description Match**:")
        
        f=f.replace('"Missing Keywords":', "**Missing Keywords**:")
        f=f.replace('"Profile Summary":', "**Profile Summary**:")
        f=f.replace('"','')
        
        st.subheader("Response: ")
        st.markdown(f)
        
