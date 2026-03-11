import streamlit as st
import numpy as np
import joblib
import pandas as pd
import os

st.set_page_config(
    page_title="FraudShield | Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* Background */
.stApp {
    background: #0a0a0f;
    color: #e8e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #1e1e3a;
}

/* Main header */
.hero-header {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a0a2e 50%, #0a1628 100%);
    border: 1px solid #2a1a4e;
    border-radius: 16px;
    padding: 40px;
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;
}

.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(120, 40, 255, 0.08) 0%, transparent 60%),
                radial-gradient(circle at 80% 20%, rgba(40, 120, 255, 0.06) 0%, transparent 50%);
    pointer-events: none;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 3rem;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-family: 'Space Mono', monospace;
    color: #6b7280;
    font-size: 0.85rem;
    margin-top: 8px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* Metric cards */
.metric-card {
    background: #0f0f1a;
    border: 1px solid #1e1e3a;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: border-color 0.3s;
}

.metric-card:hover {
    border-color: #4c1d95;
}

.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #a78bfa;
}

.metric-label {
    font-size: 0.75rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

/* Result boxes */
.fraud-result {
    background: linear-gradient(135deg, #1a0000, #2d0000);
    border: 2px solid #dc2626;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    animation: pulse-red 2s infinite;
}

.safe-result {
    background: linear-gradient(135deg, #001a0a, #002d12);
    border: 2px solid #16a34a;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
}

@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.4); }
    50% { box-shadow: 0 0 20px 5px rgba(220, 38, 38, 0.1); }
}

.result-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.6rem;
    margin: 0;
}

.result-prob {
    font-family: 'Space Mono', monospace;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 8px 0;
}

/* Input styling */
[data-testid="stNumberInput"] input {
    background: #0f0f1a !important;
    border: 1px solid #1e1e3a !important;
    color: #e8e8f0 !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
}

[data-testid="stNumberInput"] input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2) !important;
}

/* Tab styling */
[data-testid="stTab"] {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 12px 24px !important;
    transition: all 0.3s !important;
    letter-spacing: 0.5px !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4) !important;
}

/* Section headers */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #7c3aed;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e1e3a;
}

/* Warning / info boxes */
.info-box {
    background: #0a0f1a;
    border-left: 3px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 0.85rem;
    color: #93c5fd;
    font-family: 'Space Mono', monospace;
}

/* Divider */
hr {
    border-color: #1e1e3a !important;
    margin: 24px 0 !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #1e1e3a;
    border-radius: 10px;
    overflow: hidden;
}

/* Streamlit metric */
[data-testid="metric-container"] {
    background: #0f0f1a;
    border: 1px solid #1e1e3a;
    border-radius: 10px;
    padding: 16px;
}

[data-testid="metric-container"] label {
    color: #6b7280 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #a78bfa !important;
    font-family: 'Space Mono', monospace !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a1a4e; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #7c3aed; }
</style>
""", unsafe_allow_html=True)



def load_model():
    try:
        model  = joblib.load('fraud_model.pkl')
        scaler = joblib.load('scaler.pkl')
        return model, scaler, True
    except Exception as e:
        return None, None, False

model, scaler, model_loaded = load_model()



st.markdown("""
<div class="hero-header">
    <p class="hero-subtitle">🛡️ AI-Powered Security System</p>
    <h1 class="hero-title">FraudShield</h1>
    <p style="color:#6b7280; margin-top:12px; font-size:0.95rem; max-width:600px;">
        Real-time credit card fraud detection using XGBoost trained on 284,807 transactions. 
        Optimized for <span style="color:#a78bfa;">high recall</span> — catching every fraud that matters.
    </p>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.error("⚠️ Model files not found! Make sure `fraud_model.pkl` and `scaler.pkl` are in the same folder as `app.py`")
    st.stop()



with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <div style="font-size:3rem;">🛡️</div>
        <div style="font-family:'Syne',sans-serif; font-weight:800; font-size:1.3rem; color:#a78bfa;">FraudShield</div>
        <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#4b5563; letter-spacing:2px; text-transform:uppercase;">v1.0.0 · XGBoost</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="section-header">Model Performance</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("ROC-AUC", "~0.98")
        st.metric("Precision", "~0.89")
    with col2:
        st.metric("Recall", "~0.90")
        st.metric("F1 Score", "~0.89")

    st.divider()

    st.markdown('<div class="section-header">Dataset Info</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.75rem; color:#6b7280; line-height:2;">
    📊 284,807 transactions<br>
    🚨 492 fraud cases (0.17%)<br>
    🔬 SMOTE for balancing<br>
    🔑 V1–V28 (PCA features)<br>
    📅 Kaggle · ULB Dataset
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div class="info-box">
    ⚡ Focus on <b>Recall</b> — catching every fraud case is more important than false positives.
    </div>
    """, unsafe_allow_html=True)



tab1, tab2, tab3 = st.tabs(["🔍 Single Transaction", "📂 Batch Prediction", "📊 How It Works"])



with tab1:

    st.markdown('<div class="section-header">Transaction Details</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        amount = st.number_input("💰 Transaction Amount ($)",
                                  min_value=0.0, max_value=50000.0,
                                  value=149.62, step=0.01,
                                  help="The transaction amount in USD")
    with col_b:
        time = st.number_input("⏱️ Time (seconds elapsed)",
                                min_value=0.0, max_value=200000.0,
                                value=406.0, step=1.0,
                                help="Seconds elapsed since first transaction in dataset")

    st.markdown('<div class="section-header" style="margin-top:20px;">PCA Features — V1 to V28</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box" style="margin-bottom:16px;">These are anonymized PCA-transformed features. If testing, leave as 0.0 or use values from the Kaggle dataset.</div>', unsafe_allow_html=True)

    v_values = []
    rows = [st.columns(7) for _ in range(4)]
    for i in range(28):
        row_idx = i // 7
        col_idx = i % 7
        with rows[row_idx][col_idx]:
            val = st.number_input(f"V{i+1}", value=0.0, format="%.4f",
                                   key=f"v{i+1}", label_visibility="visible")
            v_values.append(val)

    st.markdown("<br>", unsafe_allow_html=True)

    predict_btn = st.button("🔮 Analyze Transaction", type="primary", use_container_width=True)

    if predict_btn:
        # Preprocess
        amount_scaled = scaler.transform([[amount]])[0][0]
        time_scaled   = scaler.transform([[time]])[0][0]

        features = np.array(v_values + [amount_scaled, time_scaled]).reshape(1, -1)

        prediction  = model.predict(features)[0]
        probability = model.predict_proba(features)[0]

        st.divider()

        if prediction == 1:
            st.markdown(f"""
            <div class="fraud-result">
                <p class="result-title" style="color:#ef4444;">🚨 FRAUDULENT TRANSACTION</p>
                <p class="result-prob" style="color:#ef4444;">{probability[1]*100:.2f}%</p>
                <p style="color:#9ca3af; font-size:0.85rem; font-family:'Space Mono',monospace;">
                    FRAUD PROBABILITY · IMMEDIATE ACTION REQUIRED
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="safe-result">
                <p class="result-title" style="color:#22c55e;">✅ LEGITIMATE TRANSACTION</p>
                <p class="result-prob" style="color:#22c55e;">{probability[0]*100:.2f}%</p>
                <p style="color:#9ca3af; font-size:0.85rem; font-family:'Space Mono',monospace;">
                    SAFE PROBABILITY · TRANSACTION CLEARED
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Probability breakdown
        col1, col2 = st.columns(2)
        with col1:
            st.metric("✅ Legitimate Probability", f"{probability[0]*100:.4f}%")
        with col2:
            st.metric("🚨 Fraud Probability", f"{probability[1]*100:.4f}%")

        # Bar chart
        prob_df = pd.DataFrame({
            'Class': ['Legitimate', 'Fraudulent'],
            'Probability': [probability[0], probability[1]]
        })
        st.bar_chart(prob_df.set_index('Class'), color=["#a78bfa"])



with tab2:

    st.markdown('<div class="section-header">Batch CSV Upload</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box" style="margin-bottom:20px;">
    📋 Upload a CSV file with columns: <b>V1–V28, Amount, Time</b><br>
    Optionally include a <b>Class</b> column to compare predictions vs actual labels.
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload CSV File", type=['csv'],
                                      label_visibility="collapsed")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.markdown('<div class="section-header">Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(df.head(5), use_container_width=True)
        st.caption(f"📊 {len(df):,} rows × {len(df.columns)} columns loaded")

        if st.button("🔮 Run Batch Analysis", type="primary", use_container_width=True):

            with st.spinner("🔄 Analyzing transactions..."):
                try:
                    df_proc = df.copy()

                    # Scale Amount and Time
                    df_proc['Amount_scaled'] = scaler.transform(df_proc[['Amount']])
                    df_proc['Time_scaled']   = scaler.transform(df_proc[['Time']])

                    # Build model input
                    feature_cols = [f'V{i}' for i in range(1, 29)] + ['Amount_scaled', 'Time_scaled']
                    X_batch = df_proc[feature_cols]

                    preds = model.predict(X_batch)
                    probs = model.predict_proba(X_batch)[:, 1]

                    df['Prediction']        = preds
                    df['Fraud_Probability'] = (probs * 100).round(4)
                    df['Result']            = df['Prediction'].map({0: '✅ Legitimate', 1: '🚨 Fraud'})

                    # ── Summary Metrics ──
                    st.divider()
                    st.markdown('<div class="section-header">Results Summary</div>', unsafe_allow_html=True)

                    fraud_count = int((preds == 1).sum())
                    legit_count = int((preds == 0).sum())
                    fraud_pct   = fraud_count / len(preds) * 100

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("📊 Total",    f"{len(preds):,}")
                    col2.metric("🚨 Fraud",    f"{fraud_count:,}")
                    col3.metric("✅ Legit",    f"{legit_count:,}")
                    col4.metric("⚠️ Fraud Rate", f"{fraud_pct:.2f}%")

                    # ── Results Table ──
                    st.markdown('<div class="section-header" style="margin-top:20px;">Detailed Results</div>', unsafe_allow_html=True)
                    display_df = df[['Result', 'Fraud_Probability']].copy()
                    display_df.index.name = 'Transaction #'
                    st.dataframe(display_df.head(100), use_container_width=True)

                    if len(df) > 100:
                        st.caption(f"Showing first 100 of {len(df):,} transactions")

                    # ── Download ──
                    csv_out = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "⬇️ Download Full Results CSV",
                        data=csv_out,
                        file_name="fraud_predictions.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"❌ Error processing file: {e}")
                    st.info("Make sure your CSV has all required columns: V1–V28, Amount, Time")



with tab3:

    st.markdown('<div class="section-header">System Overview</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background:#0f0f1a; border:1px solid #1e1e3a; border-radius:12px; padding:24px;">
            <div style="font-family:'Space Mono',monospace; font-size:0.7rem; letter-spacing:2px; color:#7c3aed; text-transform:uppercase; margin-bottom:16px;">🔬 How Detection Works</div>
            <div style="font-size:0.9rem; color:#9ca3af; line-height:2;">
            <b style="color:#e8e8f0;">1. Data Collection</b><br>
            Transaction features (V1–V28) are anonymized via PCA for privacy.<br><br>
            <b style="color:#e8e8f0;">2. Preprocessing</b><br>
            Amount and Time are scaled using StandardScaler.<br><br>
            <b style="color:#e8e8f0;">3. SMOTE Balancing</b><br>
            Synthetic minority oversampling fixes the 0.17% fraud imbalance.<br><br>
            <b style="color:#e8e8f0;">4. XGBoost Prediction</b><br>
            Gradient boosted trees classify each transaction in milliseconds.<br><br>
            <b style="color:#e8e8f0;">5. Recall-Optimized</b><br>
            Tuned to minimize missed fraud (false negatives).
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#0f0f1a; border:1px solid #1e1e3a; border-radius:12px; padding:24px;">
            <div style="font-family:'Space Mono',monospace; font-size:0.7rem; letter-spacing:2px; color:#7c3aed; text-transform:uppercase; margin-bottom:16px;">📈 Model Comparison</div>
            <table style="width:100%; font-size:0.85rem; border-collapse:collapse; font-family:'Space Mono',monospace;">
                <tr style="color:#6b7280; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px;">
                    <td style="padding:8px 0; border-bottom:1px solid #1e1e3a;">Model</td>
                    <td style="padding:8px 0; border-bottom:1px solid #1e1e3a;">AUC</td>
                    <td style="padding:8px 0; border-bottom:1px solid #1e1e3a;">Recall</td>
                    <td style="padding:8px 0; border-bottom:1px solid #1e1e3a;">Status</td>
                </tr>
                <tr style="color:#9ca3af;">
                    <td style="padding:10px 0; border-bottom:1px solid #1e1e3a;">Logistic Reg.</td>
                    <td style="padding:10px 0; border-bottom:1px solid #1e1e3a;">~0.97</td>
                    <td style="padding:10px 0; border-bottom:1px solid #1e1e3a;">~0.88</td>
                    <td style="padding:10px 0; border-bottom:1px solid #1e1e3a; color:#6b7280;">Baseline</td>
                </tr>
                <tr style="color:#9ca3af;">
                    <td style="padding:10px 0; border-bottom:1px solid #1e1e3a;">Random Forest</td>
                    <td style="padding:10px 0; border-bottom:1px solid #1e1e3a;">~0.97</td>
                    <td style="padding:10px 0; border-bottom:1px solid #1e1e3a;">~0.89</td>
                    <td style="padding:10px 0; border-bottom:1px solid #1e1e3a; color:#60a5fa;">Good</td>
                </tr>
                <tr style="color:#e8e8f0;">
                    <td style="padding:10px 0;"><b>XGBoost</b></td>
                    <td style="padding:10px 0;"><b>~0.98</b></td>
                    <td style="padding:10px 0;"><b>~0.90</b></td>
                    <td style="padding:10px 0; color:#a78bfa;"><b>✓ Selected</b></td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg, #0f0a1a, #0a0f1a); border:1px solid #2a1a4e; border-radius:12px; padding:24px; text-align:center;">
        <div style="font-family:'Space Mono',monospace; font-size:0.7rem; letter-spacing:3px; color:#7c3aed; text-transform:uppercase; margin-bottom:12px;">Built With</div>
        <div style="font-size:0.9rem; color:#6b7280;">
            🐍 Python &nbsp;·&nbsp; ⚡ XGBoost &nbsp;·&nbsp; 🔬 Scikit-learn &nbsp;·&nbsp; ⚖️ SMOTE &nbsp;·&nbsp; 🎈 Streamlit &nbsp;·&nbsp; 📊 Kaggle Dataset
        </div>
        <div style="font-family:'Space Mono',monospace; font-size:0.7rem; color:#374151; margin-top:12px;">
            FRAUDSHIELD · HACKATHON PROJECT · 2024
        </div>
    </div>
    """, unsafe_allow_html=True)



st.markdown("""
<div style="text-align:center; padding:40px 0 20px; font-family:'Space Mono',monospace; font-size:0.7rem; color:#374151; letter-spacing:1px;">
    FRAUDSHIELD · BUILT FOR HACKATHON · POWERED BY XGBOOST
</div>
""", unsafe_allow_html=True)