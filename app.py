import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Goodreads Test",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Goodreads App Test")

file_path = "clean_goodreads_books.csv"

st.write("Checking files...")

st.write("Current files in repo:")
st.write(os.listdir())

if not os.path.exists(file_path):
    st.error("CSV file was not found.")
    st.stop()

st.write("CSV file found.")

file_size = os.path.getsize(file_path)
st.write("CSV file size:", file_size)

df = pd.read_csv(file_path)

st.success("CSV loaded successfully!")

st.write("Dataset shape:")
st.write(df.shape)

st.write("Columns:")
st.write(df.columns.tolist())

st.write("Preview:")
st.dataframe(df.head())
