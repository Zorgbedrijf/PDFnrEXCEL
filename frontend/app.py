# File: frontend/app.py
# Doel: Streamlit frontend waarmee gebruikers een medicatie-PDF kunnen uploaden, laten verwerken en het resultaat als Excel kunnen downloaden.

try:
    import streamlit as st
except ImportError:
    raise ImportError("Streamlit is niet geïnstalleerd. Voeg 'streamlit' toe aan requirements.txt of installeer met 'pip install streamlit'.")
try:
    import pandas as pd
except ImportError:
    raise ImportError("Pandas is niet geïnstalleerd. Voeg 'pandas' toe aan requirements.txt of installeer met 'pip install pandas'.")
try:
    import fitz  # PyMuPDF
except ImportError:
    raise ImportError("PyMuPDF (fitz) is niet geïnstalleerd. Voeg 'PyMuPDF' toe aan requirements.txt of installeer met 'pip install PyMuPDF'.")
import re
import io

def parse_medication_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    data = []
    debug_info = []
    current_patient = None
    current_room = None

    for page_num, page in enumerate(doc):
        text = page.get_text()
        lines = text.split("\n")
        debug_info.append(f"Page {page_num + 1}: {len(lines)} lines")
        
        # Add debug info for first 20 lines
        if page_num == 0:  # Only for first page
            for i, line in enumerate(lines[:20]):
                if line.strip():
                    debug_info.append(f"Line {i+1}: '{line.strip()}'")
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue

            # Try multiple patient patterns
            # Pattern 1: Name (Kamer 123)
            match = re.match(r"^(.*?)\s+\(Kamer\s+(\d+)\)", line)
            if not match:
                # Pattern 2: Name - Room 123
                match = re.match(r"^(.*?)\s*-\s*(?:Room|Kamer)\s+(\d+)", line, re.IGNORECASE)
            if not match:
                # Pattern 3: Just look for room numbers
                match = re.match(r"^(.*?)\s+(\d+)$", line)
                if match and len(match.group(2)) <= 3:  # Room numbers are typically 1-3 digits
                    pass
                else:
                    match = None
            
            if match:
                current_patient = match.group(1).strip()
                current_room = match.group(2).strip()
                debug_info.append(f"Found patient: '{current_patient}' in room: '{current_room}'")
                i += 1
                continue

            # Try multiple medication patterns
            # Pattern 1: Original pattern
            med_match = re.match(r"^(.*?)\s+(\d+\s*[xX]?.*?)\s+(\d+(?:\.\d+)?)\s+om\s+(\d{2}:\d{2})", line)
            
            # Pattern 2: Medication name + dosage + time (more flexible)
            if not med_match:
                med_match = re.match(r"^(.*?)\s+(\d+(?:\.\d+)?(?:\s*mg|ml|g)?)\s+(\d{1,2}:\d{2})", line)
                if med_match:
                    # Restructure to match expected format
                    medication = med_match.group(1).strip()
                    dose = med_match.group(2).strip()
                    time = med_match.group(3).strip()
                    med_match = type('Match', (), {
                        'group': lambda self, n: [None, medication, "", dose, time][n]
                    })()
            
            # Pattern 3: Just medication name and time
            if not med_match:
                med_match = re.match(r"^(.*?)\s+(\d{1,2}:\d{2})", line)
                if med_match:
                    medication = med_match.group(1).strip()
                    time = med_match.group(2).strip()
                    med_match = type('Match', (), {
                        'group': lambda self, n: [None, medication, "", "", time][n]
                    })()
            
            if med_match:
                medication = med_match.group(1).strip()
                dose_info = med_match.group(2).strip() if len(med_match.group(2)) > 0 else ""
                dose = med_match.group(3).strip() if len(med_match.group(3)) > 0 else ""
                time = med_match.group(4).strip()
                
                debug_info.append(f"Found medication: '{medication}' at time: '{time}'")
                
                who = ""
                when = ""
                note = ""

                # Look for additional metadata in following lines
                j = i + 1
                while j < len(lines) and j < i + 5:  # Look at next 5 lines max
                    meta_line = lines[j].strip()
                    if not meta_line:
                        break
                    if meta_line.startswith("Wie:"):
                        who = meta_line.replace("Wie:", "").strip()
                    elif meta_line.startswith("Wanneer:"):
                        when = meta_line.replace("Wanneer:", "").strip()
                    elif meta_line.startswith("Dosis:"):
                        dose = meta_line.replace("Dosis:", "").strip()
                    elif meta_line.startswith("Opmerking:"):
                        note = meta_line.replace("Opmerking:", "").strip()
                    elif re.match(r"^[A-Z].*:", meta_line):  # Any field starting with capital letter and colon
                        # Generic field handler
                        field_name, field_value = meta_line.split(":", 1)
                        if "wie" in field_name.lower():
                            who = field_value.strip()
                        elif "wanneer" in field_name.lower() or "when" in field_name.lower():
                            when = field_value.strip()
                        elif "dosis" in field_name.lower() or "dose" in field_name.lower():
                            dose = field_value.strip()
                        elif "opmerking" in field_name.lower() or "note" in field_name.lower():
                            note = field_value.strip()
                    j += 1

                data.append({
                    "Patiënt": current_patient or "Onbekend",
                    "Kamer": current_room or "Onbekend",
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

    # Create DataFrame and add debug info
    df = pd.DataFrame(data)
    return df, debug_info

# Streamlit interface
st.set_page_config(page_title="PDF naar Excel Converter", layout="centered")
st.title("💊 Medicatie PDF naar Excel")

uploaded_files = st.file_uploader("📄 Upload één of meerdere medicatie PDF-bestanden", type="pdf", accept_multiple_files=True)

if uploaded_files:
    all_debug = []
    found_any = False
    for uploaded_file in uploaded_files:
        with st.spinner(f'PDF "{uploaded_file.name}" wordt verwerkt...'):
            df, debug_info = parse_medication_pdf(uploaded_file)
        st.markdown(f"### Bestand: `{uploaded_file.name}`")
        if len(df) > 0:
            found_any = True
            st.success(f"✅ {len(df)} medicatie items gevonden in {uploaded_file.name}.")
            st.dataframe(df, use_container_width=True)
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            excel_buffer.seek(0)
            st.download_button(
                label=f"📥 Download Excel voor {uploaded_file.name}",
                data=excel_buffer.getvalue(),
                file_name=f"{uploaded_file.name.replace('.pdf','')}_medicatie.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning(f"⚠️ Geen medicatie gegevens gevonden in {uploaded_file.name}.")
        with st.expander(f"🔍 Debug info voor {uploaded_file.name}", expanded=False):
            st.write("**PDF parsing debug informatie:**")
            for info in debug_info:
                st.text(info)
    if not found_any:
        st.warning("⚠️ Geen medicatie gegevens gevonden in de PDF(s).")
