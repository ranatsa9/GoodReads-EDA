import os
import html
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


st.set_page_config(
    page_title="Between the Lines",
    page_icon="📚",
    layout="wide"
)


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #15100d 0%, #211713 100%);
        color: #f3e7d3;
    }

    .block-container {
        max-width: 1300px;
        padding-top: 2rem;
    }

    [data-testid="stSidebar"] {
        background-color: #100c0a;
    }

    [data-testid="stSidebar"] * {
        color: #efe1ca !important;
    }

    .hero {
        background: linear-gradient(135deg, #2a1d17, #3b2920);
        border: 1px solid #5a4233;
        border-radius: 24px;
        padding: 2.5rem;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        color: #fff4df;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .hero p {
        color: #ddcab0;
        font-size: 1.05rem;
        line-height: 1.7;
    }

    h1, h2, h3 {
        color: #fff0dc !important;
    }

    p, li {
        color: #ddcdb7;
    }

    [data-testid="stMetric"] {
        background: #291e18;
        border: 1px solid #4b382d;
        border-radius: 16px;
        padding: 1rem;
    }

    .book-card {
        background: #2b201a;
        border: 1px solid #4c382e;
        border-left: 5px solid #c6a060;
        border-radius: 15px;
        padding: 1rem 1.2rem;
        margin-bottom: 1rem;
    }

    .book-title {
        color: #fff0db;
        font-weight: 800;
        font-size: 1.1rem;
    }

    .book-author {
        color: #bda98f;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }

    .book-meta {
        color: #deceb8;
        font-size: 0.9rem;
        line-height: 1.7;
    }

    .badge {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: #294033;
        color: #d8efdd;
        border: 1px solid #3e5c47;
    }

    hr {
        border-color: #49362d;
    }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def load_data():
    file_path = "clean_goodreads_books.csv"

    if not os.path.exists(file_path):
        st.error("clean_goodreads_books.csv was not found.")
        st.stop()

    df = pd.read_csv(file_path)

    numeric_columns = [
        "average_rating",
        "rating_count",
        "review_count",
        "number_of_pages",
        "publication_year"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["title"] = df["title"].fillna("Unknown Title")
    df["author"] = df["author"].fillna("Unknown Author")
    df["genres"] = df["genres"].fillna("Unknown")

    return df


df = load_data()


def format_number(number):
    if pd.isna(number):
        return "N/A"
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    if number >= 1_000:
        return f"{number / 1_000:.1f}K"
    return f"{number:,.0f}"


def make_chart_dark(fig, ax):
    fig.patch.set_facecolor("#211713")
    ax.set_facecolor("#211713")

    ax.title.set_color("#fff0dc")
    ax.xaxis.label.set_color("#e8dac5")
    ax.yaxis.label.set_color("#e8dac5")

    ax.tick_params(axis="x", colors="#e8dac5")
    ax.tick_params(axis="y", colors="#e8dac5")

    for spine in ax.spines.values():
        spine.set_color("#5a4233")

    ax.grid(True, alpha=0.15)

    return fig


def show_book_card(book):
    title = html.escape(str(book["title"]))
    author = html.escape(str(book["author"]))
    genres = html.escape(str(book["genres"]))

    page_text = ""
    if pd.notna(book["number_of_pages"]) and book["number_of_pages"] > 0:
        page_text = f" · 📖 {int(book['number_of_pages']):,} pages"

    year_text = ""
    if pd.notna(book["publication_year"]):
        year_text = f" · 🗓️ {int(book['publication_year'])}"

    st.markdown(
        f"""
        <div class="book-card">
            <div class="book-title">{title}</div>
            <div class="book-author">by {author}</div>
            <span class="badge">Hidden Gem</span>
            <div class="book-meta">
                ⭐ <strong>{book["average_rating"]:.2f}</strong>
                · 👥 {format_number(book["rating_count"])} ratings
                · 📝 {format_number(book["review_count"])} reviews
                <br>
                📚 {genres}
                {page_text}
                {year_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.sidebar.title("📚 Filters")

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

valid_years = df["publication_year"].dropna()

year_range = st.sidebar.slider(
    "Publication Year",
    min_value=int(valid_years.min()),
    max_value=int(valid_years.max()),
    value=(
        int(valid_years.min()),
        int(valid_years.max())
    )
)

search_term = st.sidebar.text_input(
    "Search title or author"
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

filtered_df = filtered_df[
    filtered_df["publication_year"].isna()
    |
    filtered_df["publication_year"].between(
        year_range[0],
        year_range[1]
    )
]

if search_term:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search_term, case=False, na=False)
        |
        filtered_df["author"].str.contains(search_term, case=False, na=False)
    ]


if filtered_df.empty:
    st.warning("No books match these filters.")
    st.stop()


st.markdown(
    """
    <div class="hero">
        <h1>📚 Between the Lines</h1>
        <p>
        A Goodreads data exploration dashboard about book quality,
        popularity, genres, and hidden gems.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Books", f"{len(filtered_df):,}")

with col2:
    st.metric("Average Rating", f"{filtered_df['average_rating'].mean():.2f}")

with col3:
    st.metric("Total Ratings", format_number(filtered_df["rating_count"].sum()))

with col4:
    hidden_count = (
        filtered_df["book_category"] == "Hidden Gem"
    ).sum()
    st.metric("Hidden Gems", f"{hidden_count:,}")


st.divider()


st.header("📊 Library Overview")

left_col, right_col = st.columns(2)

with left_col:
    category_counts = filtered_df["book_category"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))
    category_counts.sort_values().plot(kind="barh", ax=ax)

    ax.set_title("Books by Category")
    ax.set_xlabel("Number of Books")
    ax.set_ylabel("Category")

    fig = make_chart_dark(fig, ax)
    st.pyplot(fig)
    plt.close(fig)

with right_col:
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        filtered_df["average_rating"].dropna(),
        bins=25,
        edgecolor="#15100d"
    )

    ax.set_title("Distribution of Average Ratings")
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Number of Books")

    fig = make_chart_dark(fig, ax)
    st.pyplot(fig)
    plt.close(fig)


st.markdown(
    """
    Most books in the dataset have average ratings close to four stars.
    This shows that Goodreads ratings are generally concentrated in a high range.
    """
)


st.divider()


st.header("📚 Genre Analysis")

top_genres = (
    filtered_df["genres"]
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)

fig, ax = plt.subplots(figsize=(10, 5))
top_genres.sort_values().plot(kind="barh", ax=ax)

ax.set_title("Top 10 Most Common Genres")
ax.set_xlabel("Number of Books")
ax.set_ylabel("Genre")

fig = make_chart_dark(fig, ax)
st.pyplot(fig)
plt.close(fig)


st.divider()


st.header("📈 Popularity vs Rating")

scatter_df = filtered_df[
    filtered_df["rating_count"] > 0
].copy()

if len(scatter_df) > 3000:
    scatter_df = scatter_df.sample(3000, random_state=42)

fig, ax = plt.subplots(figsize=(10, 5))

ax.scatter(
    scatter_df["rating_count"].apply(lambda x: pd.NA if x <= 0 else x),
    scatter_df["average_rating"],
    alpha=0.3
)

ax.set_xscale("log")
ax.set_title("Popularity vs Average Rating")
ax.set_xlabel("Rating Count")
ax.set_ylabel("Average Rating")

fig = make_chart_dark(fig, ax)
st.pyplot(fig)
plt.close(fig)

st.markdown(
    """
    Popularity does not always mean a book has a higher rating.
    Some less popular books still receive very strong reader ratings.
    """
)


st.divider()


st.header("💎 Hidden Gems")

hidden_df = (
    filtered_df[
        filtered_df["book_category"] == "Hidden Gem"
    ]
    .sort_values(
        by=["average_rating", "rating_count"],
        ascending=[False, False]
    )
)

if hidden_df.empty:
    st.info("No hidden gems match the current filters.")
else:
    count_to_show = st.slider(
        "Number of hidden gems to show",
        5,
        20,
        10
    )

    for _, book in hidden_df.head(count_to_show).iterrows():
        show_book_card(book)


st.divider()


st.header("🔎 Browse Books")

display_columns = [
    "title",
    "author",
    "average_rating",
    "rating_count",
    "review_count",
    "genres",
    "publication_year",
    "book_category"
]

st.dataframe(
    filtered_df[display_columns].head(500),
    use_container_width=True,
    hide_index=True
)


csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download Filtered Data",
    data=csv_data,
    file_name="filtered_goodreads_books.csv",
    mime="text/csv"
)


st.divider()

st.header("🕯️ Method")

st.markdown(
    """
    Books were classified using data-based thresholds from the cleaned dataset.

    - **Hidden Gem:** highly rated books with moderate popularity.
    - **Popular and Highly Rated:** books with both high ratings and high popularity.
    - **Overrated:** highly popular books with lower ratings.
    - **Under the Radar:** books with very low rating counts.
    - **Typical:** books that do not fall into the other groups.

    The cleaned dataset contains 49,351 books after removing rows without genre
    information and books with zero ratings.
    """
)
