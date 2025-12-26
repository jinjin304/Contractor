import streamlit as st
import time
import pandas as pd

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="ContractorPro",
    page_icon="🏗️", # We can replace this with your uploaded icon URL later
    layout="centered"
)

# --- MOCK AI FUNCTIONS (Simulating Gemini 3 & Nano Banana) ---
def mock_gemini_estimate(image):
    """Simulates Gemini 3 analyzing the photo for costs."""
    time.sleep(3) # Simulate processing time
    return {
        "total": "$4,500",
        "breakdown": [
            {"Item": "Demolition & Prep", "Cost": "$500"},
            {"Item": "Materials (Tiles, Grout)", "Cost": "$1,200"},
            {"Item": "Labor (Installation)", "Cost": "$2,500"},
            {"Item": "Waste Disposal", "Cost": "$300"},
        ]
    }

def mock_nano_banana_gen(image):
    """Simulates Nano Banana generating the renovated look."""
    time.sleep(5) # Simulate processing time
    # Returns a URL to a placeholder 'After' image
    return "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=1000&auto=format&fit=crop"

# --- SIDEBAR / NAVIGATION ---
st.sidebar.title("ContractorPro")
page = st.sidebar.radio("Navigate", ["Dashboard", "New Estimate"])

# --- PAGE 1: DASHBOARD ---
if page == "Dashboard":
    st.title("📋 Job Dashboard")
    st.markdown("### Current Active Jobs")
    
    # Mock Database
    data = [
        {"Client": "Smith Residence", "Type": "Kitchen Upgrade", "Status": "In Progress", "Price": "$12,000"},
        {"Client": "Johnson Fencing", "Type": "Fence Repair", "Status": "Pending", "Price": "$2,400"},
        {"Client": "Miller Bath", "Type": "Bathroom Remodel", "Status": "Completed", "Price": "$8,500"},
    ]
    df = pd.DataFrame(data)
    
    # Display styled dataframe
    st.dataframe(df, use_container_width=True)
    
    st.info("💡 Tip: Go to 'New Estimate' to use the AI Camera tools.")

# --- PAGE 2: NEW ESTIMATE (AI INTEGRATION) ---
elif page == "New Estimate":
    st.title("📸 AI Estimator")
    st.write("Upload a site photo to generate a cost breakdown and visual preview.")

    # 1. Input: Camera or Upload
    uploaded_file = st.file_uploader("Take a photo or upload", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Show the "Before" image immediately
        st.image(uploaded_file, caption="Original Site Photo", use_container_width=True)
        
        if st.button("Generate Estimate & Visuals"):
            
            # 2. Loading State (The "While AI is loading" requirement)
            with st.status("AI Agents Working...", expanded=True) as status:
                st.write("🤖 Gemini 3 is analyzing geometry and materials...")
                estimate_data = mock_gemini_estimate(uploaded_file)
                
                st.write("🎨 Nano Banana is rendering the new design...")
                renovated_image_url = mock_nano_banana_gen(uploaded_file)
                
                status.update(label="Analysis Complete!", state="complete", expanded=False)

            # 3. The Result (Nano Banana Visual + Cost Breakdown)
            st.divider()
            
            # Layout: Image on top (or side) and costs below
            st.subheader("✨ Proposed Renovation (Nano Banana)")
            
            # This is the "Click to go full screen" equivalent in Streamlit
            st.image(renovated_image_url, caption="After Renovation", use_container_width=True)
            
            st.subheader(f"💰 Estimated Total: {estimate_data['total']}")
            
            # Display breakdown as a clean table
            breakdown_df = pd.DataFrame(estimate_data['breakdown'])
            st.table(breakdown_df)

            st.button("Save to Dashboard", type="primary")
