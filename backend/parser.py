from cyvcf2 import VCF

TARGET_GENES = [
    "CYP2D6",
    "CYP2C19",
    "CYP2C9",
    "SLCO1B1",
    "TPMT",
    "DPYD"
]

def parse_vcf(file_path):
    extracted = []

    try:
        vcf = VCF(file_path)
    except Exception as e:
        raise Exception(f"Invalid VCF file: {str(e)}")

    for variant in vcf:
        try:
            gene = variant.INFO.get("GENE")
            star = variant.INFO.get("STAR")

            if gene in TARGET_GENES:
                extracted.append({
                    "gene": gene,
                    "rsid": variant.ID,
                    "star": star
                })

        except Exception:
            continue

    return extracted
