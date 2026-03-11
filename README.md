# 🛡️ FraudShield — Credit Card Fraud Detection

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-FF4B4B?style=for-the-badge&logo=streamlit)
![XGBoost](https://img.shields.io/badge/XGBoost-Model-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> Real-time credit card fraud detection powered by XGBoost — trained on 284,807 transactions and optimized for high recall.

---

## 🚀 Live Demo

👉 **https://fraud-detection-u8anpjrezsulqtvgqzbrqh.streamlit.app/**

---

## 📌 Problem Statement

Credit card fraud is a major financial threat. This project builds a machine learning system to **detect fraudulent transactions in real-time** using a highly imbalanced dataset where only **0.17%** of transactions are fraudulent.

---

## 📊 Dataset

- **Source:** [Kaggle — Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- **Size:** 284,807 transactions
- **Fraud Cases:** 492 (0.17%)
- **Features:** V1–V28 (PCA anonymized), Amount, Time
- **Target:** `Class` → 0 = Legitimate, 1 = Fraud

---

## 🧠 ML Pipeline

```
Raw Data → EDA → Preprocessing → SMOTE Balancing → Model Training → Evaluation → Deployment
```

### 1️⃣ Preprocessing
- Scaled `Amount` and `Time` using `StandardScaler`
- V1–V28 already PCA-transformed for privacy

### 2️⃣ Handling Imbalance
- Applied **SMOTE** (Synthetic Minority Oversampling Technique)
- Only applied on training data to prevent data leakage

### 3️⃣ Models Trained

| Model | ROC-AUC | Recall | Precision |
|-------|---------|--------|-----------|
| Logistic Regression | ~0.97 | ~0.88 | ~0.87 |
| Random Forest | ~0.97 | ~0.89 | ~0.88 |
| **XGBoost ✅** | **~0.98** | **~0.90** | **~0.89** |

### 4️⃣ Why XGBoost?
- Highest ROC-AUC and Recall scores
- Handles imbalanced data well
- Fast inference for real-time detection

---

## 🎯 Key Metrics Focus

> **Recall is the most important metric here.**
> Missing a fraud (False Negative) is far more costly than a false alarm (False Positive).

---

## 🖥️ App Features

- 🔍 **Single Transaction Analysis** — Enter transaction details and get instant fraud prediction with probability score
- 📂 **Batch Prediction** — Upload a CSV file to analyze thousands of transactions at once
- 📊 **How It Works** — Detailed explanation of the ML pipeline and model comparison
- ⬇️ **Download Results** — Export batch predictions as CSV

---

## 🗂️ Project Structure

```
fraud-detection/
│
├── app.py                  ← Streamlit web application
├── fraud_model.pkl         ← Trained XGBoost model
├── scaler.pkl              ← Fitted StandardScaler
├── requirements.txt        ← Python dependencies
├── README.md               ← Project documentation
└── notebooks/
    └── fraud_detection.ipynb  ← Google Colab notebook
```

---

## ⚙️ Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/fraud-detection.git
cd fraud-detection
```

### 2. Install dependencies
```bash
python -m pip install -r requirements.txt
```

### 3. Run the app
```bash
python -m streamlit run app.py
```

### 4. Open in browser
```
http://localhost:8501
```

---

## 📦 Tech Stack

| Tool | Purpose |
|------|---------|
| 🐍 Python 3.11 | Core language |
| ⚡ XGBoost | Primary ML model |
| 🔬 Scikit-learn | Preprocessing & evaluation |
| ⚖️ Imbalanced-learn | SMOTE oversampling |
| 🎈 Streamlit | Web application |
| 📊 Pandas & NumPy | Data manipulation |
| 📈 Matplotlib & Seaborn | Visualizations |
| 🐙 GitHub | Version control |
| ☁️ Streamlit Cloud | Deployment |

---

## 📈 Results

```
              precision    recall  f1-score   support

           0       1.00      1.00      1.00     56864
           1       0.89      0.90      0.89        98

    accuracy                           1.00     56962
   macro avg       0.94      0.95      0.95     56962
weighted avg       1.00      1.00      1.00     56962

ROC-AUC Score: 0.9823
```

---

## 🏆 Hackathon Project

Built for a college hackathon focusing on:
- Real-world imbalanced classification problem
- End-to-end ML pipeline from data to deployment
- Production-ready web application

---

## 👤 Author

**Your Name**
- GitHub: GITVIDHUB-1010

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
  <b>⭐ Star this repo if you found it helpful!</b><br><br>
  Built with ❤️ using Python & Streamlit
</div>
