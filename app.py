import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Between the Lines",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Between the Lines")
st.write("Goodreads Data Exploration Dashboard")

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

category_options = sorted(df["book_category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Book Categories",
    options=category_options,
    default=category_options
)

rating_range = st.sidebar.slider(
    "Average Rating",
    min_value=float(df["average_rating"].min()),
    max_value=float(df["average_rating"].max()),
    value=(
        float(df["average_rating"].min()),
        float(df["average_rating"].max())
    ),
    step=0.1
)

filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["book_category"].isin(selected_categories)
]

filtered_df = filtered_df[
    filtered_df["average_rating"].between(
        rating_range[0],
        rating_range[1]
    )
]

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Books", f"{len(filtered_df):,}")

with col2:
    st.metric("Average Rating", f"{filtered_df['average_rating'].mean():.2f}")

with col3:
    st.metric("Hidden Gems", f"{(filtered_df['book_category'] == 'Hidden Gem').sum():,}")

st.subheader("Book Categories")

category_counts = filtered_df["book_category"].value_counts()

st.bar_chart(category_counts)

st.subheader("Average Rating Distribution")

rating_counts = filtered_df["average_rating"].round(1).value_counts().sort_index()

st.bar_chart(rating_counts)

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
    ].head(100),
    use_container_width=True
)
