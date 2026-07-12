import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Between the Lines",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Between the Lines")
st.write("Testing filters with Matplotlib charts.")

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

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Books", f"{len(filtered_df):,}")

with col2:
    st.metric("Average Rating", f"{filtered_df['average_rating'].mean():.2f}")

with col3:
    st.metric(
        "Hidden Gems",
        f"{(filtered_df['book_category'] == 'Hidden Gem').sum():,}"
    )

st.subheader("Book Categories")

category_counts = filtered_df["book_category"].value_counts()

fig, ax = plt.subplots(figsize=(8, 4))
category_counts.plot(kind="bar", ax=ax)
ax.set_title("Books by Category")
ax.set_xlabel("Category")
ax.set_ylabel("Number of Books")
plt.xticks(rotation=30)
st.pyplot(fig)

st.subheader("Average Rating Distribution")

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(filtered_df["average_rating"].dropna(), bins=20, edgecolor="black")
ax.set_title("Distribution of Average Ratings")
ax.set_xlabel("Average Rating")
ax.set_ylabel("Number of Books")
st.pyplot(fig)

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
