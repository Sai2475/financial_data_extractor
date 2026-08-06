import streamlit as st
import pandas as pd
from data_extractor import extract

# Page Configuration
st.set_page_config(
    page_title="FinExtract AI | Financial Data Extractor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for a sleek, modern financial dashboard look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header Card Styling */
    .header-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 50%, #172554 100%);
        padding: 2rem 2.5rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.4);
        margin-bottom: 2rem;
    }
    .header-title {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0 0 0.4rem 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .header-desc {
        color: #94a3b8;
        font-size: 1.02rem;
        margin: 0;
    }
    .header-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(99, 102, 241, 0.18);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.35);
        padding: 5px 14px;
        border-radius: 30px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 0.9rem;
    }

    /* Metric Cards */
    .metric-card-wrapper {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        transition: all 0.25s ease;
    }
    .metric-card-wrapper:hover {
        border-color: rgba(99, 102, 241, 0.4);
        transform: translateY(-2px);
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 0.5rem;
    }
    .metric-val {
        color: #f8fafc;
        font-size: 1.7rem;
        font-weight: 700;
    }
    .metric-subtext {
        color: #38bdf8;
        font-size: 0.85rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }

    /* Section Container */
    .section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/duotone/96/bullish.png", width=64)
    st.title("FinExtract AI")
    st.markdown("Automated LLM-driven financial earnings metric extraction.")
    
    st.divider()
    
    st.subheader("💡 How It Works")
    st.markdown("""
    1. **Paste** earnings news text into the input box.
    2. **Click Extract** to parse key metrics using **Llama-3.3 70B**.
    3. **View & Analyze** formatted tables, metric comparisons, and downloadable raw data.
    """)
    
    st.divider()
    st.caption("Powered by LangChain & Groq AI")

# Main Header Banner
st.markdown("""
    <div class="header-card">
        <div class="header-title">
            <span>📈 Financial Earnings Extractor</span>
        </div>
        <div class="header-desc">
            Instantly extract key financial metrics (Revenue & EPS - Actual vs. Expected) from corporate news & financial reports.
        </div>
    </div>
""", unsafe_allow_html=True)

# Sample Articles preset dictionary
SAMPLES = {
    "Tesla Q3 Earnings": "Tesla reported Q3 revenue of $25.18 billion, missing wall street expectations of $25.37 billion. Adjusted earnings per share came in at $0.72, topping estimated EPS of $0.60.",
    "Apple Q4 Earnings": "Apple Inc. announced fourth-quarter revenue of $89.5 billion versus analyst expectations of $89.28 billion. Diluted earnings per share reached $1.46, compared to expected EPS of $1.39.",
    "NVIDIA Q2 Report": "NVIDIA reported record quarterly revenue of $30.04 billion, beating expected revenue of $28.7 billion. Quarterly earnings per share was $0.68, outperforming expected EPS of $0.64."
}

# Input Section with Quick Sample Selector
st.markdown('<div class="section-header">📄 Input Financial Article</div>', unsafe_allow_html=True)

col_sample1, col_sample2, col_sample3 = st.columns([1, 1, 1])
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

with col_sample1:
    if st.button("📌 Load Tesla Sample", use_container_width=True):
        st.session_state["input_text"] = SAMPLES["Tesla Q3 Earnings"]
with col_sample2:
    if st.button("📌 Load Apple Sample", use_container_width=True):
        st.session_state["input_text"] = SAMPLES["Apple Q4 Earnings"]
with col_sample3:
    if st.button("📌 Load NVIDIA Sample", use_container_width=True):
        st.session_state["input_text"] = SAMPLES["NVIDIA Q2 Report"]

paragraph = st.text_area(
    "Enter financial paragraph or news report:",
    value=st.session_state["input_text"],
    height=160,
    placeholder="Paste news article, press release, or quarterly earnings report here..."
)

col_act1, col_act2 = st.columns([1, 4])
with col_act1:
    extract_btn = st.button("⚡ Extract Data", type="primary", use_container_width=True)
with col_act2:
    if st.button("🧹 Clear Text", use_container_width=False):
        st.session_state["input_text"] = ""
        st.rerun()

# Execution & Results
if extract_btn:
    if not paragraph.strip():
        st.warning("⚠️ Please enter or select a financial paragraph before clicking Extract.")
    else:
        with st.spinner("🔍 Analyzing financial report with AI model..."):
            try:
                extracted_data = extract(paragraph)
                
                st.success("✅ Financial metrics successfully extracted!")
                st.divider()

                # Metric Cards Display
                st.markdown('<div class="section-header">📊 Key Performance Metrics</div>', unsafe_allow_html=True)
                
                m1, m2, m3, m4 = st.columns(4)
                
                rev_actual = extracted_data.get('revenue_actual', 'N/A')
                rev_expected = extracted_data.get('revenue_expected', 'N/A')
                eps_actual = extracted_data.get('eps_actual', 'N/A')
                eps_expected = extracted_data.get('eps_expected', 'N/A')

                with m1:
                    st.markdown(f"""
                        <div class="metric-card-wrapper">
                            <div class="metric-label">Actual Revenue</div>
                            <div class="metric-val">{rev_actual}</div>
                            <div class="metric-subtext">Reported Value</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with m2:
                    st.markdown(f"""
                        <div class="metric-card-wrapper">
                            <div class="metric-label">Expected Revenue</div>
                            <div class="metric-val">{rev_expected}</div>
                            <div class="metric-subtext">Consensus Estimate</div>
                        </div>
                    """, unsafe_allow_html=True)

                with m3:
                    st.markdown(f"""
                        <div class="metric-card-wrapper">
                            <div class="metric-label">Actual EPS</div>
                            <div class="metric-val">{eps_actual}</div>
                            <div class="metric-subtext">Reported Per Share</div>
                        </div>
                    """, unsafe_allow_html=True)

                with m4:
                    st.markdown(f"""
                        <div class="metric-card-wrapper">
                            <div class="metric-label">Expected EPS</div>
                            <div class="metric-val">{eps_expected}</div>
                            <div class="metric-subtext">Estimated Per Share</div>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Tabbed Detail View
                tab_table, tab_json = st.tabs(["📋 Structured Data Table", "⚙️ Raw JSON Output"])
                
                data = {
                    'Measure': ['Revenue', 'EPS'],
                    'Estimated': [rev_expected, eps_expected],
                    'Actual': [rev_actual, eps_actual]
                }
                df = pd.DataFrame(data)

                with tab_table:
                    st.dataframe(
                        df,
                        column_config={
                            "Measure": st.column_config.TextColumn("Financial Metric", help="Revenue or Earnings Per Share"),
                            "Estimated": st.column_config.TextColumn("Consensus Estimate", help="Wall Street Expected"),
                            "Actual": st.column_config.TextColumn("Actual Reported", help="Company Reported"),
                        },
                        use_container_width=True,
                        hide_index=True
                    )

                    # CSV Download Option
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv_data,
                        file_name="extracted_financial_metrics.csv",
                        mime="text/csv"
                    )

                with tab_json:
                    st.json(extracted_data)

            except Exception as e:
                st.error(f"An error occurred during extraction: {str(e)}")

