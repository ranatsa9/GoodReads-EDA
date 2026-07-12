# =========================================================
# GENRE OPTIONS
# =========================================================

all_genres = sorted(
    df["genres"]
    .str.split(", ")
    .explode()
    .dropna()
    .unique()
)


genre_category_keywords = {

    "✨ Fantasy & Speculative": [
        "fantasy",
        "magic",
        "paranormal",
        "science fiction",
        "dystopia",
        "steampunk",
        "supernatural"
    ],

    "💘 Romance": [
        "romance",
        "love"
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
        "dark",
        "vampire",
        "ghost"
    ],

    "🌱 Young Readers": [
        "young adult",
        "childrens",
        "middle grade",
        "picture book"
    ],

    "🏛️ Classics & Literature": [
        "classic",
        "literature",
        "literary",
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
        "food",
        "cookbook",
        "health",
        "self help"
    ]
}


genre_categories = {}

for category, keywords in genre_category_keywords.items():

    matching_genres = []

    for genre in all_genres:

        genre_lower = str(genre).lower()

        if any(
            keyword in genre_lower
            for keyword in keywords
        ):
            matching_genres.append(genre)

    genre_categories[category] = sorted(matching_genres)
