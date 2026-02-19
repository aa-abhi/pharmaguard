## 🧬 PharmaGuard – AI-Powered Precision Medicine Risk Analyzer

PharmaGuard is a **pharmacogenomics web application** that analyzes patient genetic data (VCF files) to predict **drug safety, efficacy, and toxicity risks**.

It combines **rule-based pharmacogenomic evaluation** with **AI-generated clinical explanations** to assist in safer medication decisions.

---

### Key Features

- VCF genetic file parsing  
- Gene → Phenotype mapping  
- Drug-specific pharmacogenomic risk engine  
- Confidence scoring mechanism  
- AI-powered clinical explanation (OpenAI)  
- Downloadable structured PDF clinical reports  
- Clean interactive Streamlit UI  
- FastAPI backend architecture  

### Supported Genes

- **CYP2D6**
- **CYP2C19**
- **CYP2C9**
- **SLCO1B1**
- **TPMT**
- **DPYD**

### Supported Drugs

- **Codeine**
- **Warfarin**
- **Simvastatin**
- **Clopidogrel**
- **Azathioprine**
- **Fluorouracil**

### Architecture
```
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
```

### Project Structure
```
pharmaguard/
│
├── backend/
│ ├── main.py
│ ├── parser.py
│ ├── rules_engine.py
│ ├── llm.py
│ ├── pdf_report.py
│ ├── rules.json
│ └── schema.py
│
├── frontend/
│ └── app.py
│
├── sample_vcf/
│ ├── patient_codeine_normal.vcf
│ ├── patient_codeine_poor.vcf
│ ├── patient_simvastatin_toxic.vcf
│ ├── patient_warfarin_adjust.vcf
│ └── unknown_risk.vcf
│
└── README.md
```
## How To Run On Your PC

Follow these steps exactly.


### 1. Clone The Repository
```
git clone <your-repo-url>
cd pharmaguard
```

### 2. Create Virtual Environment

##### From project root:

```python -m venv .venv```

Activate

##### Mac/Linux

```source .venv/bin/activate```

##### Windows

```.venv\Scripts\activate```

### 3. Install Dependencies

```pip install -r requirements.txt```

### 4. Set OpenAI API Key (For LLM Explanation)

##### Mac/Linux

```export OPENAI_API_KEY=your_api_key_here```

##### Windows

```setx OPENAI_API_KEY "your_api_key_here"```

#### Restart terminal after setting.

If API key is not set, fallback explanation will be used.

### 5. Start Backend Server
cd backend
python -m uvicorn main:app --reload

You should see:

Uvicorn running on http://127.0.0.1:8000

### 5. Start Frontend

Open a new terminal.

Activate venv again:

source .venv/bin/activate

Then:

cd frontend
streamlit run app.py

Application will open at:

http://localhost:8501

### Testing With Sample Files

Use files inside sample_vcf/.
```
Recommended Demo Order
File	Expected Result
patient_codeine_normal.vcf	🟢 Safe
patient_codeine_poor.vcf	🔴 Ineffective
patient_warfarin_adjust.vcf	🟡 Dose Adjustment
patient_simvastatin_toxic.vcf	🔴 Toxic Risk
unknown_risk.vcf	⚪ Unknown Risk
```
### Features Overview
```
✔ VCF parsing using cyvcf2
✔ STAR allele extraction
✔ Gene → phenotype mapping
✔ Drug-specific rule engine
✔ Confidence score calculation
✔ LLM-based clinical explanation
✔ Clinical PDF report generation
✔ JSON report download
✔ Streamlit interactive UI
```
### 🔒 Confidence Score Logic
```
Confidence =
(number of required genes found in VCF)
÷
(number of genes required for that drug)
```
Example

Required gene present → 100%

Missing gene → 0%

### PDF Report Includes
```
Risk severity banner
Structured drug assessment table
Genetic findings section
Clinical interpretation
Timestamp
Clinical disclaimer
```
### ⚠ Known Warnings

You may see VCF contig warnings like:

Contig '22' is not defined in the header

These are harmless and occur when dummy VCF files omit full contig metadata.

#### 🧠 Tech Stack

##### Backend

- FastAPI
- Python
- cyvcf2
- ReportLab
- OpenAI API

##### Frontend
- Streamlit
