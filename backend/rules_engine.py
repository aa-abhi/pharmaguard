import json

with open("rules.json") as f:
    PHENOTYPE_MAP = json.load(f)

DRUG_RULES = {
    "Codeine": {
        "genes": ["CYP2D6"],
        "risk_if": "Poor metabolizer",
        "result": "Ineffective"
    },
    "Warfarin": {
        "genes": ["CYP2C9"],
        "risk_if": "Poor metabolizer",
        "result": "Reduce dose"
    },
    "Simvastatin": {
        "genes": ["SLCO1B1"],
        "risk_if": "High toxicity risk",
        "result": "Toxic risk"
    }
}

def evaluate(drug, variants):
    if drug not in DRUG_RULES:
        return {
            "recommendation": "Unknown drug",
            "confidence": 0
        }

    rule = DRUG_RULES[drug]
    required_genes = rule["genes"]

    found_genes = 0
    phenotype_result = None

    for gene in required_genes:
        for v in variants:
            if v["gene"] == gene:
                found_genes += 1
                star = v.get("star")
                phenotype = PHENOTYPE_MAP.get(gene, {}).get(star)

                if phenotype == rule["risk_if"]:
                    phenotype_result = phenotype
                    recommendation = rule["result"]
                    break
                elif phenotype:
                    phenotype_result = phenotype
                    recommendation = "Safe"
                else:
                    recommendation = "Unknown risk"

    confidence = round(found_genes / len(required_genes), 2)

    if found_genes == 0:
        return {
            "recommendation": "Unknown risk (gene not found)",
            "confidence": 0
        }

    return {
        "gene": gene,
        "phenotype": phenotype_result,
        "recommendation": recommendation,
        "confidence": confidence
    }
