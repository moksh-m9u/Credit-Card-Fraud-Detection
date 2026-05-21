import streamlit as st

def apply_custom_css():
    st.markdown("""
<style>
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-text {
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        opacity: 0.8;
    }
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #4b5563;
    }
    .metric-container {
        background: rgba(100, 116, 139, 0.1);
        border: 1px solid rgba(100, 116, 139, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    .metric-container:hover {
        transform: translateY(-5px);
    }
    .metric-title {
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.8;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #3b82f6;
        margin-top: 0.5rem;
    }
    .highlight {
        color: #ef4444;
    }
</style>
""", unsafe_allow_html=True)
