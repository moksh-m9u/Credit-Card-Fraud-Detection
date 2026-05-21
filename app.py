import streamlit as st
from frontend.components.style import apply_custom_css
from frontend.components.overview import render_overview
from frontend.components.model_architecture import render_model_architecture
from frontend.components.api_architecture import render_api_architecture
from frontend.components.live_testing import render_live_testing

# Page configuration
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for premium look
apply_custom_css()

# Header
st.markdown('<div class="main-header">Credit Card Fraud Detection</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">An end‑to‑end Machine Learning Pipeline & API Implementation</div>', unsafe_allow_html=True)

# ==== Navigation Tabs ====
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview & EDA",
    "Model Architecture",
    "Production API",
    "Live API Testing"
])

with tab1:
    render_overview()

with tab2:
    render_model_architecture()

with tab3:
    render_api_architecture()

with tab4:
    render_live_testing()

st.divider()
st.markdown(
    "<div style='text-align: center; opacity: 0.6;'>Developed by Moksh • Credit Card Fraud Detection Project</div>",
    unsafe_allow_html=True,
)
