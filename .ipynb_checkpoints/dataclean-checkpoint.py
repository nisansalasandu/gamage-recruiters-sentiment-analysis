"""
Step 4: Data Cleaning
Project : Sentiment Analysis of Social Media Mentions
Company : Gamage Recruiters
"""

import pandas as pd
import re

# ── File paths ─────────────────────────────────────────────
INPUT_FILE  = 'Gamage_Recruiters_Data_Collection.xlsx'
OUTPUT_FILE = 'Gamage_Recruiters_Cleaned_Data.xlsx'

# ── Load raw data ──────────────────────────────────────────
df = pd.read_excel(INPUT_FILE, sheet_name='Sheet2')
print(f'Rows loaded: {len(df)}')

# ── Rename columns ─────────────────────────────────────────
df.rename(columns={
    'Mention ID'              : 'mention_id',
    'Platform'                : 'platform',
    'Date'                    : 'date',
    'Author (Optional)'       : 'author',
    'Caption of the post'     : 'caption',
    'Comment Text'            : 'comment_text',
    'No. of Likes'            : 'likes',
    'No. of Shares / Reposts' : 'shares',
    'No. of Comments'         : 'num_comments',
    'Post URL'                : 'post_url',
    'Type of Post'            : 'post_type',
}, inplace=True)

# ── Remove fully empty rows ────────────────────────────────
df = df[df['mention_id'].notna()]
df = df.reset_index(drop=True)

# ── Fix platform spelling ──────────────────────────────────
df['platform'] = df['platform'].astype(str).str.strip().str.title()
df['platform'] = df['platform'].str.replace('Linkedin', 'LinkedIn', regex=False)

# ── Fix dates ──────────────────────────────────────────────
df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
df.loc[df['date'].dt.year > 2027, 'date'] = pd.NaT

# ── Fix post type column ───────────────────────────────────
def fix_post_type(val):
    if pd.isna(val): return 'Unknown'
    val = str(val).strip()
    if val.startswith('http'): return 'Unknown'
    if 'job' in val.lower(): return 'Job Post'
    return val

df['post_type'] = df['post_type'].apply(fix_post_type)

# ── Remove duplicates ──────────────────────────────────────
df = df.drop_duplicates(subset=['caption'], keep='first')
df = df.reset_index(drop=True)

# ── Detect language ────────────────────────────────────────
def detect_language(text):
    if pd.isna(text): return 'no_text'
    if len(re.findall(r'[\u0D80-\u0DFF]', str(text))) > 5:
        return 'sinhala'
    return 'english'

df['language'] = df['caption'].apply(detect_language)

# ── Text cleaning function ─────────────────────────────────
def clean_text(text):
    if pd.isna(text) or str(text).strip() == '': return ''
    text = str(text)
    text = re.sub(r'http\S+|www\.\S+', '', text)           # remove URLs
    text = re.sub(r'[\U00010000-\U0010ffff'
                  r'\U0001F600-\U0001F64F'
                  r'\U0001F300-\U0001F5FF'
                  r'\U0001F680-\U0001F6FF'
                  r'\u2600-\u26FF\u2700-\u27BF'
                  r'\u25A0-\u25FF\u2B00-\u2BFF]',
                  '', text, flags=re.UNICODE)                # remove emojis
    text = re.sub(r'hashtag#\S+|#\S+', '', text)           # remove hashtags
    text = re.sub(r'\b0\d{2}[\s\-]?\d{3}[\s\-]?\d{4}\b',
                  '', text)                                  # remove phone numbers
    text = re.sub(r'\S+@\S+\.\S+', '', text)               # remove emails
    text = re.sub(r'[^a-zA-Z0-9\u0D80-\u0DFF\s.,!?\'"-]',
                  ' ', text)                                 # remove special chars
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['comment_cleaned'] = df['comment_text'].apply(clean_text)

# ── Save ───────────────────────────────────────────────────
output_cols = [
    'mention_id', 'platform', 'date', 'author',
    'post_type', 'language',
    'caption', 'comment_text', 'comment_cleaned',
    'likes', 'shares', 'num_comments', 'post_url'
]

df[output_cols].to_excel(OUTPUT_FILE, index=False, sheet_name='Cleaned_Data')

print(f'Rows saved       : {len(df)}')
print(f'Rows with comment: {df["comment_cleaned"].notna().sum()}')
print(f'Output saved to  : {OUTPUT_FILE}')