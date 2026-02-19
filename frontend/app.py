import streamlit as st
import requests
import json
import base64

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="PharmaGuard", layout="centered")

st.markdown("""
<style>
.big-title {
    font-size: 34px;
    font-weight: 700;
}
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

drug = st.selectbox(
    "Select Drug",
    ["Codeine", "Warfarin", "Simvastatin",
     "Clopidogrel", "Azathioprine", "Fluorouracil"]
)

uploaded_file = st.file_uploader("Upload VCF File", type=["vcf"])

if st.button("Analyze"):

    if not uploaded_file:
        st.error("Please upload a VCF file.")
        st.stop()

    files = {
        "file": (uploaded_file.name, uploaded_file.getvalue(), "text/plain")
    }

    with st.spinner("Analyzing genetic profile..."):
        response = requests.post(API_URL, files=files, params={"drug": drug})

    data = response.json()
    result = data.get("result", {})
    recommendation = result.get("recommendation", "Unknown")
    confidence = result.get("confidence", 0)

    st.markdown("---")

    # Risk Card
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if "Safe" in recommendation:
        st.markdown(f'<div class="risk-green">🟢 {recommendation}</div>', unsafe_allow_html=True)
    elif "Reduce" in recommendation or "Adjust" in recommendation:
        st.markdown(f'<div class="risk-yellow">🟡 {recommendation}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="risk-red">🔴 {recommendation}</div>', unsafe_allow_html=True)

    st.progress(confidence)
    st.write(f"Confidence Score: {int(confidence*100)}%")

    st.markdown('</div>', unsafe_allow_html=True)

    # Genetic Findings
    if result.get("gene"):
        st.markdown("### 🧬 Genetic Findings")
        st.write(f"**Gene:** {result.get('gene')}")
        st.write(f"**Phenotype:** {result.get('phenotype')}")

    # Explanation
    if data.get("explanation"):
        st.markdown("### 📘 Clinical Explanation")
        st.write(data["explanation"])

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "Download JSON Report",
            data=json.dumps(data, indent=2),
            file_name="pharmaguard_result.json",
            mime="application/json"
        )

    with col2:
        if data.get("pdf_base64"):
            pdf_bytes = base64.b64decode(data["pdf_base64"])
            st.download_button(
                "Download Clinical PDF",
                data=pdf_bytes,
                file_name="pharmaguard_report.pdf",
                mime="application/pdf"
            )
