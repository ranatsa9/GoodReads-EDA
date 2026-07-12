import html
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Between the Lines",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM STYLE
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
        padding: 3.2rem 3.3rem;
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
        font-size: 3.5rem;
        line-height: 1;
        font-weight: 800;
        margin-bottom: 1rem;
    }

    .hero-subtitle {
        max-width: 820px;
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
        font-size: 2.15rem;
        font-weight: 800;
        margin-bottom: 1.2rem;
    }

    .section-description {
        color: #cdbba4;
        line-height: 1.75;
        margin-bottom: 1.4rem;
        max-width: 850px;
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

    .book-card {
        background:
            linear-gradient(180deg, #2b201a 0%, #211713 100%);
        border: 1px solid #4c382e;
        border-left: 5px solid #c6a060;
        border-radius: 16px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.2);
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

    .hidden-gem {
        background: #294033;
        color: #d8efdd;
        border: 1px solid #3e5c47;
    }

    .overrated {
        background: #4a2822;
        color: #ffd8cc;
        border: 1px solid #6b3c32;
    }

    .popular {
        background: #55471f;
        color: #f6e6aa;
        border: 1px solid #746329;
    }

    .radar {
        background: #342d4a;
        color: #e1dcff;
        border: 1px solid #4d446a;
    }

    .typical {
        background: #41342d;
        color: #ead9cc;
        border: 1px solid #5b4940;
    }

    button[data-baseweb="tab"] {
        color: #aa9781 !important;
        font-weight: 700;
        background: transparent !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #e1c18a !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #f1c982 !important;
        border-bottom: 2px solid #c9a66b !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #1c1512 !important;
        border-color: #49362c !important;
        color: #efe0ca !important;
    }

    input {
        color: #f3e6d3 !important;
    }

    .stButton button,
    .stDownloadButton button {
        background:
            linear-gradient(135deg, #6d4d34 0%, #967145 100%);
        color: #fff7e8 !important;
        border: 1px solid #aa8453;
        border-radius: 12px;
        font-weight: 700;
    }

    h1,
    h2,
    h3 {
        color: #fff0dc !important;
    }

    p,
    li {
        color: #ddcdb7;
    }

    hr {
        border-color: #49362d;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

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

    if os.path.getsize(file_path) == 0:
        st.error("CSV file exists but is empty. Re-upload the correct CSV file.")
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
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    data["title"] = data["title"].fillna("Unknown Title")
    data["author"] = data["author"].fillna("Unknown Author")
    data["genres"] = data["genres"].fillna("Unknown")

    return data


df = load_data()


# =========================================================
# VALIDATE DATA
# =========================================================

required_columns = [
    "title",
    "author",
    "average_rating",
    "rating_count",
    "review_count",
    "number_of_pages",
    "publication_year",
    "genres",
    "book_category"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "The CSV is missing these columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def render_html(html_code):
    st.markdown(
        html_code,
        unsafe_allow_html=True
    )


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

    return (
        f'<span class="badge {css_class}">'
        f'{html.escape(str(display_name))}'
        f'</span>'
    )


def show_book_card(book):

    title = html.escape(str(book["title"]))
    author = html.escape(str(book["author"]))
    genres = html.escape(str(book["genres"]))

    details = [
        f'⭐ <strong>{book["average_rating"]:.2f}</strong>',
        f'👥 {format_number(book["rating_count"])} ratings',
        f'📝 {format_number(book["review_count"])} reviews'
    ]

    extra_details = []

    if pd.notna(book["number_of_pages"]) and book["number_of_pages"] > 0:
        extra_details.append(
            f'📖 {int(book["number_of_pages"]):,} pages'
        )

    if pd.notna(book["publication_year"]):
        extra_details.append(
            f'🗓️ {int(book["publication_year"])}'
        )

    detail_text = " &nbsp; · &nbsp; ".join(details)
    extra_text = " &nbsp; · &nbsp; ".join(extra_details)

    card_html = (
        '<div class="book-card">'
        f'<div class="book-title">{title}</div>'
        f'<div class="book-author">by {author}</div>'
        f'{category_badge(book["book_category"])}'
        '<div class="book-meta">'
        f'{detail_text}'
        '<br>'
        f'📚 {genres}'
    )

    if extra_text:
        card_html += f'<br>{extra_text}'

    card_html += '</div></div>'

    render_html(card_html)


def filter_by_genre(data, selected_genres):

    if not selected_genres:
        return data

    selected_lower = {
        str(genre).strip().lower()
        for genre in selected_genres
    }

    def has_genre(value):

        book_genres = {
            genre.strip().lower()
            for genre in str(value).split(",")
        }

        return bool(book_genres & selected_lower)

    return data[
        data["genres"].apply(has_genre)
    ]


def make_dark_chart(fig, ax):

    fig.patch.set_facecolor("#211713")
    ax.set_facecolor("#211713")

    ax.title.set_color("#fff0dc")
    ax.xaxis.label.set_color("#e8dac5")
    ax.yaxis.label.set_color("#e8dac5")

    ax.tick_params(
        axis="x",
        colors="#e8dac5"
    )

    ax.tick_params(
        axis="y",
        colors="#e8dac5"
    )

    for spine in ax.spines.values():
        spine.set_color("#5a4233")

    ax.grid(
        True,
        alpha=0.18
    )

    return fig


# =========================================================
# GENRE OPTIONS
# =========================================================

genre_counts = (
    df["genres"]
    .str.split(", ")
    .explode()
    .dropna()
    .value_counts()
)


def is_clean_genre(genre):

    genre = str(genre).strip()

    if genre.lower() == "unknown":
        return False

    if "-" in genre:
        return False

    if len(genre.split()) > 4:
        return False

    return True


clean_genres = [
    genre
    for genre in genre_counts.index
    if is_clean_genre(genre)
]


genre_category_keywords = {

    "✨ Fantasy & Speculative": [
        "fantasy",
        "science fiction",
        "dystopia",
        "paranormal",
        "magic",
        "supernatural",
        "urban fantasy"
    ],

    "💘 Romance": [
        "romance",
        "contemporary romance",
        "historical romance",
        "paranormal romance",
        "new adult"
    ],

    "🔍 Mystery & Thriller": [
        "mystery",
        "thriller",
        "crime",
        "suspense",
        "detective"
    ],

    "👻 Horror & Dark Fiction": [
        "horror",
        "gothic",
        "vampires",
        "ghosts",
        "dark"
    ],

    "🌱 Young Readers": [
        "young adult",
        "childrens",
        "middle grade",
        "picture books"
    ],

    "🏛️ Classics & Literature": [
        "classics",
        "literature",
        "literary fiction",
        "contemporary",
        "historical fiction",
        "poetry",
        "plays"
    ],

    "🧠 Nonfiction & Ideas": [
        "nonfiction",
        "biography",
        "memoir",
        "history",
        "philosophy",
        "psychology",
        "science",
        "politics",
        "religion",
        "business"
    ],

    "🎨 Lifestyle & Culture": [
        "art",
        "music",
        "travel",
        "food and drink",
        "cookbooks",
        "health",
        "self help"
    ]
}


genre_category_min_counts = {
    "✨ Fantasy & Speculative": 200,
    "💘 Romance": 500,
    "🔍 Mystery & Thriller": 150,
    "👻 Horror & Dark Fiction": 80,
    "🌱 Young Readers": 150,
    "🏛️ Classics & Literature": 150,
    "🧠 Nonfiction & Ideas": 120,
    "🎨 Lifestyle & Culture": 60
}


genre_categories = {}

for category, keywords in genre_category_keywords.items():

    min_count = genre_category_min_counts[category]
    matching_genres = []

    for genre in clean_genres:

        genre_lower = str(genre).lower()

        if genre_counts[genre] < min_count:
            continue

        if any(keyword in genre_lower for keyword in keywords):
            matching_genres.append(genre)

    genre_categories[category] = sorted(matching_genres)


all_genres = sorted(
    [
        genre
        for genre in clean_genres
        if genre_counts[genre] >= 300
    ]
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📚 Between the Lines")

st.sidebar.write(
    """
    A Goodreads exploration project about **quality**,
    **popularity**, and overlooked books.
    """
)

st.sidebar.divider()

st.sidebar.subheader("🔎 Filter the Library")

selected_genre_category = st.sidebar.selectbox(
    "Library Section",
    ["All Books"] + list(genre_categories.keys())
)

if "last_genre_section" not in st.session_state:
    st.session_state["last_genre_section"] = selected_genre_category

if st.session_state["last_genre_section"] != selected_genre_category:
    st.session_state["specific_genres"] = []
    st.session_state["last_genre_section"] = selected_genre_category

if selected_genre_category == "All Books":
    available_genres = all_genres
else:
    available_genres = genre_categories[selected_genre_category]

selected_genres = st.sidebar.multiselect(
    "Specific Genres",
    options=available_genres,
    placeholder="Optional",
    key="specific_genres"
)

category_options = sorted(
    df["book_category"]
    .dropna()
    .unique()
)

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

if not valid_years.empty:
    year_range = st.sidebar.slider(
        "Publication Year",
        min_value=int(valid_years.min()),
        max_value=int(valid_years.max()),
        value=(
            int(valid_years.min()),
            int(valid_years.max())
        )
    )
else:
    year_range = None

st.sidebar.divider()

st.sidebar.subheader("🕯️ The Collection")

st.sidebar.write(
    f"**{len(df):,} Goodreads books**"
)

st.sidebar.markdown(
    """
    Includes:

    - Ratings
    - Reviews
    - Genres
    - Page counts
    - Publication years
    """
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

if year_range is not None:

    filtered_df = filtered_df[
        filtered_df["publication_year"].isna()
        |
        filtered_df["publication_year"].between(
            year_range[0],
            year_range[1]
        )
    ]

if selected_genres:
    filtered_df = filter_by_genre(
        filtered_df,
        selected_genres
    )

if filtered_df.empty:
    st.warning("No books match this exact combination of filters.")
    st.info("Try changing the filters in the sidebar.")
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
    'Step into a digital library of more than 49,000 books. '
    'Explore how readers rate books, how popularity shapes perception, '
    'and which titles deserve more attention than they receive.'
    '</div>'
    '</div>'
)


# =========================================================
# METRICS
# =========================================================

metric_1, metric_2, metric_3, metric_4 = st.columns(4)

with metric_1:
    st.metric(
        "📚 Books",
        f"{len(filtered_df):,}"
    )

with metric_2:
    st.metric(
        "⭐ Average Rating",
        f"{filtered_df['average_rating'].mean():.2f}"
    )

with metric_3:
    st.metric(
        "👥 Total Ratings",
        format_number(filtered_df["rating_count"].sum())
    )

with metric_4:
    hidden_count = (
        filtered_df["book_category"] == "Hidden Gem"
    ).sum()

    st.metric(
        "💎 Hidden Gems",
        f"{hidden_count:,}"
    )

st.write("")


# =========================================================
# TABS
# =========================================================

library_tab, patterns_tab, hidden_tab, browse_tab, method_tab = st.tabs(
    [
        "🏛️ The Library",
        "📊 Reading Patterns",
        "💎 Hidden Shelves",
        "🔎 Browse",
        "🕯️ Method"
    ]
)


# =========================================================
# TAB 1 — LIBRARY
# =========================================================

with library_tab:

    render_html(
        '<div class="section-label">The Collection</div>'
        '<div class="section-title">A Look Inside the Library</div>'
    )

    left_col, right_col = st.columns(
        2,
        gap="large"
    )

    with left_col:

        category_counts = (
            filtered_df["book_category"]
            .value_counts()
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        category_counts.sort_values().plot(
            kind="barh",
            ax=ax
        )

        ax.set_title("Books by Category")
        ax.set_xlabel("Number of Books")
        ax.set_ylabel("Category")

        fig = make_dark_chart(fig, ax)

        st.pyplot(fig)

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

        fig = make_dark_chart(fig, ax)

        st.pyplot(fig)

    render_html(
        '<div class="insight-box">'
        '<div class="insight-title">What stands out</div>'
        'Most books are rated close to four stars. '
        'Very low average ratings are relatively rare, showing that Goodreads ratings '
        'are concentrated within a fairly high range.'
        '</div>'
    )

    st.markdown("### 📚 The Most Common Genres")

    top_genres = (
        filtered_df["genres"]
        .str.split(", ")
        .explode()
        .value_counts()
        .head(12)
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    top_genres.sort_values().plot(
        kind="barh",
        ax=ax
    )

    ax.set_title("Most Common Genres")
    ax.set_xlabel("Number of Books")
    ax.set_ylabel("Genre")

    fig = make_dark_chart(fig, ax)

    st.pyplot(fig)


# =========================================================
# TAB 2 — PATTERNS
# =========================================================

with patterns_tab:

    render_html(
        '<div class="section-label">Exploratory Data Analysis</div>'
        '<div class="section-title">Reading Patterns</div>'
    )

    st.markdown("### Does popularity really mean quality?")

    scatter_df = filtered_df[
        filtered_df["rating_count"] > 0
    ].copy()

    if len(scatter_df) > 5000:
        scatter_df = scatter_df.sample(
            5000,
            random_state=42
        )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.scatter(
        np.log1p(scatter_df["rating_count"]),
        scatter_df["average_rating"],
        alpha=0.35
    )

    ax.set_title("Popularity vs Average Rating")
    ax.set_xlabel("Log of Rating Count")
    ax.set_ylabel("Average Rating")

    fig = make_dark_chart(fig, ax)

    st.pyplot(fig)

    render_html(
        '<div class="insight-box">'
        '<div class="insight-title">What the data suggests</div>'
        'Popularity does not guarantee a higher rating. '
        'Less popular books show a wider range of reader opinions, '
        'while highly popular books tend to settle into a more stable rating range.'
        '</div>'
    )

    st.markdown("### Average Rating by Genre")

    genre_df = filtered_df[
        [
            "genres",
            "average_rating"
        ]
    ].copy()

    genre_df["genres"] = genre_df["genres"].str.split(", ")
    genre_df = genre_df.explode("genres")

    top_10_genres = (
        genre_df["genres"]
        .value_counts()
        .head(10)
        .index
    )

    genre_rating = (
        genre_df[
            genre_df["genres"].isin(top_10_genres)
        ]
        .groupby("genres")["average_rating"]
        .mean()
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    genre_rating.plot(
        kind="barh",
        ax=ax
    )

    ax.set_title("Average Rating by Genre")
    ax.set_xlabel("Average Rating")
    ax.set_ylabel("Genre")

    fig = make_dark_chart(fig, ax)

    st.pyplot(fig)

    render_html(
        '<div class="insight-box">'
        '<div class="insight-title">Genre insight</div>'
        'The most common genres have very similar average ratings. '
        'Genre appears to make only a small difference in overall reader scores.'
        '</div>'
    )

    st.markdown("### Does book length affect rating?")

    pages_df = filtered_df.dropna(
        subset=["number_of_pages"]
    ).copy()

    pages_df = pages_df[
        pages_df["number_of_pages"] > 0
    ]

    if len(pages_df) > 5000:
        pages_df = pages_df.sample(
            5000,
            random_state=42
        )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.scatter(
        pages_df["number_of_pages"],
        pages_df["average_rating"],
        alpha=0.28
    )

    ax.set_title("Book Length vs Average Rating")
    ax.set_xlabel("Number of Pages")
    ax.set_ylabel("Average Rating")

    fig = make_dark_chart(fig, ax)

    st.pyplot(fig)

    with st.expander("📋 View Summary Statistics"):

        st.dataframe(
            filtered_df[
                [
                    "average_rating",
                    "rating_count",
                    "review_count",
                    "number_of_pages",
                    "publication_year"
                ]
            ]
            .describe()
            .round(2),
            use_container_width=True
        )


# =========================================================
# TAB 3 — HIDDEN SHELVES
# =========================================================

with hidden_tab:

    render_html(
        '<div class="section-label">Book Discovery</div>'
        '<div class="section-title">Hidden Shelves</div>'
    )

    hidden_inner, overrated_inner, loved_inner = st.tabs(
        [
            "💎 Hidden Gems",
            "📢 Overrated?",
            "👑 Popular for a Reason"
        ]
    )

    with hidden_inner:

        st.write(
            """
            Highly rated books with enough reader evidence,
            but less popularity than the typical book in the dataset.
            """
        )

        hidden_df = (
            filtered_df[
                filtered_df["book_category"] == "Hidden Gem"
            ]
            .sort_values(
                by=[
                    "average_rating",
                    "rating_count"
                ],
                ascending=[
                    False,
                    False
                ]
            )
        )

        if hidden_df.empty:
            st.info("No hidden gems match the current filters.")
        else:
            hidden_count_to_show = st.slider(
                "Number of hidden gems to show",
                5,
                25,
                10
            )

            for _, book in hidden_df.head(hidden_count_to_show).iterrows():
                show_book_card(book)

    with overrated_inner:

        st.write(
            """
            Highly popular books whose average ratings fall within
            the lower end of the dataset.
            """
        )

        overrated_df = (
            filtered_df[
                filtered_df["book_category"] == "Overrated"
            ]
            .sort_values(
                by="rating_count",
                ascending=False
            )
        )

        if overrated_df.empty:
            st.info("No overrated books match the current filters.")
        else:
            for _, book in overrated_df.head(12).iterrows():
                show_book_card(book)

    with loved_inner:

        st.write(
            """
            Books that achieved both high popularity and high reader ratings.
            """
        )

        loved_df = (
            filtered_df[
                filtered_df["book_category"] == "Popular and Highly Rated"
            ]
            .sort_values(
                by="rating_count",
                ascending=False
            )
        )

        if loved_df.empty:
            st.info("No books match the current filters.")
        else:
            for _, book in loved_df.head(12).iterrows():
                show_book_card(book)


# =========================================================
# TAB 4 — BROWSE
# =========================================================

with browse_tab:

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

        search_mask = (
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
        )

        browse_df = browse_df[
            search_mask
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
        browse_df[display_columns].head(1000),
        use_container_width=True,
        hide_index=True
    )

    csv_data = (
        browse_df.to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "⬇️ Download Filtered Collection",
        data=csv_data,
        file_name="filtered_goodreads_books.csv",
        mime="text/csv"
    )


# =========================================================
# TAB 5 — METHOD
# =========================================================

with method_tab:

    render_html(
        '<div class="section-label">Behind the Dashboard</div>'
        '<div class="section-title">The Method</div>'
        '<div class="section-description">'
        'The book categories are based on rating and popularity percentiles '
        'calculated from the cleaned dataset. This keeps the rules connected '
        'to the actual data instead of using arbitrary fixed thresholds.'
        '</div>'
    )

    high_rating = df["average_rating"].quantile(0.75)
    low_rating = df["average_rating"].quantile(0.25)
    minimum_popularity = df["rating_count"].quantile(0.25)
    median_popularity = df["rating_count"].median()
    high_popularity = df["rating_count"].quantile(0.75)

    method_1, method_2, method_3 = st.columns(3)

    with method_1:
        st.metric(
            "⭐ High Rating",
            f"{high_rating:.2f}+"
        )

    with method_2:
        st.metric(
            "👥 Minimum Evidence",
            f"{minimum_popularity:,.0f} ratings"
        )

    with method_3:
        st.metric(
            "📚 High Popularity",
            f"{high_popularity:,.0f}+ ratings"
        )

    st.markdown(
        f"""
### 💎 Hidden Gem
- Average rating of **{high_rating:.2f} or higher**
- At least **{minimum_popularity:,.0f} ratings**
- Fewer than **{median_popularity:,.0f} ratings**

---

### 👑 Popular for a Reason
- Average rating of **{high_rating:.2f} or higher**
- At least **{median_popularity:,.0f} ratings**

---

### 📢 Overrated?
- Average rating of **{low_rating:.2f} or lower**
- At least **{high_popularity:,.0f} ratings**

---

### 🌙 Under the Radar
- Fewer than **{minimum_popularity:,.0f} ratings**
- Not enough reader activity to judge confidently

---

### 📚 Typical
- Books that do not fall into the categories above
        """
    )

    st.markdown("### 🧹 Data Cleaning Process")

    st.markdown(
        """
- Kept only variables relevant to the analysis.
- Replaced missing original titles with the available title.
- Removed books without genre information.
- Removed genre vote numbers while keeping all genre labels.
- Recovered publication years from original date text.
- Removed books with zero reader ratings.
- Checked invalid ratings and duplicate records.
- Created custom book categories using dataset percentiles.
        """
    )

    st.markdown("### 🔍 Main Findings")

    st.markdown(
        """
- Most books have average ratings close to 4.0.
- Popularity does not guarantee a higher rating.
- Highly popular books tend to have more stable ratings.
- Common genres have relatively similar average scores.
- The dataset contains meaningful groups of hidden gems and highly popular lower-rated books.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

render_html(
    '<div style="'
    'text-align: center;'
    'color: #9f8b74;'
    'font-size: 0.85rem;'
    'padding: 1.5rem;'
    'letter-spacing: 0.04rem;'
    '">'
    '🕯️ Between the Lines'
    '<br>'
    'Goodreads Data Exploration Project'
    '</div>'
)
