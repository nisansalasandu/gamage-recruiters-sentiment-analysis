"""
=============================================================
STEP 4: Data Cleaning Script
Project : Sentiment Analysis of Social Media Mentions
Company : Gamage Recruiters
Author  : Data Science Intern
=============================================================

This script cleans the raw LinkedIn data collected.
"""

import pandas as pd
import re
import os

# ── File paths ────────────────────────────────────────────
INPUT_FILE  = "F:/physical science/4th year/Internship/Task 10/gamage-recruiters-sentiment-analysis/Gamage_Recruiters_Data_Collection.xlsx"
OUTPUT_FILE = "F:/physical science/4th year/Internship/Task 10/gamage-recruiters-sentiment-analysis/Gamage_Recruiters_Cleaned_Data_Collection.xlsx"

# ─────────────────────────────────────────────────────────
# LOAD THE RAW DATA
# ─────────────────────────────────────────────────────────


print("=" * 60)
print("Data Cleaning — Gamage Recruiters Dataset")
print("=" * 60)

df = pd.read_excel(INPUT_FILE, sheet_name="Sheet2")

print(f"\nRaw data loaded successfully.")
print(f"      Rows    : {len(df)}")
print(f"      Columns : {list(df.columns)}")


# ─────────────────────────────────────────────────────────
# FIX COLUMN NAMES
# ─────────────────────────────────────────────────────────
# Rename columns to shorter, code-friendly names so they
# are easier to reference throughout the script.
# ─────────────────────────────────────────────────────────

df.rename(columns={
    "Mention ID"           : "mention_id",
    "Platform"             : "platform",
    "Date"                 : "date",
    "Author (Optional)"    : "author",
    "Caption of the post"  : "caption",
    "Comment Text"         : "comment_text",
    "No. of Likes"         : "likes",
    "No. of Shares / Reposts": "shares",
    "No. of Comments"      : "num_comments",
    "Post URL"             : "post_url",
    "Type of Post"         : "post_type",
}, inplace=True)

print(f"\nColumn names renamed to code-friendly format.")


# ─────────────────────────────────────────────────────────
# REMOVE COMPLETELY EMPTY ROWS
# ─────────────────────────────────────────────────────────
# Rows where BOTH caption AND comment_text are empty have
# no text to analyze. We drop them entirely.
# ─────────────────────────────────────────────────────────

before = len(df)
df = df[~(df["caption"].isna() & df["comment_text"].isna())]
df = df[df["mention_id"].notna()]   # also drop rows with no ID
after = len(df)

print(f"Before : {before} rows")
print(f"After  : {after} rows")
print(f"Removed: {before - after} empty rows")


# ─────────────────────────────────────────────────────────
# STANDARDIZE PLATFORM NAME
# ─────────────────────────────────────────────────────────
# Data has "LinkedIn" and "LInkedIn".
# Fixing all variations to a single consistent spelling.
# ─────────────────────────────────────────────────────────

df["platform"] = df["platform"].astype(str).str.strip().str.title()
# str.title() makes it "Linkedin" — we then force correct capital
df["platform"] = df["platform"].str.replace("Linkedin", "LinkedIn", regex=False)

print(f"\nPlatform names standardized.")
print(f"      Unique platforms now: {df['platform'].unique()}")


# ─────────────────────────────────────────────────────────
# FIX DATES
# ─────────────────────────────────────────────────────────
# Dates come in mixed formats: "28/2/2026", datetime objects,
# and one obvious typo "2036". We parse all to a standard
# format YYYY-MM-DD and flag the suspicious 2036 entry.
# ─────────────────────────────────────────────────────────

df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

# Flag any dates that are clearly wrong (future beyond 2027)
suspicious = df[df["date"].dt.year > 2027]
if len(suspicious) > 0:
    print(f"\nWARNING — {len(suspicious)} suspicious date(s) found and set to NaT:")
    print(suspicious[["mention_id", "date"]])
    df.loc[df["date"].dt.year > 2027, "date"] = pd.NaT
else:
    print(f"\nAll dates look valid.")

print(f"\nDate range: {df['date'].min().date()} -> {df['date'].max().date()}")

# ─────────────────────────────────────────────────────────
# FIX POST TYPE COLUMN
# ─────────────────────────────────────────────────────────
# Some rows have URLs accidentally pasted into the post_type
# column. We detect these and replace with "Unknown" so
# the category is clean for grouping later.
# ─────────────────────────────────────────────────────────

def fix_post_type(val):
    if pd.isna(val):
        return "Unknown"
    val = str(val).strip()
    if val.startswith("http"):          # URL ended up here by mistake
        return "Unknown"
    if val.lower() in ["job ppost", "job  post"]:
        return "Job Post"               # fix typo
    return val

df["post_type"] = df["post_type"].apply(fix_post_type)

print(f"\nPost type column fixed.")
print(f"      Post type counts:\n{df['post_type'].value_counts().to_string()}")



# ─────────────────────────────────────────────────────────
# DETECT LANGUAGE (English vs Sinhala)
# ─────────────────────────────────────────────────────────
# Sinhala text (Unicode range U+0D80–U+0DFF) cannot be
# analyzed by English NLP tools like VADER or TextBlob.
# We flag these rows so you know which ones to skip or
# handle separately.
# ─────────────────────────────────────────────────────────

def detect_language(text):
    """Returns 'sinhala' if text contains Sinhala Unicode chars, else 'english'."""
    if pd.isna(text):
        return "no_text"
    # Check for Sinhala Unicode block characters
    sinhala_chars = re.findall(r'[\u0D80-\u0DFF]', str(text))
    if len(sinhala_chars) > 5:   # more than 5 Sinhala chars = Sinhala post
        return "sinhala"
    return "english"

df["language"] = df["caption"].apply(detect_language)

lang_counts = df["language"].value_counts()
print(f"\nLanguage detection complete.")
print(f"      Language breakdown:\n{lang_counts.to_string()}")
print(f"      NOTE: Sinhala posts will be excluded from English sentiment analysis.")


# ─────────────────────────────────────────────────────────
# TEXT CLEANING FUNCTION
# ─────────────────────────────────────────────────────────
# This is the core cleaning step. We apply a series of
# transformations to make raw text ready for NLP:
#
#   a) Remove URLs          (http://... or www...)
#   b) Remove emojis        (Unicode emoji characters)
#   c) Remove hashtags      (#word → removed entirely)
#   d) Remove phone numbers (077 xxx xxxx style)
#   e) Remove email addresses
#   f) Remove special characters (keep only letters/spaces)
#   g) Convert to lowercase
#   h) Remove extra whitespace
# ─────────────────────────────────────────────────────────

def clean_text(text):
    """Clean a single text string for NLP analysis."""
    if pd.isna(text) or str(text).strip() == "":
        return ""

    text = str(text)

    # a) Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)

    # b) Remove emojis (broad Unicode emoji range)
    text = re.sub(
        r'[\U00010000-\U0010ffff'   # supplementary planes (most emojis)
        r'\U0001F600-\U0001F64F'    # emoticons
        r'\U0001F300-\U0001F5FF'    # symbols & pictographs
        r'\U0001F680-\U0001F6FF'    # transport & map symbols
        r'\U0001F1E0-\U0001F1FF'    # flags
        r'\u2600-\u26FF'            # misc symbols
        r'\u2700-\u27BF'            # dingbats
        r'\u25A0-\u25FF'            # geometric shapes (▪ ▸ etc.)
        r'\u2B00-\u2BFF]',          # misc symbols
        '', text, flags=re.UNICODE
    )

    # c) Remove hashtags (e.g. hashtag#GamageRecruiters or #hiring)
    text = re.sub(r'hashtag#\S+', '', text)
    text = re.sub(r'#\S+', '', text)

    # d) Remove phone numbers (Sri Lanka format)
    text = re.sub(r'\b0\d{2}[\s\-]?\d{3}[\s\-]?\d{4}\b', '', text)

    # e) Remove email addresses
    text = re.sub(r'\S+@\S+\.\S+', '', text)

    # f) Remove special characters — keep only letters, numbers, spaces, . , ! ?
    text = re.sub(r'[^a-zA-Z0-9\u0D80-\u0DFF\s.,!?\'"-]', ' ', text)

    # g) Convert to lowercase
    text = text.lower()

    # h) Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


# Apply the cleaning function to both text columns
df["caption_cleaned"]      = df["caption"].apply(clean_text)
df["comment_text_cleaned"] = df["comment_text"].apply(clean_text)

print(f"\nText cleaning applied to caption and comment columns.")
print(f"\n      Example — BEFORE cleaning:")
print(f"      {df['caption'].iloc[2][:120]}...")
print(f"\n      Example — AFTER cleaning:")
print(f"      {df['caption_cleaned'].iloc[2][:120]}...")


# ─────────────────────────────────────────────────────────
# CREATE PRIMARY TEXT COLUMN FOR ANALYSIS
# ─────────────────────────────────────────────────────────
# For sentiment analysis, we need ONE text column
# per row. The logic is:
#   - If a comment exists → use comment (it's the public reaction)
#   - Otherwise           → use the post caption
# ─────────────────────────────────────────────────────────

def get_primary_text(row):
    comment = str(row["comment_text_cleaned"]).strip()
    caption = str(row["caption_cleaned"]).strip()
    if comment and comment != "nan":
        return comment
    elif caption and caption != "nan":
        return caption
    return ""

df["text_for_analysis"] = df.apply(get_primary_text, axis=1)

# Drop rows where we have no usable text at all
before = len(df)
df = df[df["text_for_analysis"].str.strip() != ""]
after = len(df)
print(f"\nPrimary text column created: 'text_for_analysis'")
print(f"       Rows with usable text: {after}  ({before - after} rows had no text)")


# ─────────────────────────────────────────────────────────
# FILTER BY RECRUITMENT KEYWORDS
# ─────────────────────────────────────────────────────────
# This optional step keeps only posts that mention topics
# relevant to recruitment, HR, or company reputation.
# This makes the analysis more focused.
# Set APPLY_KEYWORD_FILTER = True to activate it.
# ─────────────────────────────────────────────────────────

APPLY_KEYWORD_FILTER = False   # Change to True if you want to filter

RECRUITMENT_KEYWORDS = [
    "recruit", "hiring", "job", "career", "hr", "talent",
    "candidate", "vacancy", "interview", "apply", "position",
    "gamage", "staffing", "workforce", "payroll", "employment"
]

if APPLY_KEYWORD_FILTER:
    pattern = '|'.join(RECRUITMENT_KEYWORDS)
    before = len(df)
    df = df[df["text_for_analysis"].str.contains(pattern, case=False, na=False)]
    after = len(df)
    print(f"\nKeyword filter APPLIED — kept only recruitment-related posts.")
    print(f"       Before: {before}  →  After: {after} rows")
else:
    print(f"\nKeyword filter SKIPPED (APPLY_KEYWORD_FILTER = False).")
    print(f"       All {len(df)} rows retained.")


# ─────────────────────────────────────────────────────────
# FINAL SUMMARY & SAVE
# ─────────────────────────────────────────────────────────

# Select and reorder columns for the clean output file
output_cols = [
    "mention_id", "platform", "date", "author",
    "post_type", "language",
    "caption", "caption_cleaned",
    "comment_text", "comment_text_cleaned",
    "text_for_analysis",
    "likes", "shares", "num_comments",
    "post_url"
]

df_output = df[output_cols].copy()

# Save to Excel
df_output.to_excel(OUTPUT_FILE, index=False, sheet_name="Cleaned_Data")

print(f"\n{'=' * 60}")
print(f"CLEANING COMPLETE — FINAL SUMMARY")
print(f"{'=' * 60}")
print(f"  Total clean rows saved  : {len(df_output)}")
print(f"  English posts           : {(df_output['language'] == 'english').sum()}")
print(f"  Sinhala posts           : {(df_output['language'] == 'sinhala').sum()}")
print(f"  Posts with comments     : {(df_output['comment_text_cleaned'].notna() & (df_output['comment_text_cleaned'] != '')).sum()}")
print(f"  Post types              : {df_output['post_type'].value_counts().to_dict()}")
print(f"  Date range              : {df_output['date'].min()} -> {df_output['date'].max()}")
print(f"\n  Output saved to: {OUTPUT_FILE}")
print(f"{'=' * 60}")

