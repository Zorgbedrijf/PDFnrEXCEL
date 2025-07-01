# File: backend/parser.py
# Doel: Deze module leest de medicatie PDF en exporteert de gegevens direct naar een Excel-bestand.

import fitz  # PyMuPDF
import re
import pandas as pd
import os

def parse_medication_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    data = []
    current_patient = None
    current_room = None

    for page in doc:
        lines = page.get_text().split("\n")
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            match = re.match(r"^(.*?)\s+\(Kamer\s+(\d+)\)", line)
            if match:
                current_patient = match.group(1).strip()
                current_room = match.group(2).strip()
                i += 1
                continue

            med_match = re.match(r"^(.*?)\s+(\d+\s*[xX]?.*?)\s+(\d+(?:\.\d+)?)\s+om\s+(\d{2}:\d{2})", line)
            if med_match:
                medication = med_match.group(1).strip()
                dose = med_match.group(3).strip()
                time = med_match.group(4).strip()
                who = ""
                when = ""
                note = ""

                j = i + 1
                while j < len(lines):
                    meta_line = lines[j].strip()
                    if meta_line.startswith("Wie:"):
                        who = meta_line.replace("Wie:", "").strip()
                    elif meta_line.startswith("Wanneer:"):
                        when = meta_line.replace("Wanneer:", "").strip()
                    elif meta_line.startswith("Dosis:"):
                        dose = meta_line.replace("Dosis:", "").strip()
                    elif meta_line.startswith("Opmerking:"):
                        note = meta_line.replace("Opmerking:", "").strip()
                    elif meta_line == "":
                        break
                    j += 1

                data.append({
                    "Patiënt": current_patient,
                    "Kamer": current_room,
                    "Medicatie": medication,
                    "Tijdstip": time,
                    "Dosis": dose,
                    "Wie": who,
                    "Wanneer": when,
                    "Opmerking": note
                })
                i = j
            else:
                i += 1

    return pd.DataFrame(data)

if __name__ == "__main__":
    os.makedirs("data/output", exist_ok=True)
    df = parse_medication_pdf("2025-06-30T13_50_06+02_00_medication-tasks-report.pdf")
    df.to_excel("data/output/medicatie_export.xlsx", index=False)
    print("✅ Excel-bestand succesvol aangemaakt: data/output/medicatie_export.xlsx")
