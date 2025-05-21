import streamlit as st
from fpdf import FPDF
import tempfile

# --- LOGO (public link) ---
st.markdown(
    """
    <div style="display:flex; justify-content:center; align-items:center; margin-bottom:8px;">
        <img src="https://jobs.agristo.com/storage/attachments/9ef6eba7-7f0f-40d3-8493-bc07ac70ce56/agristo-logo-bya-forwhitebg-full-color-rgb-900px-w-72ppi.jpg" width="340">
    </div>
    """, unsafe_allow_html=True,
)

AGRISTO_YELLOW = "#FFC20F"
AGRISTO_BLACK = "#000000"
BAG_WEIGHT = 2500  # grams

# CSS for yellow accents, etc. [omitted for brevity, zie vorige code]

def product_input(product, defaults, key_suffix=""):
    # ... zelfde als vorige code ...
    # returns margin_month, stores summary info for PDF
    pass  # Vervang door de echte inhoud uit vorige code!

# ... Je bestaande layout en berekeningen ...

# --- CTA ZONE ONDERAAN ---
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align:center; margin-top:20px;'>
        <h2 style='color:{AGRISTO_BLACK}; font-size:1.3em;'>Ready to turn these numbers into real profit? <br>Let’s talk SideFry™!</h2>
    </div>
    """, unsafe_allow_html=True
)

cols = st.columns([2, 1, 2])
with cols[1]:
    # Contact button
    mailto_link = "mailto:sales@agristo.com?subject=SideFry%20calculator%20results"
    contact_btn = st.markdown(
        f"""
        <a href="{mailto_link}" target="_blank" style="
            display:inline-block;
            background-color:{AGRISTO_YELLOW};
            color:{AGRISTO_BLACK};
            font-weight:bold;
            border:none;
            padding:14px 38px;
            border-radius:10px;
            font-size:17px;
            text-decoration:none;
            margin:4px;">
            Contact our sales team
        </a>
        """, unsafe_allow_html=True
    )

    # Download PDF knop
    if st.button("Download your calculation", key="download_calc"):
        # Vul deze dict aan met jouw echte resultaten
        results_for_pdf = {
            "Standard Only (€/month)": "xxx",  # <-- vul in met echte waarde
            "Standard + SideFry™ (€/month)": "yyy",  # idem
            "EXTRA margin (€/month)": "zzz",  # idem
        }

        # PDF genereren
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, "SideFry™ Calculation Results", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        for key, value in results_for_pdf.items():
            pdf.cell(0, 10, f"{key}: {value}", ln=True)
        # Bewaren en downloaden
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf.output(tmp_file.name)
            st.download_button(
                label="Download PDF",
                data=open(tmp_file.name, "rb").read(),
                file_name="SideFry_Calculation.pdf",
                mime="application/pdf",
                key="pdf_download_btn"
            )

# Eventueel copy-tekst eronder:
st.markdown(
    f"<div style='text-align:center; margin-top:6px; color:{AGRISTO_BLACK}; font-size:1.01em;'>"
    f"Want to see SideFry™ in your kitchen or have questions? Our team is ready to help!"
    f"</div>",
    unsafe_allow_html=True
)
