import streamlit as st

def render_api_architecture():
    st.markdown('<div class="section-header">FastAPI Production Architecture</div>', unsafe_allow_html=True)
    st.markdown("""
    The heavily tuned XGBoost model was serialized as a binary (`.pkl`) and deployed via a high-performance **FastAPI** application.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Data Validation Schema (Pydantic)
        The `schema/user_input.py` defines strict rules for incoming API payloads:
        * **Required Fields**: The 8 extracted features (`V14`, `V10`, etc.) and `Amount`.
        * **Optional Fields**: The remaining 20 PCA features and `Time`. If a user provides them (e.g. pasting a raw Kaggle row), the API gracefully ignores them.
        * **Security**: `extra='forbid'` ensures malformed data is rejected immediately with HTTP 422.
        """)
        
    with col2:
        st.markdown("""
        ### API Endpoints (`src/main.py`)
        * **`/predict`**: Accepts a single transaction. The model computes the probability of fraud, actively applies our tuned **0.20 threshold**, and returns the classification, confidence, and label.
        * **`/predict/batch`**: An optimized bulk endpoint accepting a JSON array of transactions. Under the hood, it converts payloads into a single Pandas DataFrame to utilize fast, vectorized predictions rather than iterating.
        """)
        
    st.info("The entire backend is Dockerized and deployed continuously on Render. The Streamlit dashboard acts purely as a presentation and testing layer that communicates with these endpoints.")
