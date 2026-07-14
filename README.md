# 📚 Between the Lines

## Goodreads Data Exploration

**Between the Lines** is a data analysis project built using the Goodreads Books dataset. The project explores how book ratings, popularity, genres, and reader engagement relate to each other through data analysis and an interactive Streamlit dashboard.

The main question explored in this project is:

> **Does popularity really mean quality, or are some highly rated books being overlooked?**

---

## Live Demo

🌐 https://goodreads-eda.streamlit.app/

---

## Project Objectives

This project was completed as part of a Data Science and AI bootcamp to practice the full data analysis workflow.

The project covers:

- Loading and exploring a real-world dataset
- Cleaning and preparing the data
- Performing exploratory data analysis (EDA)
- Creating visualizations to discover patterns
- Building an interactive Streamlit dashboard
- Applying a simple machine learning model

---

## Dataset

- **Source:** Goodreads Books Dataset (Kaggle)
 https://www.kaggle.com/datasets/austinreese/goodreads-books
- **Original Size:** 52,199 books
- **Cleaned Size:** 49,351 books

The dataset includes:

- Book titles
- Authors
- Genres
- Average ratings
- Rating counts
- Review counts
- Number of pages
- Publication years
- Star rating distributions

---

## Data Cleaning

The dataset was cleaned before analysis by:

- Selecting only the required columns
- Handling missing values
- Removing duplicate records
- Cleaning genre names
- Recovering missing publication years when possible
- Removing books with zero ratings
- Converting data types
- Creating a custom **Book Category** column

---

## Exploratory Data Analysis

The notebook includes:

- Distribution of average ratings
- Most common genres
- Distribution of page counts
- Popularity vs average rating
- Number of pages vs average rating
- Correlation heatmap
- Average rating by genre
- Book category distribution
- Boxplots and summary insights

Each visualization includes a short explanation of the findings.

---

## Book Categories

Books were grouped into five custom categories based on their ratings and popularity.

| Category | Description |
|----------|-------------|
| 💎 Hidden Gem | Highly rated books with lower popularity |
| 👑 Popular and Highly Rated | Books with both high ratings and high popularity |
| 📢 Overrated | Very popular books with relatively lower ratings |
| 🔍 Under the Radar | Books with very few ratings |
| 📚 Typical | Books that do not fit the other categories |

---

## Predictive Model

As an optional extension, a simple Logistic Regression model was created to predict whether a book is popular.

Features used:

- Average Rating
- Review Count
- Number of Pages
- Publication Year

Model accuracy:

**89.1%**

This shows that the selected features can predict book popularity with good accuracy.

---

## Streamlit Dashboard

The dashboard allows users to explore the dataset interactively.

Features include:

- Genre filtering
- Book category filtering
- Rating and publication year filters
- Interactive Plotly charts
- Hidden Gems explorer
- Book search
- Collection browser
- Download filtered data

---

## Repository Structure

```
GoodReads-EDA/
│
├── app.py
├── clean_goodreads_books.csv
├── Goodreads_EDA_project.ipynb
├── requirements.txt
├── runtime.txt
└── README.md
```

---

## How to Run

1. Clone the repository

```bash
git clone https://github.com/your-username/GoodReads-EDA.git
```

2. Install the required libraries

```bash
pip install -r requirements.txt
```

3. Run the dashboard

```bash
streamlit run app.py
```

---

## Tools Used

- Python
- Pandas
- NumPy
- Plotly
- Matplotlib
- Seaborn
- Streamlit
- Scikit-learn
- Google Colab

---

## Key Findings

- Most Goodreads books are rated close to 4 stars.
- Popularity does not always mean a higher rating.
- Book length has only a weak relationship with ratings.
- Hidden Gems can be identified by combining ratings with popularity.
- Reader engagement is a strong indicator of whether a book is popular.

