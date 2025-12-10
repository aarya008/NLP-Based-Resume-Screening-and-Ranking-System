# NLP-Based Resume Screening and Ranking System

📌 Project Overview

Recruitment often involves manually reviewing hundreds of resumes, which is time-consuming, subjective, and inefficient. This project automates the resume screening process by leveraging Natural Language Processing (NLP) and machine learning–based text similarity techniques to objectively evaluate and rank resumes against a given job description.

The system compares candidate resumes with job requirements, assigns relevance scores, and produces a ranked output, enabling recruiters to shortlist suitable candidates quickly and consistently.
⚙️ How the System Works

Job Description Processing

Reads the job description from a text file.

Extracts role context and required skills using rule-based parsing.

Resume Processing

Converts candidate resume PDFs into plain text.

Cleans and normalizes the text to remove noise.

Extracts skills, years of experience, and basic contact details using regex-based pattern recognition.

Text Vectorization & Scoring

Uses TF-IDF (Term Frequency–Inverse Document Frequency) to convert text into numerical vectors.

Applies cosine similarity to calculate how closely each resume matches the job description.

Generates a relevance score for every candidate.

Data Storage & Ranking

Stores job descriptions, candidate data, and scores in an SQLite database.

Fetches and ranks candidates in descending order of similarity score.

Exports the final ranked list as a CSV file for recruiter-friendly review.

🛠️ Technologies Used

Programming Language: Python

NLP & ML: TF-IDF Vectorization, Cosine Similarity (Scikit-learn)

Text Processing: Regex, custom text cleaning pipeline

Database: SQLite

Data Handling: Pandas

PDF Processing: PyPDF2
## Architecture Overview

- **OCR / Parsing**: Extract text from resume PDFs.
- **NLP Preprocessing**: Clean text (lowercasing, punctuation & stopword removal).
- **Feature Extraction**: Extract skills, experience, and basic metadata.
- **Vectorization**: TF-IDF vectorization for resumes and job description.
- **Similarity Scoring**: Cosine similarity to compute a score per candidate.
- **Database Logging**: Store candidate data and scores in SQLite.
- **Ranking Engine**: Export a ranked CSV of candidates.

## Project Structure

```text
resume-screening-bot/
│
├── data/
│   ├── resumes/              # Input PDF resumes
│   ├── jd/                   # Job description text files
│   └── samples/              # Optional sample skills lists, etc.
│
├── src/
│   ├── parser/
│   │   ├── pdf_reader.py     # PDF text extraction
│   │   └── text_cleaner.py   # Clean, normalize text
│   │
│   ├── nlp/
│   │   ├── skill_extractor.py  # Extract skills using NLP / patterns
│   │   ├── jd_processor.py     # Process job description
│   │   └── vectorizer.py       # TF-IDF vectorization
│   │
│   ├── engine/
│   │   └── scorer.py         # Cosine similarity scoring
│   │
│   ├── database/
│   │   ├── db_config.py
│   │   └── db_operations.py  # Insert/retrieve candidates and JDs
│   │
│   ├── automation/
│   │   └── ranker.py         # Generate final ranking CSV
│   │
│   └── app.py                # Main pipeline entry point
│
├── sql/
│   └── schema.sql            # Database schema
│
├── utils/
│   └── logger.py             # Simple logging wrapper
│
├── requirements.txt
└── output/
    └── ranked_candidates.csv # Generated after running the app
```

## Installation

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Place resume PDF files in `data/resumes/`.
2. Place a job description text file (e.g. `jd.txt`) in `data/jd/`.
3. Run the main application from the project root:

```bash
python -m src.app
```

This will:

- Load the job description from `data/jd/` (first `.txt` file found).
- Parse and clean each PDF resume in `data/resumes/`.
- Extract skills and estimate experience.
- Vectorize resumes and JD using TF-IDF.
- Compute cosine similarity scores.
- Store candidates and scores in a SQLite DB file `resume_screening.db`.
- Export `output/ranked_candidates.csv` sorted by score (descending).

## Notes

- The implementation uses TF-IDF by default for simplicity and reliability.
- You can later extend `vectorizer.py` to plug in Sentence-BERT embeddings.
- OCR for image-based PDFs can be added on top of `pdf_reader.py` using Tesseract if needed.
