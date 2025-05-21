import streamlit as st

st.title("SideFry™ Omzet Calculator")

# Inputvelden voor de gebruiker
aantal_gasten = st.number_input("Aantal gasten per dag", min_value=0, value=100)
gemiddelde_prijs_side = st.number_input("Gemiddelde prijs per side (€)", min_value=0.0, value=3.5, step=0.1)
extra_sides_per_gast = st.number_input("Gemiddeld aantal extra sides per gast", min_value=0.0, value=0.4, step=0.1)
dagen_per_jaar = st.number_input("Aantal dagen open per jaar", min_value=1, value=300)

# Simpele omzetformule
extra_omzet_per_dag = aantal_gasten * gemiddelde_prijs_side * extra_sides_per_gast
extra_omzet_per_jaar = extra_omzet_per_dag * dagen_per_jaar

# Resultaat tonen
st.subheader("Resultaat")
st.write(f"**Extra omzet per dag:** €{extra_omzet_per_dag:,.2f}")
st.write(f"**Extra omzet per jaar:** €{extra_omzet_per_jaar:,.2f}")

# Optioneel: grafiekje van de jaaromzet bij verschillende aantallen extra sides
import matplotlib.pyplot as plt
import numpy as np

extra_sides_range = np.linspace(0, 1, 11)
yearly_revenue = aantal_gasten * gemiddelde_prijs_side * extra_sides_range * dagen_per_jaar

fig, ax = plt.subplots()
ax.plot(extra_sides_range, yearly_revenue, marker='o')
ax.set_xlabel("Gemiddeld aantal extra sides per gast")
ax.set_ylabel("Extra omzet per jaar (€)")
ax.set_title("Impact van extra sides op jaaromzet")
st.pyplot(fig)
