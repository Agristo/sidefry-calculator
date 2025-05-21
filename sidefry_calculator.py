import streamlit as st
import pandas as pd

st.title("SideFry™ Interactieve Cost & Margin Calculator")

BAG_WEIGHT = 2500  # gram

producten = [
    "Super Crispy straight cut fries",
    "Super Crispy SIDEWINDERS fries",
    "Super Crispy seasoned waffle cut fries - skin on",
    "Super Crispy crinkle cut fries",
    "Crispy dippers",
    "Mini hash browns",
    "SmartChef mashed potatoes"
]

defaults = {
    "Super Crispy straight cut fries":       {"portion_weight": 200, "cost_bag": 6.25, "selling_price": 5.00, "bags_month": 10},
    "Super Crispy SIDEWINDERS fries":        {"portion_weight": 120, "cost_bag": 8.21, "selling_price": 6.00, "bags_month": 2},
    "Super Crispy seasoned waffle cut fries - skin on": {"portion_weight": 160, "cost_bag": 7.08, "selling_price": 6.00, "bags_month": 0},
    "Super Crispy crinkle cut fries":        {"portion_weight": 190, "cost_bag": 7.00, "selling_price": 6.00, "bags_month": 0},
    "Crispy dippers":                        {"portion_weight": 150, "cost_bag": 5.55, "selling_price": 6.00, "bags_month": 1},
    "Mini hash browns":                      {"portion_weight": 190, "cost_bag": 8.05, "selling_price": 6.00, "bags_month": 0},
    "SmartChef mashed potatoes":             {"portion_weight": 160, "cost_bag": 5.79, "selling_price": 6.00, "bags_month": 0},
}

st.write("Pas per product de parameters aan. De calculator rekent alle marges direct uit.")

results = []
standard_margin = 0
sidefry_margin = 0

for prod in producten:
    st.markdown(f"#### {prod}")
    cols = st.columns([1.2, 1.2, 1.5, 1, 1.5])
    portion_weight = cols[0].number_input(f"Weight/portion (g)", min_value=50, max_value=500, value=defaults[prod]["portion_weight"], step=10, key=f"weight_{prod}")
    cost_bag = cols[1].number_input(f"Cost/bag (€)", min_value=1.0, max_value=20.0, value=float(defaults[prod]["cost_bag"]), step=0.01, key=f"cost_{prod}")
    selling_price = cols[2].number_input(f"Advised selling price/portion (€)", min_value=1.0, max_value=15.0, value=float(defaults[prod]["selling_price"]), step=0.10, key=f"sell_{prod}")
    bags_month = cols[3].number_input(f"Bags sold/month", min_value=0, max_value=100, value=int(defaults[prod]["bags_month"]), step=1, key=f"bags_{prod}")

    portions_per_bag = BAG_WEIGHT / portion_weight
    foodcost_per_portion = cost_bag / portions_per_bag
    margin_per_portion = selling_price - foodcost_per_portion
    margin_per_bag = margin_per_portion * portions_per_bag
    margin_month = margin_per_bag * bags_month

    # KPI direct rechts tonen
    cols[4].markdown(f"<div style='font-size:18px;font-weight:bold;color:#388e3c;'>Margin/month:<br>€{margin_month:,.2f}</div>", unsafe_allow_html=True)

    # Alleen relevante info in het overzicht hieronder
    with st.expander("Details & Berekeningen", expanded=False):
        st.write(f"- **Portions per bag:** {portions_per_bag:.2f}")
        st.write(f"- **Foodcost per portion:** €{foodcost_per_portion:.3f}")
        st.write(f"- **Margin per portion:** €{margin_per_portion:.3f}")
        st.write(f"- **Margin per bag:** €{margin_per_bag:.2f}")

    results.append({
        "Product": prod,
        "Margin per month (€)": margin_month
    })

    # Voor scenario-berekening
    if prod == "Super Crispy straight cut fries":
        standard_margin += margin_month
    else:
        sidefry_margin += margin_month

total_margin = standard_margin + sidefry_margin

st.markdown("---")
st.subheader("Vergelijking: standaard vs. SideFry assortiment")
col1, col2, col3 = st.columns(3)
col1.metric("Enkel standaard", f"€{standard_margin:,.2f}/maand")
col2.metric("Alle extra SideFry producten", f"€{sidefry_margin:,.2f}/maand")
col3.metric("EXTRA margin door SideFry assortiment", f"€{sidefry_margin:,.2f}/maand")

st.markdown("---")
st.subheader("Overzichtsmarge per product")
st.dataframe(pd.DataFrame(results).set_index("Product"))
