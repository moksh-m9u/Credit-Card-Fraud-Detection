import streamlit as st
import os
from PIL import Image

def render_overview():
    st.markdown('<div class="section-header">Project Context & Data Understanding</div>', unsafe_allow_html=True)
    st.markdown("""
    Identifying fraudulent credit card transactions is critical to preventing unauthorized charges. 
    This project leverages machine learning to detect anomalies in a highly imbalanced dataset of transactions made by European cardholders in September 2013.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-title">Total Transactions</div>
            <div class="metric-value">284,807</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-title">Fraud Cases</div>
            <div class="metric-value highlight">492</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-title">Fraud Percentage</div>
            <div class="metric-value highlight">0.172%</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.info("Challenge: The dataset is extremely imbalanced (0.172% frauds), meaning standard accuracy is highly misleading. The focus is on maximizing Recall and the Area Under the Precision-Recall Curve (AUPRC).")

    st.markdown('<div class="section-header">Exploratory Data Analysis (EDA)</div>', unsafe_allow_html=True)
    st.markdown("""
    During the initial EDA phase, we focused heavily on understanding the data distribution and identifying key patterns that separate fraudulent transactions from legitimate ones.
    
    * **Pandas Profiling**: We generated and compared independent Pandas Profiling reports for both fraud and legit cases. This allowed us to immediately spot divergent data distributions between the classes.
    * **Distribution Analysis**: We thoroughly analyzed the `Transaction Amount` and `Time` distributions to check for financial or temporal anomalies.
    * **Correlation & Non-Linearity**: We evaluated both Pearson (linear) and Spearman (monotonic) correlations.
    """)

    col_img1, col_img2 = st.columns(2)
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    with col_img1:
        try:
            pearson_path = os.path.join(base_path, "assets", "pearson.png")
            img_pearson = Image.open(pearson_path)
            st.image(img_pearson, caption="Pearson Correlation Matrix (Linear Relationships)", width="stretch")
        except Exception as e:
            st.warning(f"Pearson correlation image not found in assets/pearson.png")

    with col_img2:
        try:
            spearman_path = os.path.join(base_path, "assets", "spearman.png")
            img_spearman = Image.open(spearman_path)
            st.image(img_spearman, caption="Spearman Correlation Matrix (Monotonic Relationships)", width="stretch")
        except Exception as e:
            st.warning(f"Spearman correlation image not found in assets/spearman.png")

    st.warning(" **Crucial Finding:** The correlation matrices and profiling revealed that the dataset is riddled with extreme outliers. Linear parameters are insufficient to capture the complex, non-linear patterns of fraud. This necessitated a shift towards robust, tree-based models.")
