import streamlit as st
import pandas as pd

st.title("SideFry™ Interactieve Cost & Margin Calculator")

BAG_WEIGHT = 2500  # gram

# De productenlijst
producten = [
    "Super Crispy straight cut fries",
    "Super Crispy SIDEWINDERS fries",
    "Super Crispy seasoned waffle cut fries - skin on",
    "Super Crispy crinkle cut fries",
    "Crispy dippers",
    "Mini hash browns",
    "SmartChef mashed potatoes"
]

# Defaultwaarden uit jouw sheet (pas gerust aan)
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
    st.header(prod)
    cols = st.columns(4)
    portion_weight = cols[0].number_input(f"Weight/portion (g) - {prod}", min_value=50, max_value=500, value=defaults[prod]["portion_weight"], step=10, key=f"weight_{prod}")
    cost_bag = cols[1].number_input(f"Cost/bag (€) - {prod}", min_value=1.0, max_value=20.0, value=float(defaults[prod]["cost_bag"]), step=0.01, key=f"cost_{prod}")
    selling_price = cols[2].number_input(f"Advised selling price/portion (€) - {prod}", min_value=1.0, max_value=15.0, value=float(defaults[prod]["selling_price"]), step=0.10, key=f"sell_{prod}")
    bags_month = cols[3].number_input(f"Bags sold/month - {prod}", min_value=0, max_value=100, value=int(defaults[prod]["bags_month"]), step=1, key=f"bags_{prod}")

    portions_per_bag = BAG_WEIGHT / portion_weight
    foodcost_per_portion = cost_bag / portions_per_bag
    margin_per_portion = selling_price - foodcost_per_portion
    selling_price_per_bag = selling_price * portions_per_bag
    margin_per_bag = selling_price_per_bag - cost_bag
    margin_pct = margin_per_bag / selling_price_per_bag if selling_price_per_bag else 0
    margin_month = margin_per_bag * bags_month

    # Toon de berekeningen overzichtelijk
    st.write(f"- **Portions per bag:** {portions_per_bag:.2f}")
    st.write(f"- **Foodcost per portion:** €{foodcost_per_portion:.3f}")
    st.write(f"- **Margin per portion:** €{margin_per_portion:.3f}")
    st.write(f"- **Selling price per bag:** €{selling_price_per_bag:.2f}")
    st.write(f"- **Margin per bag:** €{margin_per_bag:.2f}")
    st.write(f"- **% Margin:** {margin_pct:.2%}")
    st.write(f"- **Margin per month:** €{margin_month:.2f}")

    results.append({
        "Product": prod,
        "Margin per month (€)": margin_month
    })

    # Sommen voor scenario's
    if prod == "Super Crispy straight cut fries":
        standard_margin += margin_month
    else:
        sidefry_margin += margin_month

# Totale marge
total_margin = standard_margin + sidefry_margin

st.subheader("TOTALE MARGE PER MAAND (alle producten samen)")
st.success(f"€{total_margin:,.2f}")

st.subheader("Vergelijking: standaard vs. SideFry assortiment")
st.write(f"**Enkel standaard (Super Crispy straight cut fries):** €{standard_margin:,.2f} per maand")
st.write(f"**Alle extra SideFry producten samen:** €{sidefry_margin:,.2f} per maand")
st.write(f"**EXTRA margin door SideFry assortiment:** €{sidefry_margin:,.2f} per maand")

# Tabelweergave (optioneel)
st.dataframe(pd.DataFrame(results).set_index("Product"))
