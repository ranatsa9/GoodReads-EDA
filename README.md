# GoodReads-EDA
# 📚 Between the Lines

## Goodreads Data Exploration Project

Between the Lines is a data analysis and dashboard project that explores Goodreads book data to understand the relationship between book quality, popularity, genres, and reader engagement.

The main goal of this project is to answer the question:

**Does popularity really mean quality, or are some highly rated books being overlooked?**

---
## Live Demo

You can view the interactive Streamlit dashboard here:

[Open the Live Dashboard](https://goodreads-eda.streamlit.app/)
## Project Overview

This project analyzes a Goodreads dataset containing more than 52,000 books. After cleaning the data, the final dataset includes 49,351 books with useful information such as ratings, review counts, genres, page counts, publication years, and custom book categories.

The project includes:

- Data cleaning
- Exploratory data analysis
- Data visualization
- Hidden Gem classification
- Interactive Streamlit dashboard
- Final report and presentation

---

## Dataset

**Dataset Name:** Goodreads Books  
**Source:** Kaggle  
**Original Size:** 52,199 rows and 31 columns  
**Cleaned Size:** 49,351 books

The dataset includes information about:

- Book title
- Author
- Average rating
- Rating count
- Review count
- Genres
- Number of pages
- Publication date
- Star rating counts

---

## Main Questions

This project focuses on answering the following questions:

1. What are the main patterns in Goodreads book ratings?
2. Does popularity lead to higher average ratings?
3. Which genres are most common?
4. Do different genres receive different average ratings?
5. Does book length affect rating?
6. Which books can be considered Hidden Gems?

---

## Data Cleaning

The cleaning process included:

- Keeping only relevant columns
- Replacing missing original titles with book titles
- Removing rows without genre information
- Cleaning genre values by removing vote numbers
- Recovering publication years from original date text
- Removing books with zero ratings
- Checking for duplicate records
- Checking for invalid average ratings
- Creating a new `book_category` column

---

## Book Categories

Books were classified into five categories using data-based thresholds:

| Category | Description |
|---|---|
| Hidden Gem | Highly rated books with moderate popularity |
| Popular and Highly Rated | Books with both high ratings and high popularity |
| Overrated | Highly popular books with lower ratings |
| Under the Radar | Books with very low rating counts |
| Typical | Books that do not fall into the other categories |

### Category Counts

| Category | Number of Books |
|---|---:|
| Typical | 26,091 |
| Under the Radar | 12,332 |
| Popular and Highly Rated | 5,549 |
| Hidden Gem | 2,966 |
| Overrated | 2,413 |

---

## Dashboard Features

The Streamlit dashboard allows users to interact with the cleaned Goodreads dataset.

Dashboard features include:

- Sidebar filters
- Genre filtering
- Book category filtering
- Rating and publication year filters
- Interactive charts
- Hidden Gems discovery section
- Book search feature
- Filtered data preview
- Download option for filtered data

---

## Files in This Repository

| File | Description |
|---|---|
| `app.py` | Streamlit dashboard code |
| `clean_goodreads_books.csv` | Cleaned dataset used in the dashboard |
| `requirements.txt` | Required Python libraries |
| `Between_the_Lines.ipynb` | Colab notebook for cleaning and analysis |
| `Between_the_Lines_Report.pdf` | Final project report |
| `Between_the_Lines_Presentation.pptx` | Final presentation |

---

## How to Run the Dashboard

First, install the required libraries:

```bash
pip install -r requirements.txt
