import os
import faiss
import numpy as np
import pandas as pd
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate


os.environ["GOOGLE_API_KEY"] = "AIzaSyBmtamOc6vgzcAdG3mGH4R"


model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5)
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


def load_excel_data(uploaded_file):
    df = pd.read_excel(uploaded_file)
    records = []

    for _, row in df.iterrows():
        row_dict = row.to_dict()
        formatted_text = ", ".join([f"{col}: {val}" for col, val in row_dict.items()])
        records.append(formatted_text)

    return df, records

def create_faiss_index(records):
    embeddings = [embedding_model.embed_query(text) for text in records]
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))
    return index, records


def find_similar_case(query, index, records):
    query_vector = np.array([embedding_model.embed_query(query)]).astype("float32")
    distances, indices = index.search(query_vector, k=1)
    if indices[0][0] < len(records):
        return records[indices[0][0]]
    else:
        return "No similar case found."


def generate_medical_response(symptoms, retrieved_case):
    prompt = PromptTemplate.from_template(
        """You are an expert medical assistant. 
        A patient has described their symptoms as follows:
        Symptoms: {symptoms}

        Based on a similar past case:
        {retrieved_case}

        Now provide a concise, structured response including:
        1. Possible Diagnosis
        2. Initial Treatment
        3. Follow-up Recommendations"""
    )
    final_prompt = prompt.format(symptoms=symptoms, retrieved_case=retrieved_case)
    response = model.invoke(final_prompt)
    return response.content


st.title("💊 AI-Powered Medical Diagnosis Assistant")
st.write("Upload an Excel file with patient data and enter symptoms to find similar cases.")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    df, patient_records = load_excel_data(uploaded_file)
    faiss_index, processed_data = create_faiss_index(patient_records)

    st.success("✅ Excel file processed successfully! Now enter symptoms below.")
    user_input = st.text_area("Describe your symptoms:")

    if st.button("Find Diagnosis & Treatment"):
        if user_input.strip():
            with st.spinner("Analyzing and generating response..."):
                similar_case = find_similar_case(user_input, faiss_index, patient_records)
                final_response = generate_medical_response(user_input, similar_case)

            st.subheader("🔍 Closest Matching Case")
            st.write(similar_case)

            st.subheader("💡 AI-Generated Medical Advice")
            st.write(final_response)
        else:
            st.warning("⚠️ Please enter symptoms before searching.")
