from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_explanation(drug, gene, phenotype):

    prompt = f"""
Explain pharmacogenomic impact:

Drug: {drug}
Gene: {gene}
Phenotype: {phenotype}

Include:
- Mechanism
- Clinical impact
- Recommendation
Keep concise.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            timeout=10
        )

        return response.choices[0].message.content

    except Exception:
        return f"""
This patient has {phenotype} status for {gene}.
This affects how {drug} is metabolized.
Recommendation: {phenotype}.
"""
