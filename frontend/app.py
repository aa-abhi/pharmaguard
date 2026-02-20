import streamlit as st
import requests
import json
import base64
import os

# ---------- Secrets Handling ----------
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    api_key = os.getenv("OPENAI_API_KEY")

try:
    backend_url = st.secrets["BACKEND_URL"]
except Exception:
    backend_url = "http://127.0.0.1:8000"  # fallback for local

if not api_key:
    st.error("OPENAI_API_KEY not configured.")
    st.stop()

if not backend_url.startswith("http"):
    st.error("Invalid BACKEND_URL in secrets.")
    st.stop()

# Normalize backend URL (prevent double slash issues)
backend_url = backend_url.rstrip("/")
API_URL = f"{backend_url}/analyze"

# ---------- Page Config ----------
st.set_page_config(page_title="PharmaGuard", layout="centered")

st.markdown("""
<style>
.big-title { font-size: 34px; font-weight: 700; }
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #f8f9fa;
    margin-bottom: 20px;
}
.risk-red {color: #d9534f; font-weight: 600;}
.risk-yellow {color: #f0ad4e; font-weight: 600;}
.risk-green {color: #5cb85c; font-weight: 600;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">🧬 PharmaGuard</div>', unsafe_allow_html=True)
st.caption("AI-Powered Precision Medicine Risk Analyzer")

# ---------- UI ----------
drug = st.selectbox(
    "Select Drug",
    ["Codeine", "Warfarin", "Simvastatin",
     "Clopidogrel", "Azathioprine", "Fluorouracil"]
)

uploaded_file = st.file_uploader("Upload VCF File", type=["vcf"])

# ---------- Analyze ----------
if st.button("Analyze"):

    if not uploaded_file:
        st.error("Please upload a VCF file.")
        st.stop()

    files = {
        "file": (uploaded_file.name, uploaded_file.getvalue(), "text/plain")
    }

    with st.spinner("Analyzing genetic profile..."):
        try:
            response = requests.post(
                API_URL,
                files=files,
                params={"drug": drug},
                timeout=60
            )
        except requests.exceptions.RequestException as e:
            st.error("Backend connection failed.")
            st.write(str(e))
            st.stop()

    if response.status_code != 200:
        st.error(f"Backend error: {response.status_code}")
        st.write(response.text)
        st.stop()

    try:
        data = response.json()
    except Exception:
        st.error("Invalid JSON returned from backend.")
        st.stop()

    result = data.get("result", {})
    recommendation = result.get("recommendation", "Unknown")

    try:
        confidence = float(result.get("confidence", 0))
    except (TypeError, ValueError):
        confidence = 0

    confidence = max(0, min(confidence, 1))

    st.markdown("---")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if "Safe" in recommendation:
        st.markdown(f'<div class="risk-green">🟢 {recommendation}</div>', unsafe_allow_html=True)
    elif "Reduce" in recommendation or "Adjust" in recommendation:
        st.markdown(f'<div class="risk-yellow">🟡 {recommendation}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="risk-red">🔴 {recommendation}</div>', unsafe_allow_html=True)

    st.progress(confidence)
    st.write(f"Confidence Score: {int(confidence * 100)}%")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- Genetic Findings ----------
    if result.get("gene"):
        st.markdown("### 🧬 Genetic Findings")
        st.write(f"**Gene:** {result.get('gene')}")
        st.write(f"**Phenotype:** {result.get('phenotype')}")

    # ---------- Explanation ----------
    if data.get("explanation"):
        st.markdown("### 📘 Clinical Explanation")
        st.write(data["explanation"])

    st.markdown("---")

    col1, col2 = st.columns(2)

    # ---------- Download JSON ----------
    with col1:
        st.download_button(
            "Download JSON Report",
            data=json.dumps(data, indent=2),
            file_name="pharmaguard_result.json",
            mime="application/json"
        )

    # ---------- Download PDF ----------
    with col2:
        if data.get("pdf_base64"):
            try:
                pdf_bytes = base64.b64decode(data["pdf_base64"])
                st.download_button(
                    "Download Clinical PDF",
                    data=pdf_bytes,
                    file_name="pharmaguard_report.pdf",
                    mime="application/pdf"
                )
            except Exception:
                st.error("Failed to decode PDF.")
