import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Between the Lines",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Between the Lines")
st.write("Testing filters only — no charts yet.")

df = pd.read_csv("clean_goodreads_books.csv")

numeric_columns = [
    "average_rating",
    "rating_count",
    "review_count",
    "number_of_pages",
    "publication_year"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df["title"] = df["title"].fillna("Unknown Title")
df["author"] = df["author"].fillna("Unknown Author")
df["genres"] = df["genres"].fillna("Unknown")

st.sidebar.title("Filters")

category_options = sorted(
    df["book_category"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "Book Categories",
    options=category_options,
    default=category_options
)

filtered_df = df[
    df["book_category"].isin(selected_categories)
]

st.success("App loaded successfully.")

st.write("Original dataset shape:", df.shape)
st.write("Filtered dataset shape:", filtered_df.shape)

st.subheader("Preview")

st.dataframe(
    filtered_df[
        [
            "title",
            "author",
            "average_rating",
            "rating_count",
            "genres",
            "publication_year",
            "book_category"
        ]
    ].head(50),
    use_container_width=True
)
