# GenAI ClinicalBot

A Streamlit-based clinical assistant that uses Google Gemini + FAISS retrieval to analyze patient symptoms against uploaded historical case data and generate structured AI guidance.

## What This Project Does

- Accepts an Excel file (`.xlsx`) containing patient/case records
- Converts each row into text and builds embeddings
- Stores embeddings in a FAISS vector index
- Finds the closest matching case for user-provided symptoms
- Generates a structured response with:
  - Possible diagnosis
  - Initial treatment
  - Follow-up recommendations

## Tech Stack

- Python
- Streamlit
- Pandas + NumPy
- FAISS
- LangChain
- Google Gemini (`gemini-2.0-flash`)
- Google embedding model (`models/embedding-001`)

## Project Structure

```text
GenAI_ClinicalBot-master/
├── app.py
└── README.md
```

## Prerequisites

- Python 3.9+ (recommended 3.10 or newer)
- A valid Google Generative AI API key
- Internet connection (for Gemini API calls)

## Installation

### 1) Clone or open the project

```bash
git clone <your-repo-url>
cd GenAI_ClinicalBot-master
```

### 2) Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install streamlit pandas numpy faiss-cpu langchain langchain-core langchain-google-genai openpyxl
```

## Configure API Key

Set your Google API key as an environment variable before running:

Windows (PowerShell):

```powershell
$env:GOOGLE_API_KEY="your_google_api_key_here"
```

macOS/Linux:

```bash
export GOOGLE_API_KEY="your_google_api_key_here"
```

> Security note: avoid hardcoding API keys in source files. Use environment variables and rotate any exposed key immediately.

## Run the App

```bash
streamlit run app.py
```

Then open the local URL shown in terminal (usually `http://localhost:8501`).

## Expected Excel Input

The app reads each row and combines all columns into text for retrieval.  
It works best when your file includes clinically meaningful columns, for example:

- `PatientID`
- `Symptoms`
- `History`
- `Diagnosis`
- `Treatment`
- `Notes`

## Usage Flow

1. Launch the app.
2. Upload an `.xlsx` file with historical cases.
3. Enter patient symptoms in the text area.
4. Click **Find Diagnosis & Treatment**.
5. Review:
   - closest matching case
   - AI-generated structured recommendation

## Important Disclaimer

This project is for educational/research prototyping only.  
It is **not** a substitute for licensed medical judgment, diagnosis, or treatment.

## Common Issues

- `ModuleNotFoundError`: install missing package with `pip install <package-name>`
- Excel read errors: ensure file is `.xlsx` and `openpyxl` is installed
- FAISS install issues on some systems: use `faiss-cpu`
- API/auth errors: verify `GOOGLE_API_KEY` is correctly set in your active shell session

