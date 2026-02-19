from fastapi import FastAPI, UploadFile
import shutil
import os
import uuid

from parser import parse_vcf
from rules_engine import evaluate
from llm import generate_explanation
from pdf_report import generate_pdf

app = FastAPI()

from fastapi.responses import JSONResponse
import base64

@app.post("/analyze")
async def analyze(drug: str, file: UploadFile):

    temp_vcf_path = f"temp_{uuid.uuid4().hex}.vcf"

    with open(temp_vcf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    variants = parse_vcf(temp_vcf_path)
    result = evaluate(drug, variants)

    explanation = None
    if result.get("gene"):
        explanation = generate_explanation(
            drug,
            result.get("gene"),
            result.get("phenotype"),
        )

    # Generate PDF
    pdf_filename = f"report_{uuid.uuid4().hex}.pdf"
    generate_pdf(
        {
            "drug": drug,
            "result": result,
            "explanation": explanation,
        },
        file_path=pdf_filename,
    )

    # Read PDF as bytes
    with open(pdf_filename, "rb") as f:
        pdf_bytes = f.read()

    # Encode to base64 so JSON can carry it
    encoded_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    # Cleanup temp files
    os.remove(temp_vcf_path)
    os.remove(pdf_filename)

    return {
        "drug": drug,
        "result": result,
        "confidence": result.get("confidence", 0),
        "explanation": explanation,
        "pdf_base64": encoded_pdf,
    }
