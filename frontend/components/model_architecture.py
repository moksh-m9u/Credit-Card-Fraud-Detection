import streamlit as st
import os
from PIL import Image

def render_model_architecture():
    st.markdown('<div class="section-header">Feature Extraction & Preprocessing</div>', unsafe_allow_html=True)
    st.markdown("""
    Before training heavy models, a baseline Random Forest was trained on the entire dataset to extract the most influential features. 
    We narrowed down 30 features to just **8 critical features** (plus Amount) that captured the maximum portion of the pattern.
    
    * **Retained Features**: `V14, V10, V12, V17, V4, V3, V11, V16` + `Amount`
    * **Preprocessing Pipeline**: Dropped duplicates and the `Time` column. Created a `ColumnTransformer` to apply `RobustScaler` to the `Amount` column (to handle outliers), while passing through the already PCA-scaled `V` features.
    """)

    st.markdown('<div class="section-header">Model 1: Random Forest Classifier</div>', unsafe_allow_html=True)
    st.markdown("""
    Instead of synthesizing data (like SMOTE), we handled the imbalance directly through algorithmic weighting.
    * **Handling Imbalance**: Used `class_weight='balanced'` which is specialized for imbalanced datasets.
    * **Tuning**: Ran `RandomizedSearchCV` for hyperparameter tuning.
    * **Threshold Optimization**: To prioritize capturing fraud (Recall), the default decision threshold was lowered. By checking the Precision-Recall curve, we finalized a threshold of **0.1**. 
    * **Results**: At threshold 0.1, we achieved **Precision: 0.84** and **Recall: 0.80**. Cross-validation confirmed a robust mean recall of ~0.76 to 0.82.
    """)

    st.markdown('<div class="section-header">Model 2: XGBoost Classifier (Final Model)</div>', unsafe_allow_html=True)
    st.markdown("""
    * **Baseline (No Tuning)**: The default XGBoost hit an accuracy of 0.99939 (misleading) with a Recall of 0.72 and F1 of 0.79.
    * **Scale Pos Weight**: Addressed the extreme imbalance by setting `scale_pos_weight` to the exact ratio of Legit-to-Fraud cases (**~598.84**).
    * **Stratified K-Fold CV**: Evaluated using Stratified K-Fold, shifting the scoring metric to PR-AUC and F2-Score.
    * **Hyperparameter Tuning**: Ran `RandomizedSearchCV` optimizing heavily for the **F2 Score** (which prioritizes recall over precision). The best model pushed the mean recall to **0.82**, F2 to **0.837**, and Precision to **0.886**.
    * **Final Threshold Tweaking**: We tested thresholds between 0.10 and 0.30. At **0.20**, the confusion matrix hit the sweet spot, minimizing false negatives and missing only **25** fraud cases entirely.
    """)
    
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        xgb_path = os.path.join(base_path, "assets", "xgbfeatureimportance.png")
        img_xgb = Image.open(xgb_path)
        st.image(img_xgb, caption="XGBoost Top Feature Importance", width="content")
    except Exception as e:
        st.warning(f"XGBoost feature importance image not found in assets/xgbfeatureimportance.png")
