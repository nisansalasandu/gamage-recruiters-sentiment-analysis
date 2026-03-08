# 📊 Sentiment Analysis of Social Media Mentions
### Gamage Recruiters (Pvt) Ltd — LinkedIn Brand Perception Analysis


---

## 📌 Project Overview

This project is a **Data Science Internship Task** focused on analyzing the sentiment of LinkedIn social media mentions of **Gamage Recruiters (Pvt) Ltd** — a professional recruitment and HR solutions company based in Sri Lanka.

The goal is to understand how the public perceives the company on LinkedIn by classifying public comments as **Positive**, **Neutral**, or **Negative** using Natural Language Processing (NLP) techniques. The findings are intended to support the company's **HR, recruitment, and marketing teams** in making data-driven decisions about their brand and engagement strategy.

---

## 🎯 Objectives

- Determine the overall public sentiment toward Gamage Recruiters on LinkedIn
- Identify recurring themes in positive and negative public reactions
- Analyze sentiment differences between Job Posts and Marketing Posts
- Provide actionable recommendations for HR, recruitment, and marketing teams
- Produce a professional summary report with visualizations

---

## 🔍 Focus Area

**Recruitment & HR / Branding Analytics**

---

## 📁 Project Structure

```
gamage-recruiters-sentiment-analysis/
│
├── 📂 charts/
│   ├── chart1_pie_overall_sentiment.png
│   ├── chart2_bar_sentiment_by_posttype.png
│   ├── chart3_hbar_vader_scores.png
│   ├── chart4_stacked_quality.png
│   ├── chart5_scatter_vader_vs_textblob.png
│   ├── chart6_boxplot_by_posttype.png
│   └── chart7_bar_engagement_by_sentiment.png
│
├── 📂 data/
│   ├── Gamage_Recruiters_Data_Collection.xlsx         ← Raw collected data (Step 3)
│   ├── Gamage_Recruiters_Cleaned_Data.xlsx            ← Cleaned data (Step 4)
│   ├── Gamage_Recruiters_Sentiment_Results.xlsx       ← Sentiment scores (Step 5)
│   └── Gamage_Recruiters_Aggregated_Results.xlsx      ← Aggregated results (Step 6)
│
├── 📄 step4_clean_data.py                             ← Data cleaning script
├── 📓 step5_sentiment_analysis.ipynb                  ← Sentiment analysis notebook
├── 📓 step6_aggregation.ipynb                         ← Aggregation notebook
├── 📓 step7_visualization.ipynb                       ← Visualization notebook
│
├── 📄 Gamage_Recruiters_Sentiment_Analysis_Report.docx ← Final summary report
├── 📄 README.md                                        ← This file
└── 📄 requirements.txt                                 ← Python dependencies
```

---

## 📊 Dataset Summary

| Attribute | Detail |
|---|---|
| **Platform** | LinkedIn |
| **Collection Method** | Manual scraping |
| **Collection Period** | January 2025 — February 2026 |
| **Total Posts Collected** | 112 |
| **Marketing Posts** | 64 |
| **Job Posts** | 48 |
| **Posts with Public Comments** | 21 (used for sentiment analysis) |
| **Posts without Comments** | 90 (excluded — no public text to analyze) |
| **English Posts** | 103 |
| **Sinhala Posts** | 8 (excluded — NLP tools are English-only) |

> **Why only 21 rows?**
> Sentiment analysis requires text written by the **public**, not by the company itself.
> Post captions are authored by Gamage Recruiters and reflect the company's own voice —
> analyzing them would measure self-promotional language, not genuine public perception.
> Only public comments (written by other LinkedIn users) were used for sentiment analysis.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.8+** | Core programming language |
| **pandas** | Data loading, manipulation, and aggregation |
| **openpyxl** | Reading and writing Excel (.xlsx) files |
| **vaderSentiment** | Primary sentiment analysis (designed for social media) |
| **TextBlob** | Secondary sentiment analysis (validation) |
| **matplotlib** | Chart creation and visualization |
| **seaborn** | Statistical chart styling |
| **re (regex)** | Text cleaning and pattern matching |
| **Jupyter Notebook** | Interactive analysis environment |

---

## ⚙️ Setup Instructions

### Prerequisites

Make sure you have **Python 3.8 or higher** installed.
You can check your version by running:

```bash
python --version
```

If you do not have Python installed, download it from [python.org](https://www.python.org/downloads/).

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/nisansalasandu/gamage-recruiters-sentiment-analysis.git
cd gamage-recruiters-sentiment-analysis
```

---

### Step 2 — (Recommended) Create a Virtual Environment

Using a virtual environment keeps your project dependencies isolated.

```bash
# Create virtual environment
python -m venv venv

# Activate it — Windows
venv\Scripts\activate

# Activate it — Mac / Linux
source venv/bin/activate
```

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

Or install each library individually:

```bash
pip install pandas
pip install openpyxl
pip install vaderSentiment
pip install textblob
pip install matplotlib
pip install seaborn
pip install jupyter
```

After installing TextBlob, download its language corpus (run this once):

```bash
python -m textblob.download_corpora
```

---

### Step 4 — Launch Jupyter Notebook

```bash
jupyter notebook
```

This will open Jupyter in your browser. Navigate to the project folder and open the notebooks in order.

---

## 🚀 How to Run the Project

Run the files in the following order. Each step depends on the output of the previous one.

### 1️⃣ Step 4 — Data Cleaning

```bash
python dataclean.py
```

**What it does:**
- Loads `Gamage_Recruiters_Data_Collection.xlsx`
- Renames columns to code-friendly format
- Removes empty rows and duplicates
- Fixes platform name spelling inconsistencies
- Standardizes date formats and removes typos (e.g. year 2036)
- Fixes post type column (removes accidentally pasted URLs)
- Detects language (English vs Sinhala)
- Cleans text: removes URLs, emojis, hashtags, phone numbers, emails, special characters
- Converts text to lowercase and removes extra whitespace

**Output:** `Gamage_Recruiters_Cleaned_Data.xlsx`

---

### 2️⃣ Step 5 — Sentiment Analysis

Open `sentiment_analysis.ipynb` in Jupyter and run all cells.

**What it does:**
- Loads the cleaned data
- Filters to only rows with public comment text (21 rows)
- Flags low-quality generic engagement phrases (CFBR, etc.)
- Applies **VADER** sentiment analysis (primary method)
- Applies **TextBlob** sentiment analysis (secondary / validation)
- Compares both methods and assigns a final sentiment label
- Classifies each comment as **Positive**, **Neutral**, or **Negative**

**Output:** `Gamage_Recruiters_Sentiment_Results.xlsx`

---

### 3️⃣ Step 6 — Aggregation

Open `step6_aggregation.ipynb` in Jupyter and run all cells.

**What it does:**
- Counts mentions per sentiment category
- Calculates percentages
- Breaks down sentiment by post type (Job Post vs Marketing Post)
- Analyzes meaningful vs low-quality comments
- Computes average engagement metrics per sentiment category

**Output:** `Gamage_Recruiters_Aggregated_Results.xlsx`

---

### 4️⃣ Step 7 — Visualization

Open `step7_visualization.ipynb` in Jupyter and run all cells.

**What it does:**
- Generates 7 charts saved to the `charts/` folder

**Output:** 7 `.png` chart files in `charts/`

---

## 📈 Results Summary

| Sentiment | Count | Percentage |
|---|---|---|
| ✅ Positive | 19 | 90.5% |
| ➖ Neutral | 2 | 9.5% |
| ❌ Negative | 0 | 0.0% |
| **Total** | **21** | **100%** |

**Key findings:**
- 90.5% of all public LinkedIn comments were classified as **Positive**
- **0% Negative** sentiment detected during the entire collection period
- Both VADER and TextBlob achieved **100% agreement** across all 21 comments
- **Marketing Posts** received 100% positive reactions
- **Job Posts** received 87.5% positive reactions
- 81.2% of posts received zero public comments — indicating low audience engagement overall

---

## 📉 Charts

All charts are saved in the `charts/` folder.

| File | Description |
|---|---|
| `chart1_pie_overall_sentiment.png` | Overall sentiment distribution (Positive / Neutral / Negative) |
| `chart2_bar_sentiment_by_posttype.png` | Sentiment counts and percentages by post type |
| `chart3_hbar_vader_scores.png` | VADER compound score per individual comment |
| `chart4_stacked_quality.png` | Sentiment split by meaningful vs low-quality comments |
| `chart5_scatter_vader_vs_textblob.png` | VADER vs TextBlob score agreement scatter plot |
| `chart6_boxplot_by_posttype.png` | Score distribution box plot by post type |
| `chart7_bar_engagement_by_sentiment.png` | Average likes, shares, and comments by sentiment |

---

## 🧠 Methodology

### Why Only Comment Text Was Analyzed

Post captions are written by Gamage Recruiters themselves and reflect the company's own marketing voice. Analyzing them would measure the company's self-promotional language rather than genuine public perception. Only **public comments written by other LinkedIn users** were used for sentiment analysis.

### Sentiment Tools

**VADER (Primary)**
VADER — Valence Aware Dictionary and sEntiment Reasoner — was built specifically for social media text. It handles informal language, short phrases, and punctuation patterns common in LinkedIn comments.

| Score | Meaning |
|---|---|
| compound >= 0.05 | Positive |
| compound <= -0.05 | Negative |
| between -0.05 and 0.05 | Neutral |

**TextBlob (Secondary / Validation)**
TextBlob provides a polarity score from -1.0 to +1.0. It was used as a cross-check. Where VADER and TextBlob agreed, the result was marked as **High Confidence**.

### Final Label Decision Rule
- Both methods agree → use that label (High Confidence)
- Methods disagree → use VADER label (Low Confidence)
- Result: **100% of results were High Confidence** (both methods agreed on all 21 comments)

---

## ⚠️ Limitations

- Only 21 comments were available for analysis out of 112 total posts
- Data collected from LinkedIn only — Facebook, Instagram, and Glassdoor not included
- Most comments are short generic phrases ("Great opportunity", "Exciting opportunity")
- 8 Sinhala-language posts were excluded as VADER and TextBlob do not support Sinhala
- No negative comments found — this may reflect genuine satisfaction or silent disengagement
- Data was collected manually which introduces potential for human transcription error

---

## 💡 Recommendations

| Recommendation | Team | Priority |
|---|---|---|
| Include industry name clearly in every job post | Recruitment | 🔴 High |
| Standardize weekly hiring bulletin format | Recruitment | 🔴 High |
| Grow LinkedIn follower base | HR & Branding | 🔴 High |
| Continue marketing partnership content | Marketing | 🟡 Medium |
| Reply to every comment received | Marketing | 🟡 Medium |
| Follow up on "I'm interested" comments | Recruitment & Marketing | 🟡 Medium |
| Expand data collection to Facebook and Glassdoor | HR & Branding | 🟢 Low |

---

## 📄 Report

The full summary report is available as a Word document:

📥 `Gamage_Recruiters_Sentiment_Analysis_Report.docx`

It includes:
- Executive Summary
- Objective and Scope
- Data Sources and Collection Method
- Sentiment Analysis Methodology
- Key Results with tables
- Key Insights
- Recommendations by team
- Limitations
- Conclusion

---

## 📦 requirements.txt

```
pandas>=1.5.0
openpyxl>=3.0.0
vaderSentiment>=3.3.2
textblob>=0.17.1
matplotlib>=3.5.0
seaborn>=0.12.0
jupyter>=1.0.0
nltk>=3.7
```

---

## 👤 Author

**Nisansala Ruwan Pathirana**
Data Science Intern
Gamage Recruiters (Pvt) Ltd
March 2026

---

## 📜 License

This project is for internal academic and internship purposes only.
Data collected is publicly available LinkedIn content.
All analysis complies with LinkedIn's terms of service and data privacy guidelines.
