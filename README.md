# NLP-Based Resume Screening and Ranking System

## 📌 Overview
This project automates resume screening by using **Natural Language Processing (NLP)** and **machine learning–based text similarity** to match candidate resumes with a job description. It objectively scores and ranks resumes, reducing manual effort and improving hiring efficiency.

---

## ⚙️ How It Works
- Reads a job description and extracts required skills.
- Converts resume PDFs into text and cleans the data.
- Extracts candidate skills, experience, and contact details.
- Uses **TF-IDF** vectorization and **cosine similarity** to compute match scores.
- Stores results in an **SQLite database**.
- Exports ranked candidates as a **CSV file**.

---

## 🛠️ Tech Stack
- **Language:** Python  
- **NLP / ML:** TF-IDF, Cosine Similarity (Scikit-learn)  
- **Text Processing:** Regex, custom cleaning pipeline  
- **Database:** SQLite  
- **Data Handling:** Pandas  
- **PDF Parsing:** PyPDF2  

---

## ✅ Key Features
- Automated resume screening
- Objective, data-driven ranking
- Modular and scalable design
- Recruiter-friendly CSV output

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
