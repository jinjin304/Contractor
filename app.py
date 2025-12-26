import streamlit as st
import time
import pandas as pd

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="ProEstimate AI",
    page_icon="🏗️",
    layout="wide"
)

# --- CUSTOM CSS (The "Vibe" Injector) ---
st.markdown("""
    <style>
    /* Background and Main Container */
    .stApp {
        background-color: #0F172A;
        color: #FFFFFF;
    }
    
    /* Welcome Text */
    .welcome-text {
        color: #94A3B8;
        font-size: 14px;
        margin-bottom: -10px;
    }
    
    /* Custom Card Design for Metrics */
    .metric-card {
        background: #1E293B;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #334155;
        text-align: left;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 5px 0;
    }
    .metric-label {
        color: #94A3B8;
        font-size: 14px;
    }
    
    /* New Estimate Button Styling */
    .estimate-btn {
        background: #FB923C;
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin-top: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Standard Streamlit Button Overrides */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        background-color: #FB923C !important;
        color: white !important;
        border: none;
        padding: 10px;
        font-weight: bold;
    }
    
    /* Hide Default Header */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("ProEstimate")
    page = st.radio("Navigation", ["Home", "AI Estimator"])

# --- PAGE 1: HOME (MATCHING YOUR IMAGE) ---
if page == "Home":
    st.markdown('<p class="welcome-text">Welcome back</p>', unsafe_allow_html=True)
    st.title("ProEstimate")
    
    # Metrics Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><p class="metric-label">🔨 Active Jobs</p><p class="metric-value">8</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><p class="metric-label">💰 This Month</p><p class="metric-value">$42.5k</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><p class="metric-label">🕒 Pending</p><p class="metric-value">12</p></div>', unsafe_allow_html=True)
    
    # Large Orange Button
    st.markdown("""
        <div class="estimate-btn">
            <div>
                <h3 style="margin:0; color:white;">New Estimate</h3>
                <p style="margin:0; color:white; opacity:0.8;">Create a quick estimate using AI</p>
            </div>
            <div style="font-size:30px;">↗️</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Active Jobs")
    st.info("Your active jobs list will appear here.")

# --- PAGE 2: AI ESTIMATOR ---
elif page == "AI Estimator":
    st.title("AI Photo Estimator")
    uploaded_file = st.file_uploader("Upload a photo of the job site", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption="Current Site Photo", use_container_width=True)
        
        if st.button("RUN GEMINI 3 & NANO BANANA"):
            with st.spinner("Analyzing site and generating vision..."):
                time.sleep(3) # Simulated AI logic
                
                st.divider()
                st.success("Analysis Complete!")
                
                # Layout for Results
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.subheader("Visualized Design")
                    st.image("https://via.placeholder.com/600x400/1E293B/FB923C?text=Renovated+View", use_container_width=True)
                
                with res_col2:
                    st.subheader("Cost Breakdown")
                    st.write("**Labor:** $2,400")
                    st.write("**Materials:** $1,850")
                    st.write("**Total:** $4,250")
