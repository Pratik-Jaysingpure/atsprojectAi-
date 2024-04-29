from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai
from docx import Document

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, content, prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def input_word_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the Word document
        doc = Document(uploaded_file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

        word_parts = [
            {
                "mime_type": "text/plain",
                "data": base64.b64encode(text.encode()).decode()  # encode to base64
            }
        ]
        return word_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF or Word)...", type=["pdf", "docx"])

if uploaded_file is not None:
    st.write("File Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")
submit4 = st.button("How to Make 100% Match")

input_prompt1 = """
You are an experienced Technical Human Resource Manager; your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First, the output should come as a percentage and then keywords missing, and last final thoughts.
"""

input_prompt4 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to create a prompt for an ATS (Applicant Tracking System) using Google data to achieve 100% match. 
Using the job description, write ATS-friendly keywords to get the resume shortlisted. 
Resume match and selection would involve specifying key criteria and skills. However, 
it's important to note that achieving a 100% match might not always be practical or desirable. 
Resumes are nuanced, and a holistic approach is often necessary. 
Here's a prompt that aims for high accuracy.
"""

if submit1:
    if uploaded_file is not None:
        if uploaded_file.type == 'application/pdf':
            content = input_pdf_setup(uploaded_file)
        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            content = input_word_setup(uploaded_file)
        else:
            st.write("Unsupported file format. Please upload a PDF or Word document.")
            st.stop()

        response = get_gemini_response(input_prompt1, content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        if uploaded_file.type == 'application/pdf':
            content = input_pdf_setup(uploaded_file)
        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            content = input_word_setup(uploaded_file)
        else:
            st.write("Unsupported file format. Please upload a PDF or Word document.")
            st.stop()

        response = get_gemini_response(input_prompt3, content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

if submit4:
    if uploaded_file is not None:
        if uploaded_file.type == 'application/pdf':
            content = input_pdf_setup(uploaded_file)
        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            content = input_word_setup(uploaded_file)
        else:
            st.write("Unsupported file format. Please upload a PDF or Word document.")
            st.stop()

        response = get_gemini_response(input_prompt4, content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")
