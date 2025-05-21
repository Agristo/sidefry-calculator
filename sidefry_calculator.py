import streamlit as st

st.set_page_config(page_title="SideFry™ Cost & Margin Calculator", layout="wide")

AGRISTO_YELLOW = "#FFC20F"
AGRISTO_BLACK = "#000000"
BAG_WEIGHT = 2500  # grams

# Custom CSS for yellow increment/decrement and bold expander hover
st.markdown(f"""
    <style>
        button[aria-label="Increment"], button[aria-label="Decrement"] {{
            border-radius: 8px !important;
        }}
        button[aria-label="Increment"]:hover, button[aria-label="Decrement"]:hover,
        button[aria-label="Increment"]:focus, button[aria-label="Decrement"]:focus {{
            background-color: {AGRISTO_YELLOW} !important;
            color: {AGRISTO_BLACK} !important;
        }}
        details summary:hover {{
            font-weight: bold !important;
            color: inherit !important;
        }}
        details summary {{
            font-size: 1.03em !important;
        }}
    </style>
""", unsafe_allow_html=True)

def product_input(product, defaults, key_suffix=""):
    st.markdown(f"<h4 style='margin-bottom:0px; margin-top:24px; color:{AGRISTO_BLACK};'>{product}</h4>", unsafe_allow_html=True)
    cols = st.columns([1.2, 1.2, 1.4, 1, 1.1])
    portion_weight = cols[0].number_input("Weight per portion (g)", min_value=50, max_value=500, value=defaults["portion_weight"], step=10, key=f"weight_{product}{key_suffix}")
    cost_bag = cols[1].number_input("Cost per bag (€)", min_value=1.0, max_value=20.0, value=float(defaults["cost_bag"]), step=0.01, key=f"cost_{product}{key_suffix}")
    selling_price = cols[2].number_input("Advised selling price per portion (€)", min_value=1.0, max_value=15.0, value=float(defaults["selling_price"]), step=0.10, key=f"sell_{product}{key_suffix}")
    bags_month = cols[3].number_input("Bags sold per month", min_value=0, max_value=100, value=int(defaults["bags_month"]), step=1, key=f"bags_{product}{key_suffix}")

    portions_per_bag = BAG_WEIGHT / portion_weight
    foodcost_per_portion = cost_bag / portions_per_bag
    margin_per_portion = selling_price - foodcost_per_portion
    margin_per_bag = margin_per_portion * portions_per_bag
    margin_month = margin_per_bag * bags_month

    badge_html = f"""
    <div style="background-color:{AGRISTO_YELLOW}; color:{AGRISTO_BLACK};
        padding:13px 5px; border-radius:10px; text-align:center;
        font-size:18px; font-weight:bold; margin-top:6px; margin-bottom:6px;">
        Margin/month<br>€{margin_month:,.2f}
    </div>
    """
    cols[4].markdown(badge_html, unsafe_allow_html=True)

    with st.expander("Show full breakdown"):
        st.write(f"• Portions per bag: **{portions_per_bag:.2f}**")
        st.write(f"• Foodcost per portion: **€{foodcost_per_portion:.3f}**")
        st.write(f"• Margin per portion: **€{margin_per_portion:.3f}**")
        st.write(f"• Margin per bag: **€{margin_per_bag:.2f}**")
        st.write(f"• Margin per month: **€{margin_month:,.2f}**")

    return margin_month

# Defaults
default_standard = {"portion_weight": 200, "cost_bag": 6.25, "selling_price": 5.00, "bags_month": 10}
default_standard_plus = {"portion_weight": 200, "cost_bag": 6.25, "selling_price": 5.00, "bags_month": 8}
sidefry_products = [
    {"name": "Super Crispy SIDEWINDERS fries",        "defaults": {"portion_weight": 120, "cost_bag": 8.21, "selling_price": 6.00, "bags_month": 2}},
    {"name": "Super Crispy seasoned waffle cut fries - skin on", "defaults": {"portion_weight": 160, "cost_bag": 7.08, "selling_price": 6.00, "bags_month": 0}},
    {"name": "Super Crispy crinkle cut fries",        "defaults": {"portion_weight": 190, "cost_bag": 7.00, "selling_price": 6.00, "bags_month": 0}},
    {"name": "Crispy dippers",                        "defaults": {"portion_weight": 150, "cost_bag": 5.55, "selling_price": 6.00, "bags_month": 1}},
    {"name": "Mini hash browns",                      "defaults": {"portion_weight": 190, "cost_bag": 8.05, "selling_price": 6.00, "bags_month": 0}},
    {"name": "SmartChef mashed potatoes",             "defaults": {"portion_weight": 160, "cost_bag": 5.79, "selling_price": 6.00, "bags_month": 0}},
]

st.markdown(
    f"<h1 style='color:{AGRISTO_BLACK};font-family:sans-serif;'>SideFry™ Interactive Cost & Margin Calculator</h1>",
    unsafe_allow_html=True
)

# Section 1: Standard Only
st.markdown(
    f"<div style='background-color:#F7F7F7; border-radius:14px; padding:28px 18px 8px 18px; border: 2px solid {AGRISTO_YELLOW}; margin-bottom:18px;'>"
    f"<h2 style='color:{AGRISTO_BLACK};margin-top:0;'>1. Standard Only</h2>"
    f"<p style='color:{AGRISTO_BLACK};'>Super Crispy straight cut fries</p>",
    unsafe_allow_html=True,
)
standard_margin = product_input("Super Crispy straight cut fries", default_standard, key_suffix="_std")
st.markdown("</div>", unsafe_allow_html=True)

# Section 2: Standard + SideFry
st.markdown(
    f"<div style='background-color:#F7F7F7; border-radius:14px; padding:28px 18px 8px 18px; border: 2px solid {AGRISTO_YELLOW}; margin-bottom:18px;'>"
    f"<h2 style='color:{AGRISTO_BLACK};margin-top:0;'>2. Standard + SideFry</h2>"
    f"<p style='color:{AGRISTO_BLACK};'>Super Crispy straight cut fries and extra SideFry options</p>",
    unsafe_allow_html=True,
)
# First product: Super Crispy straight cut fries (8 bags/month)
sidefry_total_margin = product_input("Super Crispy straight cut fries", default_standard_plus, key_suffix="_plus")
# The rest: SideFry products, each with own subtitle/tussentitel
for prod in sidefry_products:
    sidefry_total_margin += product_input(prod["name"], prod["defaults"], key_suffix=f'_{prod["name"].replace(" ", "_")}')

st.markdown("</div>", unsafe_allow_html=True)

# Comparison block
st.markdown("---")
st.subheader("Comparison: Standard Only vs. Standard + SideFry")
col1, col2, col3 = st.columns(3)
col1.markdown(
    f"<div style='background-color:{AGRISTO_YELLOW}; color:{AGRISTO_BLACK}; padding:16px; border-radius:10px; text-align:center; font-size:19px; font-weight:bold;'>"
    f"Standard Only<br>€{standard_margin:,.2f}/month</div>",
    unsafe_allow_html=True,
)
col2.markdown(
    f"<div style='background-color:{AGRISTO_YELLOW}; color:{AGRISTO_BLACK}; padding:16px; border-radius:10px; text-align:center; font-size:19px; font-weight:bold;'>"
    f"Standard + SideFry<br>€{sidefry_total_margin:,.2f}/month</div>",
    unsafe_allow_html=True,
)
extra_margin = sidefry_total_margin - standard_margin
col3.markdown(
    f"<div style='background-color:{AGRISTO_BLACK}; color:{AGRISTO_YELLOW}; padding:16px; border-radius:10px; text-align:center; font-size:19px; font-weight:bold;'>"
    f"EXTRA margin<br>€{extra_margin:,.2f}/month</div>",
    unsafe_allow_html=True,
)
