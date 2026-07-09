import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


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
# CUSTOM LIBRARY AESTHETIC
# =========================================================

st.markdown(
    """
    <style>

    /* Main app background */
    .stApp {
        background:
            radial-gradient(circle at top right, rgba(116, 81, 45, 0.10), transparent 30%),
            linear-gradient(180deg, #F8F2E7 0%, #F3E8D6 100%);
        color: #2F241F;
    }

    /* Main page width */
    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #241A16 0%, #35251F 100%);
        border-right: 1px solid #5B4033;
    }

    [data-testid="stSidebar"] * {
        color: #F7EEDC;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #E8C98E;
    }

    /* Hero */
    .hero {
        padding: 2.8rem 3rem;
        border-radius: 24px;
        background:
            linear-gradient(
                120deg,
                rgba(41, 27, 21, 0.96),
                rgba(75, 46, 35, 0.93)
            );
        box-shadow: 0 18px 45px rgba(64, 42, 31, 0.18);
        margin-bottom: 2rem;
        border: 1px solid rgba(232, 201, 142, 0.25);
    }

    .hero-eyebrow {
        color: #D6B478;
        font-size: 0.85rem;
        letter-spacing: 0.18rem;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }

    .hero-title {
        color: #FFF8EB;
        font-size: 3.2rem;
        line-height: 1.05;
        font-weight: 700;
        margin: 0;
    }

    .hero-subtitle {
        color: #E8D9C2;
        font-size: 1.1rem;
        margin-top: 1rem;
        max-width: 800px;
        line-height: 1.7;
    }

    /* Section heading */
    .section-label {
        color: #7A4E36;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.13rem;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
    }

    .section-title {
        color: #35241D;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    /* Custom cards */
    .library-card {
        background: rgba(255, 252, 245, 0.88);
        border: 1px solid #E2D2BA;
        border-radius: 18px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 8px 24px rgba(72, 49, 35, 0.07);
        height: 100%;
    }

    .card-label {
        color: #806B5A;
        font-size: 0.78rem;
        letter-spacing: 0.08rem;
        text-transform: uppercase;
    }

    .card-value {
        color: #3A2720;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 0.35rem;
    }

    /* Book recommendation cards */
    .book-card {
        background: #FFFDF8;
        border: 1px solid #E0D1BB;
        border-left: 6px solid #7A4735;
        padding: 1.3rem 1.5rem;
        border-radius: 14px;
        margin-bottom: 1rem;
        box-shadow: 0 6px 18px rgba(67, 44, 31, 0.07);
    }

    .book-title {
        color: #38261E;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .book-author {
        color: #7C6455;
        font-size: 0.92rem;
        margin-bottom: 0.8rem;
    }

    .book-meta {
        color: #55443A;
        font-size: 0.88rem;
        line-height: 1.7;
    }

    /* Insight box */
    .insight-box {
        background: #EEE2CC;
        border-left: 5px solid #6A4A38;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin: 1rem 0;
        color: #3E3028;
    }

    /* Category badges */
    .badge {
        display: inline-block;
        padding: 0.32rem 0.7rem;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 700;
        margin-right: 0.4rem;
    }

    .hidden-gem {
        background: #DDE9D7;
        color: #385233;
    }

    .overrated {
        background: #F2D8D0;
        color: #783C31;
    }

    .popular {
        background: #EEE0B8;
        color: #6B5418;
    }

    .radar {
        background: #DDD9E9;
        color: #554971;
    }

    .typical {
        background: #E8E2DA;
        color: #655B52;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-size: 0.95rem;
        font-weight: 600;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: rgba(255, 252, 245, 0.86);
        border: 1px solid #E2D2BA;
        padding: 1rem;
        border-radius: 16px;
    }

    /* Hide Streamlit menu/footer */
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
    data = pd.read_csv("clean_goodreads_books.csv")

    numeric_columns = [
        "average_rating",
        "rating_count",
        "review_count",
        "number_of_pages",
        "publication_year"
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

    data["genres"] = data["genres"].fillna("Unknown")
    data["title"] = data["title"].fillna("Unknown Title")
    data["author"] = data["author"].fillna("Unknown Author")

    return data


df = load_data()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_all_genres(data):
    genres = (
        data["genres"]
        .str.split(", ")
        .explode()
        .dropna()
        .unique()
    )

    return sorted(genres)


def filter_by_genres(data, selected_genres):
    if not selected_genres:
        return data

    genre_mask = data["genres"].apply(
        lambda value: any(
            selected_genre in value.split(", ")
            for selected_genre in selected_genres
        )
    )

    return data[genre_mask]


def format_number(number):
    if pd.isna(number):
        return "N/A"

    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"

    if number >= 1_000:
        return f"{number / 1_000:.1f}K"

    return f"{number:,.0f}"


def category_badge(category):
    badge_classes = {
        "Hidden Gem": "hidden-gem",
        "Overrated": "overrated",
        "Popular and Highly Rated": "popular",
        "Under the Radar": "radar",
        "Typical": "typical"
    }

    css_class = badge_classes.get(
        category,
        "typical"
    )

    return (
        f'<span class="badge {css_class}">'
        f'{category}'
        f'</span>'
    )


def show_book_card(book):
    pages = (
        f"{int(book['number_of_pages']):,} pages"
        if pd.notna(book["number_of_pages"])
        else "Page count unavailable"
    )

    year = (
        str(int(book["publication_year"]))
        if pd.notna(book["publication_year"])
        else "Unknown year"
    )

    st.markdown(
        f"""
        <div class="book-card">
            <div class="book-title">
                {book["title"]}
            </div>

            <div class="book-author">
                by {book["author"]}
            </div>

            {category_badge(book["book_category"])}

            <div class="book-meta">
                ⭐ <strong>{book["average_rating"]:.2f}</strong>
                &nbsp; · &nbsp;
                👥 {format_number(book["rating_count"])} ratings
                <br>
                📚 {book["genres"]}
                <br>
                📖 {pages}
                &nbsp; · &nbsp;
                🗓️ {year}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("# 📚 Between the Lines")

st.sidebar.markdown(
    """
    A Goodreads data exploration project focused on
    **quality, popularity, and overlooked books**.
    """
)

st.sidebar.divider()

st.sidebar.markdown("### 🔎 Filter the Library")

all_genres = get_all_genres(df)

selected_genres = st.sidebar.multiselect(
    "Genres",
    options=all_genres,
    placeholder="Choose one or more genres"
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

rating_min = float(df["average_rating"].min())
rating_max = float(df["average_rating"].max())

rating_range = st.sidebar.slider(
    "Average Rating",
    min_value=rating_min,
    max_value=rating_max,
    value=(rating_min, rating_max),
    step=0.1
)

available_years = (
    df["publication_year"]
    .dropna()
)

if not available_years.empty:
    min_year = int(available_years.min())
    max_year = int(available_years.max())

    year_range = st.sidebar.slider(
        "Publication Year",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
else:
    year_range = None

st.sidebar.divider()

st.sidebar.markdown(
    """
    ### 📖 Dataset

    **52K+ Goodreads books**

    Includes:

    - Book ratings
    - Reader engagement
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
    filtered_df["book_category"].isin(
        selected_categories
    )
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

filtered_df = filter_by_genres(
    filtered_df,
    selected_genres
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">
            Goodreads Data Exploration
        </div>

        <h1 class="hero-title">
            Between the Lines
        </h1>

        <div class="hero-subtitle">
            Does popularity really mean quality?
            Explore more than 49,000 books,
            uncover reader patterns, find hidden gems,
            and discover which books may be getting
            more attention than their ratings suggest.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# METRICS
# =========================================================

if filtered_df.empty:
    st.warning(
        "No books match the selected filters. "
        "Try adjusting the sidebar options."
    )
    st.stop()


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
        format_number(
            filtered_df["rating_count"].sum()
        )
    )

with metric_4:
    hidden_gem_count = (
        filtered_df["book_category"]
        == "Hidden Gem"
    ).sum()

    st.metric(
        "💎 Hidden Gems",
        f"{hidden_gem_count:,}"
    )


st.write("")


# =========================================================
# TABS
# =========================================================

(
    overview_tab,
    explore_tab,
    gems_tab,
    finder_tab,
    methodology_tab
) = st.tabs(
    [
        "🏛️ Library Overview",
        "📊 Between the Numbers",
        "💎 Hidden Gems & Hot Takes",
        "🔮 Find My Next Read",
        "🧠 How It Works"
    ]
)


# =========================================================
# TAB 1 — LIBRARY OVERVIEW
# =========================================================

with overview_tab:

    st.markdown(
        """
        <div class="section-label">
            The Collection
        </div>

        <div class="section-title">
            A Look Inside the Library
        </div>
        """,
        unsafe_allow_html=True
    )

    left_col, right_col = st.columns(
        [1.1, 1],
        gap="large"
    )

    with left_col:

        category_counts = (
            filtered_df["book_category"]
            .value_counts()
            .reset_index()
        )

        category_counts.columns = [
            "Category",
            "Books"
        ]

        category_fig = px.pie(
            category_counts,
            values="Books",
            names="Category",
            hole=0.58,
            title="How the Library Is Classified"
        )

        category_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend_title_text="",
            margin=dict(
                l=10,
                r=10,
                t=60,
                b=10
            )
        )

        st.plotly_chart(
            category_fig,
            use_container_width=True
        )

    with right_col:

        rating_fig = px.histogram(
            filtered_df,
            x="average_rating",
            nbins=25,
            title="Distribution of Average Ratings",
            labels={
                "average_rating": "Average Rating"
            }
        )

        rating_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            yaxis_title="Number of Books"
        )

        st.plotly_chart(
            rating_fig,
            use_container_width=True
        )

    st.markdown(
        """
        <div class="insight-box">
            <strong>Key insight:</strong>
            Most books are rated close to 4 stars.
            Very low average ratings are uncommon,
            meaning Goodreads ratings are generally
            concentrated in a relatively high range.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📚 Most Common Genres")

    genre_counts = (
        filtered_df["genres"]
        .str.split(", ")
        .explode()
        .value_counts()
        .head(12)
        .reset_index()
    )

    genre_counts.columns = [
        "Genre",
        "Books"
    ]

    genre_fig = px.bar(
        genre_counts,
        x="Books",
        y="Genre",
        orientation="h",
        title="Top Genres in the Selected Library"
    )

    genre_fig.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        genre_fig,
        use_container_width=True
    )


# =========================================================
# TAB 2 — BETWEEN THE NUMBERS
# =========================================================

with explore_tab:

    st.markdown(
        """
        <div class="section-label">
            Exploratory Data Analysis
        </div>

        <div class="section-title">
            Between the Numbers
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "### Does popularity really mean a better rating?"
    )

    scatter_data = filtered_df[
        filtered_df["rating_count"] > 0
    ].copy()

    if len(scatter_data) > 7000:
        scatter_data = scatter_data.sample(
            7000,
            random_state=42
        )

    scatter_data["log_rating_count"] = np.log1p(
        scatter_data["rating_count"]
    )

    popularity_fig = px.scatter(
        scatter_data,
        x="log_rating_count",
        y="average_rating",
        hover_name="title",
        hover_data={
            "author": True,
            "rating_count": ":,",
            "book_category": True,
            "log_rating_count": False
        },
        title="Popularity vs Average Rating",
        labels={
            "log_rating_count":
                "Log of Rating Count",
            "average_rating":
                "Average Rating"
        },
        opacity=0.45
    )

    popularity_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        popularity_fig,
        use_container_width=True
    )

    st.markdown(
        """
        <div class="insight-box">
            <strong>What the chart suggests:</strong>
            Popularity does not guarantee a higher rating.
            Less popular books show a much wider range of
            reader opinions, while very popular books tend
            to settle into a more stable rating range.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### How do genres compare?")

    expanded_genres = filtered_df[
        ["genres", "average_rating"]
    ].copy()

    expanded_genres["genres"] = (
        expanded_genres["genres"]
        .str.split(", ")
    )

    expanded_genres = expanded_genres.explode(
        "genres"
    )

    top_genre_names = (
        expanded_genres["genres"]
        .value_counts()
        .head(10)
        .index
    )

    genre_rating_data = (
        expanded_genres[
            expanded_genres["genres"].isin(
                top_genre_names
            )
        ]
        .groupby("genres")["average_rating"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    genre_rating_fig = px.bar(
        genre_rating_data,
        x="genres",
        y="average_rating",
        title="Average Rating Across the Most Common Genres",
        labels={
            "genres": "Genre",
            "average_rating": "Average Rating"
        }
    )

    genre_rating_fig.update_yaxes(
        range=[
            max(
                0,
                genre_rating_data[
                    "average_rating"
                ].min() - 0.15
            ),
            min(
                5,
                genre_rating_data[
                    "average_rating"
                ].max() + 0.10
            )
        ]
    )

    genre_rating_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_tickangle=-35
    )

    st.plotly_chart(
        genre_rating_fig,
        use_container_width=True
    )

    st.markdown(
        """
        <div class="insight-box">
            <strong>Genre insight:</strong>
            The most common genres have very similar
            average ratings. Genre appears to make only
            a small difference in overall reader scores.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Does book length affect rating?")

    pages_df = filtered_df.dropna(
        subset=["number_of_pages"]
    ).copy()

    pages_df = pages_df[
        pages_df["number_of_pages"] > 0
    ]

    if len(pages_df) > 7000:
        pages_df = pages_df.sample(
            7000,
            random_state=42
        )

    pages_fig = px.scatter(
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

    pages_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        pages_fig,
        use_container_width=True
    )

    with st.expander(
        "📋 View Summary Statistics"
    ):
        st.dataframe(
            filtered_df[
                [
                    "average_rating",
                    "rating_count",
                    "review_count",
                    "number_of_pages",
                    "publication_year"
                ]
            ].describe().round(2),
            use_container_width=True
        )


# =========================================================
# TAB 3 — HIDDEN GEMS & HOT TAKES
# =========================================================

with gems_tab:

    st.markdown(
        """
        <div class="section-label">
            Book Discovery
        </div>

        <div class="section-title">
            Hidden Gems & Hot Takes
        </div>
        """,
        unsafe_allow_html=True
    )

    hidden_tab, overrated_tab, loved_tab = st.tabs(
        [
            "💎 Hidden Gems",
            "📢 Overrated?",
            "👑 Popular for a Reason"
        ]
    )

    # ---------------- HIDDEN GEMS ----------------

    with hidden_tab:

        st.markdown(
            """
            Books with ratings in the top 25%,
            enough readers to provide evidence,
            but popularity below the dataset median.
            """
        )

        hidden_df = filtered_df[
            filtered_df["book_category"]
            == "Hidden Gem"
        ].sort_values(
            by=[
                "average_rating",
                "rating_count"
            ],
            ascending=[
                False,
                False
            ]
        )

        if hidden_df.empty:
            st.info(
                "No hidden gems match the current filters."
            )
        else:
            number_to_show = st.slider(
                "Number of hidden gems to show",
                3,
                20,
                8,
                key="hidden_number"
            )

            for _, book in hidden_df.head(
                number_to_show
            ).iterrows():
                show_book_card(book)

    # ---------------- OVERRATED ----------------

    with overrated_tab:

        st.markdown(
            """
            Highly popular books whose average ratings
            fall within the bottom 25% of the dataset.
            """
        )

        overrated_df = filtered_df[
            filtered_df["book_category"]
            == "Overrated"
        ].sort_values(
            by="rating_count",
            ascending=False
        )

        if overrated_df.empty:
            st.info(
                "No overrated books match the current filters."
            )
        else:
            for _, book in overrated_df.head(10).iterrows():
                show_book_card(book)

    # ---------------- POPULAR & HIGHLY RATED ----------------

    with loved_tab:

        st.markdown(
            """
            The books that managed to achieve both:
            high popularity and high reader ratings.
            """
        )

        loved_df = filtered_df[
            filtered_df["book_category"]
            == "Popular and Highly Rated"
        ].sort_values(
            by="rating_count",
            ascending=False
        )

        if loved_df.empty:
            st.info(
                "No books match the current filters."
            )
        else:
            for _, book in loved_df.head(10).iterrows():
                show_book_card(book)


# =========================================================
# TAB 4 — FIND MY NEXT READ
# =========================================================

with finder_tab:

    st.markdown(
        """
        <div class="section-label">
            Personal Discovery
        </div>

        <div class="section-title">
            Find My Next Read
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "Tell the library what you are looking for, "
        "and it will search the cleaned Goodreads data."
    )

    finder_col_1, finder_col_2 = st.columns(2)

    with finder_col_1:

        finder_genre = st.selectbox(
            "What genre are you in the mood for?",
            ["Any Genre"] + all_genres
        )

        minimum_rating = st.slider(
            "Minimum rating",
            1.0,
            5.0,
            4.0,
            0.1
        )

    with finder_col_2:

        finder_category = st.selectbox(
            "What kind of book?",
            [
                "Any Category",
                "Hidden Gem",
                "Popular and Highly Rated",
                "Under the Radar",
                "Typical",
                "Overrated"
            ]
        )

        max_pages = st.slider(
            "Maximum number of pages",
            100,
            2000,
            700,
            50
        )

    recommendation_df = df.copy()

    recommendation_df = recommendation_df[
        recommendation_df["average_rating"]
        >= minimum_rating
    ]

    recommendation_df = recommendation_df[
        recommendation_df["number_of_pages"].isna()
        |
        (
            recommendation_df["number_of_pages"]
            <= max_pages
        )
    ]

    if finder_genre != "Any Genre":
        recommendation_df = recommendation_df[
            recommendation_df["genres"].apply(
                lambda value:
                    finder_genre
                    in value.split(", ")
            )
        ]

    if finder_category != "Any Category":
        recommendation_df = recommendation_df[
            recommendation_df["book_category"]
            == finder_category
        ]

    st.write("")

    if st.button(
        "📖 Search the Shelves",
        use_container_width=True
    ):

        if recommendation_df.empty:
            st.warning(
                "No books match those preferences. "
                "Try changing one of the filters."
            )

        else:
            recommendations = (
                recommendation_df
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
                .head(12)
            )

            st.success(
                f"Found {len(recommendation_df):,} "
                "matching books. Here are some of the best."
            )

            for _, book in recommendations.iterrows():
                show_book_card(book)


# =========================================================
# TAB 5 — METHODOLOGY
# =========================================================

with methodology_tab:

    st.markdown(
        """
        <div class="section-label">
            Behind the Classification
        </div>

        <div class="section-title">
            How the Book Categories Work
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        """
        The categories are based on rating and popularity
        percentiles calculated from the cleaned dataset.
        This avoids choosing arbitrary fixed numbers.
        """
    )

    high_rating = df[
        "average_rating"
    ].quantile(0.75)

    low_rating = df[
        "average_rating"
    ].quantile(0.25)

    minimum_popularity = df[
        "rating_count"
    ].quantile(0.25)

    median_popularity = df[
        "rating_count"
    ].median()

    high_popularity = df[
        "rating_count"
    ].quantile(0.75)

    threshold_col_1, threshold_col_2, threshold_col_3 = (
        st.columns(3)
    )

    threshold_col_1.metric(
        "High Rating",
        f"{high_rating:.2f}+"
    )

    threshold_col_2.metric(
        "Minimum Evidence",
        f"{minimum_popularity:,.0f} ratings"
    )

    threshold_col_3.metric(
        "High Popularity",
        f"{high_popularity:,.0f}+ ratings"
    )

    st.write("")

    st.markdown(
        f"""
        ### 💎 Hidden Gem

        - Average rating of **{high_rating:.2f} or higher**
        - At least **{minimum_popularity:,.0f} ratings**
        - Fewer than **{median_popularity:,.0f} ratings**

        ---

        ### 👑 Popular and Highly Rated

        - Average rating of **{high_rating:.2f} or higher**
        - At least **{median_popularity:,.0f} ratings**

        ---

        ### 📢 Overrated

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

    st.markdown("### 🧹 Data Cleaning Summary")

    st.write(
        """
        The raw Goodreads data was prepared by:

        - keeping only variables relevant to the analysis
        - handling missing original titles
        - removing books without genre information
        - cleaning vote counts from genre labels
        - converting publication dates
        - creating a publication year feature
        - removing books with no reader ratings
        - checking invalid ratings and duplicate records
        """
    )


# =========================================================
# DATA EXPLORER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="section-label">
        Search the Collection
    </div>

    <div class="section-title">
        Explore the Data
    </div>
    """,
    unsafe_allow_html=True
)

search_term = st.text_input(
    "Search by book title or author",
    placeholder="Try a title or author name..."
)

display_df = filtered_df.copy()

if search_term:
    search_mask = (
        display_df["title"]
        .str.contains(
            search_term,
            case=False,
            na=False
        )
        |
        display_df["author"]
        .str.contains(
            search_term,
            case=False,
            na=False
        )
    )

    display_df = display_df[search_mask]


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
    display_df[display_columns]
    .sort_values(
        by="average_rating",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# DOWNLOAD
# =========================================================

csv_data = display_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Books",
    data=csv_data,
    file_name="filtered_goodreads_books.csv",
    mime="text/csv"
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <br><br>

    <div style="
        text-align: center;
        color: #816D60;
        font-size: 0.85rem;
        padding: 2rem;
    ">
        📚 Between the Lines
        <br>
        A Goodreads Data Exploration Project
    </div>
    """,
    unsafe_allow_html=True
)
