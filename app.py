import streamlit as st
import time
import pandas as pd

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="ContractorPro AI",
    page_icon="🏗️",
    layout="centered"
)

# --- CUSTOM CSS (The "Vibe" Injector) ---
st.markdown("""
    <style>
    /* Background and Main Container */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* Custom Card Design */
    .job-card {
        background: #1E232D;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363D;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(90deg, #FFD700, #FFA500);
        color: black !important;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
    }

    /* Headlines */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: #FFD700;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #000000;
    }
    </style>
    """, unsafe_allow_帖=True)

# --- MOCK AI FUNCTIONS ---
def mock_gemini_estimate():
    time.sleep(2)
    return {"total": "$4,500", "items": [("Demolition", "$500"), ("Materials", "$1,200"), ("Labor", "$2,500"), ("Waste", "$300")]}

def mock_nano_banana():
    time.sleep(3)
    return "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=1000&auto=format&fit=crop"

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://via.placeholder.com/100/FFD700/000000?text=AI", width=80)
    st.title("ContractorPro")
    page = st.radio("MENU", ["🏠 Dashboard", "📸 New AI Estimate"])

# --- PAGE 1: DASHBOARD ---
if page == "🏠 Dashboard":
    st.title("Project Dashboard")
    
    # Custom HTML for "Vibe" Cards
    col1, col2 = st.columns(2)
    
    jobs = [
        {"client": "Smith Kitchen", "price": "$12k", "status": "In Progress"},
        {"client": "Johnson Fence", "price": "$2.4k", "status": "Pending"}
    ]
    
    for job in jobs:
        st.markdown(f"""
            <div class="job-card">
                <p style="color:#888; margin-bottom:0;">CLIENT</p>
                <h3 style="margin-top:0;">{job['client']}</h3>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:#FFD700; font-weight:bold;">{job['price']}</span>
                    <span style="color:#00FF41;">{job['status']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- PAGE 2: NEW ESTIMATE ---
elif page == "📸 New AI Estimate":
    st.title("AI Visual Estimator")
    
    uploaded_file = st.file_uploader("Upload site photo", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption="Original View", use_container_width=True)
        
        if st.button("✨ START AI GENERATION"):
            with st.status("Analyzing with Gemini 3...", expanded=True) as status:
                st.write("🔍 Identifying materials...")
                est = mock_gemini_estimate()
                st.write("🎨 Rendering with Nano Banana...")
                img_after = mock_nano_banana()
                status.update(label="Analysis Ready!", state="complete")

            # The Result
            st.divider()
            st.markdown("### 🪄 Renovated Vision")
            st.image(img_after, use_container_width=True)
            
            # Full Screen simulation (Streamlit images expand on click by default)
            st.caption("Click image to expand to full screen")

            st.markdown(f"## Total Estimate: {est['total']}")
            
            # Stylized breakdown
            for item, price in est['items']:
                st.markdown(f"**{item}**: {price}")
            
            st.button("💾 Save Job to Cloud")
