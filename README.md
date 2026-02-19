🧬 PharmaGuard – Precision Medicine Risk Analyzer

PharmaGuard is an AI-powered pharmacogenomics web application that analyzes a patient's genetic VCF file and predicts how they will respond to specific medications.

It combines:

VCF variant parsing

Gene → phenotype mapping

Rule-based drug risk engine

AI-generated clinical explanations

Confidence scoring

Downloadable clinical PDF reports

🚀 What Problem Does It Solve?

Drug response varies due to genetic differences.

PharmaGuard helps determine whether a drug is:

🟢 Safe

🟡 Requires dose adjustment

🔴 Ineffective

🔴 Toxic risk

Based on curated pharmacogenomic logic aligned with CPIC-style guidelines.

🏗 Architecture

Frontend (Streamlit)
↓
Backend API (FastAPI)
↓
VCF Parser → Variant Extractor → Rule Engine
↓
LLM Clinical Explanation Generator
↓
Confidence Scoring
↓
PDF Report Generator

📂 Project Structure
pharmaguard/
│
├── backend/
│   ├── main.py
│   ├── parser.py
│   ├── rules_engine.py
│   ├── llm.py
│   ├── pdf_report.py
│   ├── rules.json
│   └── schema.py
│
├── frontend/
│   └── app.py
│
├── sample_vcf/
│   ├── patient_codeine_normal.vcf
│   ├── patient_codeine_poor.vcf
│   ├── patient_simvastatin_toxic.vcf
│   ├── patient_warfarin_adjust.vcf
│   └── unknown_risk.vcf
│
└── README.md

⚙️ How To Run On Your PC

Follow these steps exactly.

1️⃣ Clone The Repository
git clone <your-repo-url>
cd pharmaguard

2️⃣ Create Virtual Environment

From project root:

python -m venv .venv


Activate:

Mac/Linux:

source .venv/bin/activate


Windows:

.venv\Scripts\activate

3️⃣ Install Backend Dependencies
pip install fastapi uvicorn cyvcf2 openai reportlab python-multipart streamlit requests


Optional:

pip install -r requirements.txt

4️⃣ Set OpenAI API Key (For LLM Explanation)

Mac/Linux:

export OPENAI_API_KEY=your_api_key_here


Windows:

setx OPENAI_API_KEY "your_api_key_here"


Restart terminal after setting.

If API key is not set, fallback explanation will be used.

5️⃣ Start Backend Server

Go to backend folder:

cd backend


Run:

python -m uvicorn main:app --reload


You should see:

Uvicorn running on http://127.0.0.1:8000

6️⃣ Start Frontend

Open new terminal.

Activate venv again:

source .venv/bin/activate


Go to frontend:

cd frontend


Run:

streamlit run app.py


It will open:

http://localhost:8501

🧪 Testing With Sample Files

Use files inside sample_vcf/.

Recommended demo order:

File	Expected Result
patient_codeine_normal.vcf	Safe
patient_codeine_poor.vcf	Ineffective
patient_warfarin_adjust.vcf	Dose Adjustment
patient_simvastatin_toxic.vcf	Toxic Risk
unknown_risk.vcf	Unknown Risk
📊 Features

✔ VCF parsing using cyvcf2
✔ STAR allele extraction
✔ Gene → phenotype mapping
✔ Drug-specific rule engine
✔ Confidence score calculation
✔ LLM-based clinical explanation
✔ Clinical PDF report generation
✔ JSON report download
✔ Streamlit interactive UI

🔒 Confidence Score Logic

Confidence =
(number of required genes found in VCF)
÷
(number of genes required for that drug)

Example:

Required gene present → 100%

Missing gene → 0%

📄 PDF Report Includes

Risk severity banner

Drug assessment table

Genetic findings

Clinical interpretation

Timestamp

Clinical disclaimer

⚠ Known Warnings

You may see VCF contig warnings:

Contig '22' is not defined in the header


These are harmless and occur when dummy VCF files omit full contig metadata.

💡 Future Improvements

Multi-gene drug logic (e.g., CYP2C9 + VKORC1 for Warfarin)

Patient ID input

CPIC reference linking

Deployment on Render + Streamlit Cloud

Authentication layer

Batch patient analysis mode

🧠 Tech Stack

Backend:

FastAPI

Python

cyvcf2

ReportLab

OpenAI API

Frontend:

Streamlit