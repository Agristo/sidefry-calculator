import streamlit as st
import pandas as pd

st.set_page_config(page_title="SideFry™ Cost & Margin Calculator", layout="wide")

BAG_WEIGHT = 2500  # grams

# Colors
AGRISTO_YELLOW = "#FFC20F"
AGRISTO_BLACK = "#000000"

products = [
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

st.markdown(
    f"<h1 style='color:{AGRISTO_BLACK};font-family:sans-serif;'>SideFry™ Interactive Cost & Margin Calculator</h1>",
    unsafe_allow_html=True
)
st.markdown(
    f"<p style='color:{AGRISTO_BLACK};font-size:1.1em;'>Adjust the parameters for each product. Click <b>Show full breakdown</b> for calculation details.</p>",
    unsafe_allow_html=True
)

results = []
standard_margin = 0
sidefry_margin = 0

for prod in products:
    st.markdown(f"<h4 style='margin-bottom:0px; margin-top:28px; color:{AGRISTO_BLACK};'>{prod}</h4>", unsafe_allow_html=True)
    cols = st.columns([1.2, 1.2, 1.4, 1, 1.1])
    portion_weight = cols[0].number_input("Weight per portion (g)", min_value=50, max_value=500, value=defaults[prod]["portion_weight"], step=10, key=f"weight_{prod}")
    cost_bag = cols[1].number_input("Cost per bag (€)", min_value=1.0, max_value=20.0, value=float(defaults[prod]["cost_bag"]), step=0.01, key=f"cost_{prod}")
    selling_price = cols[2].number_input("Advised selling price per portion (€)", min_value=1.0, max_value=15.0, value=float(defaults[prod]["selling_price"]), step=0.10, key=f"sell_{prod}")
    bags_month = cols[3].number_input("Bags sold per month", min_value=0, max_value=100, value=int(defaults[prod]["bags_month"]), step=1, key=f"bags_{prod}")

    portions_per_bag = BAG_WEIGHT / portion_weight
    foodcost_per_portion = cost_bag / portions_per_bag
    margin_per_portion = selling_price - foodcost_per_portion
    margin_per_bag = margin_per_portion * portions_per_bag
    margin_month = margin_per_bag * bags_month

    # Minimal yellow badge for margin/month (no border, lighter look)
    badge_html = f"""
    <div style="background-color:{AGRISTO_YELLOW}; color:{AGRISTO_BLACK}; 
        padding:13px 5px; border-radius:10px; text-align:center; 
        font-size:18px; font-weight:bold; margin-top:6px; margin-bottom:6px;">
        Margin/month<br>€{margin_month:,.2f}
    </div>
    """
    cols[4].markdown(badge_html, unsafe_allow_html=True)

    # Show calculation breakdown in expander only
    with st.expander("Show full breakdown"):
        st.write(f"• Portions per bag: **{portions_per_bag:.2f}**")
        st.write(f"• Foodcost per portion: **€{foodcost_per_portion:.3f}**")
        st.write(f"• Margin per portion: **€{margin_per_portion:.3f}**")
        st.write(f"• Margin per bag: **€{margin_per_bag:.2f}**")
        st.write(f"• Margin per month: **€{margin_month:,.2f}**")

    results.append({
        "Product": prod,
        "Margin per month (€)": margin_month
    })

    if prod == "Super Crispy straight cut fries":
        standard_margin += margin_month
    else:
        sidefry_margin += margin_month

total_margin = standard_margin + sidefry_margin

st.markdown("---")
st.subheader("Standard vs. SideFry Assortment Comparison")
col1, col2, col3 = st.columns(3)
col1.markdown(
    f"<div style='background-color:{AGRISTO_YELLOW}; color:{AGRISTO_BLACK}; padding:16px; border-radius:10px; text-align:center; font-size:19px; font-weight:bold;'>"
    f"Standard only<br>€{standard_margin:,.2f}/month</div>",
    unsafe_allow_html=True,
)
col2.markdown(
    f"<div style='background-color:{AGRISTO_YELLOW}; color:{AGRISTO_BLACK}; padding:16px; border-radius:10px; text-align:center; font-size:19px; font-weight:bold;'>"
    f"All extra SideFry products<br>€{sidefry_margin:,.2f}/month</div>",
    unsafe_allow_html=True,
)
col3.markdown(
    f"<div style='background-color:{AGRISTO_BLACK}; color:{AGRISTO_YELLOW}; padding:16px; border-radius:10px; text-align:center; font-size:19px; font-weight:bold;'>"
    f"EXTRA margin<br>€{sidefry_margin:,.2f}/month</div>",
    unsafe_allow_html=True,
)
