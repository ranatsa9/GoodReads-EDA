
import html
import os
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Between the Lines",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# STYLE
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top right, rgba(199, 158, 91, 0.08), transparent 28%),
            linear-gradient(180deg, #15100d 0%, #1c1410 55%, #17110e 100%);
        color: #f3e7d3;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #100c0a 0%, #18110e 45%, #211612 100%);
        border-right: 1px solid #49352a;
    }

    [data-testid="stSidebar"] * {
        color: #efe1ca !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #d7b77d !important;
    }

    .hero-box {
        position: relative;
        overflow: hidden;
        background:
            radial-gradient(circle at 84% 18%, rgba(203, 165, 100, 0.15), transparent 28%),
            linear-gradient(135deg, #2a1d17 0%, #3b2920 48%, #241915 100%);
        border: 1px solid #5a4233;
        border-radius: 28px;
        padding: 3rem 3.2rem;
        margin-bottom: 1.8rem;
        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.34),
            inset 0 1px 0 rgba(255, 255, 255, 0.03);
    }

    .hero-decoration {
        position: absolute;
        right: 3rem;
        top: 1.4rem;
        font-size: 4.5rem;
        color: rgba(215, 183, 125, 0.13);
        pointer-events: none;
    }

    .hero-small {
        color: #d7b77d;
        font-size: 0.78rem;
        letter-spacing: 0.22rem;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 0.9rem;
    }

    .hero-title {
        color: #fff4df;
        font-size: 3.4rem;
        line-height: 1;
        font-weight: 800;
        margin-bottom: 1rem;
    }

    .hero-subtitle {
        max-width: 850px;
        color: #ddcab0;
        font-size: 1.08rem;
        line-height: 1.85;
    }

    .section-label {
        color: #c9a66b;
        font-size: 0.78rem;
        letter-spacing: 0.2rem;
        text-transform: uppercase;
        font-weight: 700;
        margin-top: 0.6rem;
        margin-bottom: 0.3rem;
    }

    .section-title {
        color: #fff0dc;
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 1.2rem;
    }

    .section-description {
        color: #cdbba4;
        line-height: 1.75;
        margin-bottom: 1.4rem;
        max-width: 900px;
    }

    [data-testid="stMetric"] {
        background:
            linear-gradient(180deg, #291e18 0%, #211713 100%);
        border: 1px solid #4b382d;
        border-radius: 18px;
        padding: 1.15rem;
        box-shadow: 0 9px 24px rgba(0, 0, 0, 0.22);
    }

    [data-testid="stMetricLabel"] {
        color: #c7aa7b !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricValue"] {
        color: #fff1dd !important;
    }

    .book-card,
    .featured-card {
        background:
            radial-gradient(circle at top right, rgba(210,169,95,0.08), transparent 30%),
            linear-gradient(180deg, #2b201a 0%, #211713 100%);
        border: 1px solid #4c382e;
        border-left: 5px solid #c6a060;
        border-radius: 16px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.2);
    }

    .featured-card {
        border-radius: 20px;
        padding: 1.6rem;
    }

    .book-title {
        color: #fff0db;
        font-size: 1.12rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .book-author {
        color: #bda98f;
        font-size: 0.91rem;
        margin-bottom: 0.75rem;
    }

    .book-meta {
        color: #deceb8;
        font-size: 0.9rem;
        line-height: 1.8;
    }

    .insight-box {
        background:
            linear-gradient(90deg, rgba(66, 48, 38, 0.96), rgba(42, 30, 24, 0.96));
        border: 1px solid #554034;
        border-left: 5px solid #c9a66b;
        border-radius: 14px;
        padding: 1.1rem 1.25rem;
        margin: 1rem 0 1.5rem 0;
        color: #e8dac5;
        line-height: 1.75;
    }

    .insight-title {
        color: #f3cc8a;
        font-weight: 800;
        margin-bottom: 0.35rem;
    }

    .badge {
        display: inline-block;
        padding: 0.3rem 0.72rem;
        border-radius: 999px;
        font-size: 0.73rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }

    .hidden-gem { background:#294033; color:#d8efdd; border:1px solid #3e5c47; }
    .overrated { background:#4a2822; color:#ffd8cc; border:1px solid #6b3c32; }
    .popular { background:#55471f; color:#f6e6aa; border:1px solid #746329; }
    .radar { background:#342d4a; color:#e1dcff; border:1px solid #4d446a; }
    .typical { background:#41342d; color:#ead9cc; border:1px solid #5b4940; }

    div[data-baseweb="select"] > div {
        background-color: #1c1512 !important;
        border-color: #49362c !important;
        color: #efe0ca !important;
    }

    input { color: #f3e6d3 !important; }

    .stButton button,
    .stDownloadButton button {
        background: linear-gradient(135deg, #6d4d34 0%, #967145 100%);
        color: #fff7e8 !important;
        border: 1px solid #aa8453;
        border-radius: 12px;
        font-weight: 700;
    }

    h1, h2, h3 { color: #fff0dc !important; }
    p, li { color: #ddcdb7; }
    hr { border-color: #49362d; }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    file_path = "clean_goodreads_books.csv"

    if not os.path.exists(file_path):
        st.error("CSV file was not found. Make sure clean_goodreads_books.csv is in the repository.")
        st.stop()

    data = pd.read_csv(file_path)

    numeric_columns = [
        "average_rating",
        "rating_count",
        "review_count",
        "number_of_pages",
        "publication_year"
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data["title"] = data["title"].fillna("Unknown Title")
    data["author"] = data["author"].fillna("Unknown Author")
    data["genres"] = data["genres"].fillna("Unknown")
    data["book_category"] = data["book_category"].fillna("Typical")

    return data


df = load_data()


# =========================================================
# HELPERS
# =========================================================

def render_html(code):
    st.markdown(code, unsafe_allow_html=True)


def format_number(number):
    if pd.isna(number):
        return "N/A"
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    if number >= 1_000:
        return f"{number / 1_000:.1f}K"
    return f"{number:,.0f}"


def category_badge(category):
    css_classes = {
        "Hidden Gem": "hidden-gem",
        "Overrated": "overrated",
        "Popular and Highly Rated": "popular",
        "Under the Radar": "radar",
        "Typical": "typical"
    }

    display_names = {
        "Overrated": "Overrated?",
        "Popular and Highly Rated": "Popular for a Reason"
    }

    css_class = css_classes.get(category, "typical")
    display_name = display_names.get(category, category)

    return f'<span class="badge {css_class}">{html.escape(str(display_name))}</span>'


def show_book_card(book, featured=False):
    safe_title = html.escape(str(book["title"]))
    safe_author = html.escape(str(book["author"]))
    safe_genres = html.escape(str(book["genres"]))

    extra_details = []

    if pd.notna(book["number_of_pages"]) and book["number_of_pages"] > 0:
        extra_details.append(f'📖 {int(book["number_of_pages"]):,} pages')

    if pd.notna(book["publication_year"]):
        extra_details.append(f'🗓️ {int(book["publication_year"])}')

    card_class = "featured-card" if featured else "book-card"
    extra_text = " &nbsp; · &nbsp; ".join(extra_details)

    card_html = (
        f'<div class="{card_class}">'
        f'<div class="book-title">{safe_title}</div>'
        f'<div class="book-author">by {safe_author}</div>'
        f'{category_badge(book["book_category"])}'
        '<div class="book-meta">'
        f'⭐ <strong>{book["average_rating"]:.2f}</strong>'
        f' &nbsp; · &nbsp; 👥 {format_number(book["rating_count"])} ratings'
        f' &nbsp; · &nbsp; 📝 {format_number(book["review_count"])} reviews'
        '<br>'
        f'📚 {safe_genres}'
    )

    if extra_text:
        card_html += f'<br>{extra_text}'

    card_html += '</div></div>'
    render_html(card_html)


def filter_by_genre(data, selected_genres):
    if not selected_genres:
        return data

    selected_lower = {str(genre).strip().lower() for genre in selected_genres}

    def has_selected_genre(value):
        book_genres = {genre.strip().lower() for genre in str(value).split(",")}
        return bool(book_genres & selected_lower)

    return data[data["genres"].apply(has_selected_genre)]


def style_plotly(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#211713",
        font=dict(color="#e8dac5"),
        title=dict(font=dict(color="#fff0dc", size=20)),
        xaxis=dict(gridcolor="rgba(201,166,107,0.12)", zeroline=False),
        yaxis=dict(gridcolor="rgba(201,166,107,0.12)", zeroline=False),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=40, r=30, t=70, b=40)
    )
    return fig


def get_daily_hidden_gem(data):
    hidden = data[data["book_category"] == "Hidden Gem"].copy()

    if hidden.empty:
        hidden = data.sort_values(
            by=["average_rating", "rating_count"],
            ascending=[False, False]
        ).head(100)

    seed = int(date.today().strftime("%Y%m%d"))
    return hidden.sample(1, random_state=seed).iloc[0]


# =========================================================
# GENRES
# =========================================================

genre_counts = (
    df["genres"]
    .str.split(", ")
    .explode()
    .dropna()
    .value_counts()
)

all_genres = sorted(genre_counts[genre_counts >= 120].index)

genres_to_remove = {"LGBT"}

all_genres = [
    genre for genre in all_genres
    if genre not in genres_to_remove
]

genre_category_keywords = {
    "✨ Fantasy & Speculative": [
        "fantasy", "magic", "paranormal", "science fiction",
        "dystopia", "steampunk", "supernatural"
    ],
    "💘 Romance": [
        "romance", "love", "new adult"
    ],
    "🔍 Mystery & Thriller": [
        "mystery", "thriller", "crime", "suspense", "detective"
    ],
    "👻 Horror & Dark Fiction": [
        "horror", "gothic", "dark", "vampire", "ghost"
    ],
    "🌱 Young Readers": [
        "young adult", "childrens", "middle grade", "picture book"
    ],
    "🏛️ Classics & Literature": [
        "classic", "literature", "literary", "contemporary",
        "historical fiction", "poetry", "plays"
    ],
    "🧠 Nonfiction & Ideas": [
        "nonfiction", "biography", "memoir", "history",
        "philosophy", "psychology", "science", "politics",
        "religion", "business"
    ],
    "🎨 Lifestyle & Culture": [
        "art", "music", "travel", "food",
        "cookbook", "health", "self help"
    ]
}

genre_categories = {}

for category, keywords in genre_category_keywords.items():
    genre_categories[category] = sorted(
        [
            genre
            for genre in all_genres
            if any(keyword in str(genre).lower() for keyword in keywords)
        ]
    )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📚 Between the Lines")

st.sidebar.write(
    """
    A Goodreads data exploration project about **quality**,
    **popularity**, and books that deserve another look.
    """
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Dashboard Page",
    [
        "🏠 Home",
        "🏛️ Library Overview",
        "📊 Reading Patterns",
        "💎 Hidden Shelves",
        "🔍 Find Your Next Read",
        "⚖️ Compare Genres",
        "🏆 Hall of Fame",
        "🎲 Surprise Me",
        "📈 Reading Trends",
        "🤖 Predict Popularity",
        "🔎 Browse Books",
        "🕯️ Method"
    ]
)

st.sidebar.divider()
st.sidebar.subheader("🔎 Filter the Library")

selected_genre_category = st.sidebar.selectbox(
    "Library Section",
    ["All Books"] + list(genre_categories.keys())
)

if selected_genre_category == "All Books":
    available_genres = all_genres
else:
    available_genres = genre_categories[selected_genre_category]

selected_genres = st.sidebar.multiselect(
    "Specific Genres",
    options=available_genres,
    placeholder="Optional"
)

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


# =========================================================
# APPLY FILTERS
# =========================================================

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

if selected_genres:
    filtered_df = filter_by_genre(filtered_df, selected_genres)

if filtered_df.empty:
    st.warning("No books match this combination of filters.")
    st.stop()


# =========================================================
# HERO
# =========================================================

render_html(
    '<div class="hero-box">'
    '<div class="hero-decoration">✦</div>'
    '<div class="hero-small">A Goodreads Data Exploration Project</div>'
    '<div class="hero-title">Between the Lines</div>'
    '<div class="hero-subtitle">'
    'Explore how readers rate books, how popularity shapes perception, '
    'and which titles deserve more attention than they receive.'
    '</div>'
    '</div>'
)


# =========================================================
# MAIN METRICS
# =========================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("📚 Books", f"{len(filtered_df):,}")

with m2:
    st.metric("⭐ Average Rating", f"{filtered_df['average_rating'].mean():.2f}")

with m3:
    st.metric("👥 Total Ratings", format_number(filtered_df["rating_count"].sum()))

with m4:
    hidden_count = (filtered_df["book_category"] == "Hidden Gem").sum()
    st.metric("💎 Hidden Gems", f"{hidden_count:,}")

st.write("")


# =========================================================
# HOME
# =========================================================

if page == "🏠 Home":
    render_html(
        '<div class="section-label">Welcome</div>'
        '<div class="section-title">Your Goodreads Library at a Glance</div>'
        '<div class="section-description">'
        'This dashboard uses a historical Goodreads dataset to explore ratings, '
        'popularity, genres, and overlooked books.'
        '</div>'
    )

    st.markdown("### 📖 Today's Hidden Gem")
    show_book_card(get_daily_hidden_gem(filtered_df), featured=True)

    most_popular = filtered_df.loc[filtered_df["rating_count"].idxmax()]

    reliable = filtered_df[filtered_df["rating_count"] >= 500]
    highest_rated = reliable.sort_values(
        by=["average_rating", "rating_count"],
        ascending=[False, False]
    ).iloc[0]

    oldest_book = (
        filtered_df.dropna(subset=["publication_year"])
        .sort_values("publication_year")
        .iloc[0]
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("👑 Most Popular", most_popular["title"][:28])
        st.caption(f"{format_number(most_popular['rating_count'])} ratings")

    with c2:
        st.metric("⭐ Highest Rated", highest_rated["title"][:28])
        st.caption(f"{highest_rated['average_rating']:.2f} average rating")

    with c3:
        st.metric("📅 Oldest Book", oldest_book["title"][:28])
        st.caption(f"Published in {int(oldest_book['publication_year'])}")

    render_html(
        '<div class="insight-box">'
        '<div class="insight-title">Dataset note</div>'
        'The dataset was last updated several years ago, so these results '
        'should be viewed as a historical snapshot.'
        '</div>'
    )


# =========================================================
# LIBRARY OVERVIEW
# =========================================================

elif page == "🏛️ Library Overview":
    render_html(
        '<div class="section-label">The Collection</div>'
        '<div class="section-title">A Look Inside the Library</div>'
    )

    left, right = st.columns(2)

    with left:
        category_counts = (
            filtered_df["book_category"]
            .value_counts()
            .rename_axis("Category")
            .reset_index(name="Books")
        )

        fig = px.bar(
            category_counts,
            x="Books",
            y="Category",
            orientation="h",
            title="Books by Category"
        )
        fig.update_layout(yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(style_plotly(fig), use_container_width=True)

    with right:
        fig = px.histogram(
            filtered_df,
            x="average_rating",
            nbins=25,
            title="Distribution of Average Ratings",
            labels={"average_rating": "Average Rating"}
        )
        st.plotly_chart(style_plotly(fig), use_container_width=True)

    render_html(
        '<div class="insight-box">'
        '<div class="insight-title">What this tells us</div>'
        'Most books are rated close to four stars, while very low ratings are uncommon.'
        '</div>'
    )

    top_genres = (
        filtered_df["genres"]
        .str.split(", ")
        .explode()
        .value_counts()
        .head(12)
        .rename_axis("Genre")
        .reset_index(name="Books")
    )

    fig = px.bar(
        top_genres,
        x="Books",
        y="Genre",
        orientation="h",
        title="Most Common Genres"
    )
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(style_plotly(fig), use_container_width=True)


# =========================================================
# READING PATTERNS
# =========================================================

elif page == "📊 Reading Patterns":
    render_html(
        '<div class="section-label">Exploratory Data Analysis</div>'
        '<div class="section-title">Reading Patterns</div>'
    )

    scatter_df = filtered_df[filtered_df["rating_count"] > 0].copy()

    if len(scatter_df) > 3000:
        scatter_df = scatter_df.sample(3000, random_state=42)

    fig = px.scatter(
        scatter_df,
        x="rating_count",
        y="average_rating",
        hover_name="title",
        hover_data=["author", "book_category"],
        log_x=True,
        opacity=0.45,
        title="Popularity vs Average Rating",
        labels={
            "rating_count": "Number of Ratings",
            "average_rating": "Average Rating"
        }
    )
    st.plotly_chart(style_plotly(fig), use_container_width=True)

    render_html(
        '<div class="insight-box">'
        '<div class="insight-title">What this tells us</div>'
        'Popularity does not always mean a higher rating.'
        '</div>'
    )

    pages_df = filtered_df[
        filtered_df["number_of_pages"].between(1, 1500)
    ].copy()

    if len(pages_df) > 3000:
        pages_df = pages_df.sample(3000, random_state=42)

    fig = px.scatter(
        pages_df,
        x="number_of_pages",
        y="average_rating",
        hover_name="title",
        opacity=0.4,
        title="Book Length vs Average Rating",
        labels={
            "number_of_pages": "Number of Pages",
            "average_rating": "Average Rating"
        }
    )
    st.plotly_chart(style_plotly(fig), use_container_width=True)

    render_html(
        '<div class="insight-box">'
        '<div class="insight-title">What this tells us</div>'
        'Book length has only a weak relationship with average rating.'
        '</div>'
    )


# =========================================================
# HIDDEN SHELVES
# =========================================================

elif page == "💎 Hidden Shelves":
    render_html(
        '<div class="section-label">Book Discovery</div>'
        '<div class="section-title">Hidden Shelves</div>'
    )

    discovery_type = st.radio(
        "Choose discovery type",
        [
            "💎 Hidden Gems",
            "📢 Overrated?",
            "👑 Popular for a Reason"
        ],
        horizontal=True
    )

    mapping = {
        "💎 Hidden Gems": "Hidden Gem",
        "📢 Overrated?": "Overrated",
        "👑 Popular for a Reason": "Popular and Highly Rated"
    }

    selected_df = filtered_df[
        filtered_df["book_category"] == mapping[discovery_type]
    ].copy()

    if discovery_type == "💎 Hidden Gems":
        selected_df = selected_df.sort_values(
            by=["average_rating", "rating_count"],
            ascending=[False, False]
        )
    else:
        selected_df = selected_df.sort_values(
            by="rating_count",
            ascending=False
        )

    if selected_df.empty:
        st.info("No books match the current filters.")
    else:
        number_to_show = st.slider("Number of books to show", 5, 25, 10)

        for _, book in selected_df.head(number_to_show).iterrows():
            show_book_card(book)


# =========================================================
# FIND YOUR NEXT READ
# =========================================================

elif page == "🔍 Find Your Next Read":
    render_html(
        '<div class="section-label">Recommendation Explorer</div>'
        '<div class="section-title">Find Your Next Read</div>'
    )

    c1, c2 = st.columns(2)

    with c1:
        rec_genre = st.selectbox(
            "Choose a genre",
            options=["Any Genre"] + all_genres
        )

        min_rating = st.slider(
            "Minimum rating",
            0.0,
            5.0,
            4.0,
            0.1
        )

    with c2:
        min_year = st.slider(
            "Published after",
            int(valid_years.min()),
            int(valid_years.max()),
            max(int(valid_years.min()), 2000)
        )

        max_pages = st.slider(
            "Maximum pages",
            100,
            1500,
            600,
            50
        )

    recommendations = filtered_df[
        (filtered_df["average_rating"] >= min_rating)
        & (
            filtered_df["publication_year"].isna()
            | (filtered_df["publication_year"] >= min_year)
        )
        & (
            filtered_df["number_of_pages"].isna()
            | (filtered_df["number_of_pages"] <= max_pages)
        )
    ].copy()

    if rec_genre != "Any Genre":
        recommendations = filter_by_genre(
            recommendations,
            [rec_genre]
        )

    recommendations = recommendations.sort_values(
        by=["average_rating", "rating_count"],
        ascending=[False, False]
    )

    if recommendations.empty:
        st.info("No recommendations match those choices.")
    else:
        st.success(f"Found {len(recommendations):,} matching books.")

        for _, book in recommendations.head(8).iterrows():
            show_book_card(book)


# =========================================================
# COMPARE GENRES
# =========================================================

elif page == "⚖️ Compare Genres":
    render_html(
        '<div class="section-label">Interactive Comparison</div>'
        '<div class="section-title">Compare Two Genres</div>'
    )

    c1, c2 = st.columns(2)

    with c1:
        genre_one = st.selectbox("First genre", all_genres, index=0)

    with c2:
        genre_two = st.selectbox(
            "Second genre",
            all_genres,
            index=1 if len(all_genres) > 1 else 0
        )

    rows = []

    for genre in [genre_one, genre_two]:
        subset = filter_by_genre(filtered_df, [genre])

        rows.append({
            "Genre": genre,
            "Books": len(subset),
            "Average Rating": subset["average_rating"].mean(),
            "Average Pages": subset["number_of_pages"].mean(),
            "Average Reviews": subset["review_count"].mean()
        })

    comparison_df = pd.DataFrame(rows)

    st.dataframe(
        comparison_df.round(2),
        use_container_width=True,
        hide_index=True
    )

    measure = st.selectbox(
        "Choose a measure",
        ["Average Rating", "Average Pages", "Average Reviews"]
    )

    fig = px.bar(
        comparison_df,
        x="Genre",
        y=measure,
        title=f"{measure}: {genre_one} vs {genre_two}"
    )
    st.plotly_chart(style_plotly(fig), use_container_width=True)


# =========================================================
# HALL OF FAME
# =========================================================

elif page == "🏆 Hall of Fame":
    render_html(
        '<div class="section-label">Standout Books</div>'
        '<div class="section-title">Hall of Fame</div>'
    )

    reliable = filtered_df[filtered_df["rating_count"] >= 500]

    hidden_candidates = filtered_df[
        filtered_df["book_category"] == "Hidden Gem"
    ]

    hall_books = {
        "👑 Most Popular": filtered_df.loc[
            filtered_df["rating_count"].idxmax()
        ],
        "⭐ Highest Rated": reliable.sort_values(
            ["average_rating", "rating_count"],
            ascending=[False, False]
        ).iloc[0],
        "📖 Longest Book": filtered_df.dropna(
            subset=["number_of_pages"]
        ).sort_values(
            "number_of_pages",
            ascending=False
        ).iloc[0],
        "📅 Oldest Book": filtered_df.dropna(
            subset=["publication_year"]
        ).sort_values(
            "publication_year"
        ).iloc[0]
    }

    if not hidden_candidates.empty:
        hall_books["💎 Best Hidden Gem"] = hidden_candidates.sort_values(
            ["average_rating", "rating_count"],
            ascending=[False, False]
        ).iloc[0]

    for label, book in hall_books.items():
        st.markdown(f"### {label}")
        show_book_card(book)


# =========================================================
# SURPRISE ME
# =========================================================

elif page == "🎲 Surprise Me":
    render_html(
        '<div class="section-label">Random Discovery</div>'
        '<div class="section-title">Surprise Me</div>'
    )

    if "surprise_index" not in st.session_state:
        st.session_state["surprise_index"] = 0

    if st.button("🎲 Pick Another Book"):
        st.session_state["surprise_index"] += 1

    surprise_book = filtered_df.sample(
        1,
        random_state=st.session_state["surprise_index"] + 42
    ).iloc[0]

    show_book_card(surprise_book, featured=True)


# =========================================================
# READING TRENDS
# =========================================================

elif page == "📈 Reading Trends":
    render_html(
        '<div class="section-label">Historical View</div>'
        '<div class="section-title">Books by Publication Year</div>'
        '<div class="section-description">'
        'This chart shows the historical distribution of books in the dataset.'
        '</div>'
    )

    trends_df = filtered_df.dropna(
        subset=["publication_year"]
    ).copy()

    trends_df = trends_df[
        trends_df["publication_year"].between(1800, valid_years.max())
    ]

    yearly_counts = (
        trends_df.groupby("publication_year")
        .size()
        .reset_index(name="Books")
    )

    fig = px.line(
        yearly_counts,
        x="publication_year",
        y="Books",
        title="Number of Books by Publication Year",
        labels={"publication_year": "Publication Year"}
    )
    st.plotly_chart(style_plotly(fig), use_container_width=True)

    render_html(
        '<div class="insight-box">'
        '<div class="insight-title">Important limitation</div>'
        'This chart reflects books included in the dataset, not all books '
        'published worldwide.'
        '</div>'
    )


# =========================================================
# MODEL PAGE
# =========================================================

elif page == "🤖 Predict Popularity":
    render_html(
        '<div class="section-label">Optional Machine Learning</div>'
        '<div class="section-title">Predicting Book Popularity</div>'
    )

    st.metric("Model Accuracy", "89.1%")

    st.markdown(
        """
The Logistic Regression model used:

- Average rating
- Review count
- Number of pages
- Publication year
        """
    )

    render_html(
        '<div class="insight-box">'
        '<div class="insight-title">Model result</div>'
        'The model achieved 89.1% accuracy, meaning it correctly classified '
        'most books as popular or not popular.'
        '</div>'
    )


# =========================================================
# BROWSE
# =========================================================

elif page == "🔎 Browse Books":
    render_html(
        '<div class="section-label">Search the Collection</div>'
        '<div class="section-title">Browse Books</div>'
    )

    search_term = st.text_input(
        "Search by title or author",
        placeholder="Search the shelves..."
    )

    browse_df = filtered_df.copy()

    if search_term:
        browse_df = browse_df[
            browse_df["title"].str.contains(
                search_term,
                case=False,
                na=False
            )
            |
            browse_df["author"].str.contains(
                search_term,
                case=False,
                na=False
            )
        ]

    sort_option = st.selectbox(
        "Sort books by",
        [
            "Average Rating",
            "Rating Count",
            "Review Count",
            "Publication Year"
        ]
    )

    sort_mapping = {
        "Average Rating": "average_rating",
        "Rating Count": "rating_count",
        "Review Count": "review_count",
        "Publication Year": "publication_year"
    }

    browse_df = browse_df.sort_values(
        by=sort_mapping[sort_option],
        ascending=False
    )

    if search_term and not browse_df.empty:
        st.markdown("### Best Match")
        show_book_card(browse_df.iloc[0], featured=True)

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
        browse_df[display_columns].head(500),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇️ Download Filtered Collection",
        data=browse_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_goodreads_books.csv",
        mime="text/csv"
    )


# =========================================================
# METHOD
# =========================================================

elif page == "🕯️ Method":
    render_html(
        '<div class="section-label">Behind the Dashboard</div>'
        '<div class="section-title">The Method</div>'
    )

    high_rating = df["average_rating"].quantile(0.75)
    low_rating = df["average_rating"].quantile(0.25)
    minimum_popularity = df["rating_count"].quantile(0.25)
    median_popularity = df["rating_count"].median()
    high_popularity = df["rating_count"].quantile(0.75)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("⭐ High Rating", f"{high_rating:.2f}+")

    with c2:
        st.metric(
            "👥 Minimum Evidence",
            f"{minimum_popularity:,.0f} ratings"
        )

    with c3:
        st.metric(
            "📚 High Popularity",
            f"{high_popularity:,.0f}+ ratings"
        )

    st.markdown(
        f"""
### 💎 Hidden Gem
- Rating of **{high_rating:.2f} or higher**
- At least **{minimum_popularity:,.0f} ratings**
- Fewer than **{median_popularity:,.0f} ratings**

### 👑 Popular for a Reason
- Rating of **{high_rating:.2f} or higher**
- At least **{median_popularity:,.0f} ratings**

### 📢 Overrated?
- Rating of **{low_rating:.2f} or lower**
- At least **{high_popularity:,.0f} ratings**

### 🌙 Under the Radar
- Fewer than **{minimum_popularity:,.0f} ratings**

### 📚 Typical
- Books that do not fit the categories above
        """
    )

    st.markdown("### Dataset Limitation")

    st.write(
        "The dataset was last updated several years ago, so the results "
        "should be viewed as a historical snapshot of Goodreads data."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

render_html(
    '<div style="text-align:center;color:#9f8b74;font-size:0.85rem;'
    'padding:1.5rem;letter-spacing:0.04rem;">'
    '🕯️ Between the Lines<br>Goodreads Data Exploration Project'
    '</div>'
)
