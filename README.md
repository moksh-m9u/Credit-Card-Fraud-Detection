# Credit Card Fraud Detection

A machine learning project designed to detect fraudulent credit card transactions using FastAPI for model serving. The system utilizes Random Forest and XGBoost classifiers trained on highly imbalanced data.

## Project Structure

- **data/**: Contains the `creditcard.csv` dataset.
- **notebooks/**: Jupyter notebooks for exploratory data analysis and model training.
- **schema/**: Pydantic models for input validation.
- **src/**: FastAPI application source code.
- **model/**: Pre-trained model artifacts.

## Data Source

The project uses the [Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) from Kaggle.

### Context
It is essential for credit card companies to identify fraudulent transactions to prevent customers from being charged for unauthorized purchases.

### Content
The dataset contains transactions made by European cardholders in September 2013. It includes 492 frauds out of 284,807 transactions, making it highly imbalanced (0.172% fraud cases).

- **Features V1-V28**: Principal components obtained via PCA due to confidentiality issues.
- **Time**: Seconds elapsed between the transaction and the first transaction in the dataset.
- **Amount**: The transaction amount, suitable for cost-sensitive learning.
- **Class**: The response variable (1 for fraud, 0 otherwise).

Due to the extreme class imbalance, performance is measured using the Area Under the Precision-Recall Curve (AUPRC) rather than standard accuracy.

## Exploratory Data Analysis

The EDA phase focused on understanding the distribution of legit vs. fraudulent transactions:
- **Class Imbalance**: Identified and addressed the significant skew in target classes.
- **Profiling**: Used pandas-profiling for comprehensive data visualization and comparison.
- **Feature Importance**: Derived importance using Pearson and Spearman correlations.
- **Refined Selection**: Transitioned to Random Forest for feature extraction to capture non-linear patterns, identifying top features including V14, V10, V12, V4, V17, V3, V11, V16, and Amount.

## Model Development

### Random Forest
- **Preprocessing**: RobustScaler was applied to the Amount feature. PCA-transformed features (V1-V28) were kept as-is.
- **Strategy**: Used `class_weight='balanced'` and Random Search CV for hyperparameter tuning.
- **Threshold Optimization**: Finalized a threshold of 0.1 to maximize recall (0.80) and precision (0.84).

### XGBoost
- **Preprocessing**: Similar pipeline using RobustScaler for the Amount feature.
- **Strategy**: Implemented `scale_pos_weight` to handle imbalance and optimized for F2 score using Random Search CV.
- **Threshold Optimization**: Finalized a threshold of 0.2, achieving a mean recall of 0.82 and precision of 0.88.

## API Documentation

The FastAPI server provides endpoints for real-time predictions:

- **POST /predict**: Single transaction prediction. Requires key features and optional PCA components.
- **POST /predict_batch**: Batch prediction for a list of transactions.

### Required Features
The model expects the following primary features:
`V14, V10, V12, V4, V17, V3, V11, V16, Amount`

## Setup and Installation

### Local Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the server:
   ```bash
   uvicorn src.main:app --reload
   ```
3. Access documentation at: `http://127.0.0.1:8000/docs`

### Docker Setup
The containerized application is available on [Docker Hub](https://hub.docker.com/r/mokshm9u/project-server).

Pull and run the image:
```bash
docker pull mokshm9u/project-server
docker run -p 3000:3000 mokshm9u/project-server:latest
```

## Deployment
The backend server is deployed on Render and can be accessed at:
[https://credict-card-server.onrender.com/docs](https://credict-card-server.onrender.com/docs)

## Project Status and Roadmap

This repository serves as a learning project, implemented to apply and showcase skills in Docker, FastAPI, and machine learning techniques for handling highly imbalanced datasets.

The current implementation is a functional prototype that will be refined further. Planned improvements include:
- **Modularization**: Refactoring the codebase into a more robust and maintainable structure.
- **Data Version Control (DVC)**: Implementing DVC for managing datasets and model versions.
- **Experiment Tracking**: Integrating MLflow for comprehensive monitoring and experiment tracking.
- **CI/CD**: Establishing automated pipelines for testing and deployment.