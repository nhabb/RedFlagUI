# app.py
import streamlit as st
import requests
import pandas as pd
import json

# Page config
st.set_page_config(page_title="RedFlag SOC Dashboard", page_icon="⚐", layout="wide")

# Configuration - Update with your n8n webhook URL
N8N_WEBHOOK_URL = st.secrets.get("N8N_WEBHOOK_URL", "https://your-n8n-instance.com/webhook/alert-triage")

# Initialize session state for storing data
if 'threats_detected' not in st.session_state:
    st.session_state.threats_detected = 0
if 'false_positive' not in st.session_state:
    st.session_state.false_positive = 0
if 'true_positive' not in st.session_state:
    st.session_state.true_positive = 0
if 'final_threat_count' not in st.session_state:
    st.session_state.final_threat_count = 0
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None

# Function to send data to n8n
def send_to_n8n(file_data):
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={
                "fileName": file_data.name,
                "timestamp": pd.Timestamp.now().isoformat(),
                "data": file_data.getvalue().decode('utf-8')
            },
            timeout=30
        )
        
        if response.ok:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to n8n: {str(e)}")
        return None

# Function to update metrics from n8n response
def update_metrics(response_data):
    if response_data:
        st.session_state.threats_detected = response_data.get('threats_detected', 0)
        st.session_state.false_positive = response_data.get('false_positive', 0)
        st.session_state.true_positive = response_data.get('true_positive', 0)
        st.session_state.final_threat_count = response_data.get('final_threat_count', 0)
        st.session_state.analysis_data = response_data

# Sidebar menu
st.sidebar.title("🔴 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Alert Analysis", "Threat Intelligence", "Reports", "Settings"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")
st.sidebar.metric("Active Alerts", "12")
st.sidebar.metric("Response Time", "2.3s")
st.sidebar.markdown("---")
st.sidebar.info("💡 Upload a CSV file to analyze security alerts")

# Custom CSS for black and red theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #121212;
        color: white;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #8b0000 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Text */
    p, span, div, label {
        color: #cccccc !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background-color: #1e1e1e;
        border: 2px solid #8b0000;
        border-radius: 10px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #a00000;
        box-shadow: 0 4px 12px rgba(139, 0, 0, 0.4);
    }
    
    [data-testid="stFileUploader"] label {
        color: #8b0000 !important;
        font-weight: bold;
        font-size: 18px;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #8b0000;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #a00000;
        box-shadow: 0 4px 12px rgba(139, 0, 0, 0.5);
        transform: translateY(-2px);
    }
    
    /* Text inputs and text areas */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #1e1e1e;
        color: white;
        border: 2px solid #8b0000;
        border-radius: 8px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 2px solid #8b0000;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 3rem;
        max-width: 1400px;
    }
    
    /* Title styling */
    .main-title {
        font-size: 70px;
        font-weight: bold;
        color: #8b0000;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    .subtitle {
        text-align: center;
        color: #cccccc;
        font-size: 18px;
        margin-bottom: 40px;
    }
    
    /* Upload section */
    .upload-section {
        background-color: #1e1e1e;
        border-left: 4px solid #8b0000;
        border-top: 4px solid #8b0000;
        border-radius: 8px;
        padding: 30px;
        margin-bottom: 40px;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-left-color: white;
        border-top-color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 255, 255, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Main content based on selected page
if page == "Dashboard":
    # Main title
    st.markdown('<h1 class="main-title">🔴 RedFlag Check</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Advanced SOC Alert Triage Dashboard</p>', unsafe_allow_html=True)

    # Upload section
    # st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.subheader("📁 Upload logs")
    uploaded_file = st.file_uploader("Upload CSV file containing security alerts", type=['csv'])
    
    # Process file when uploaded
    if uploaded_file is not None:
        with st.spinner('🔄 Processing file and sending to n8n...'):
            result = send_to_n8n(uploaded_file)
            
            if result:
                update_metrics(result)
                st.success('✅ File processed successfully!')
                
                # Display result details if available
                if 'message' in result:
                    st.info(result['message'])
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Create cards using containers with custom styling
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">{st.session_state.threats_detected}</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">THREATS DETECTED</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">{st.session_state.false_positive}</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">FALSE POSITIVE</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">{st.session_state.true_positive}</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">TRUE POSITIVE</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">{st.session_state.final_threat_count}</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">FINAL THREAT COUNT</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "Alert Analysis":
    st.title("📊 Alert Analysis")
    st.write("Detailed analysis of security alerts")
    
    # Alert Analysis Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">156</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">TOTAL ALERTS THIS WEEK</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">89%</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">AUTO-TRIAGE SUCCESS RATE</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">23</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">CRITICAL ALERTS</p>
        </div>
        """, unsafe_allow_html=True)
    
elif page == "Threat Intelligence":
    st.title("🔍 Threat Intelligence")
    st.write("Real-time threat intelligence feeds and indicators")
    
    # Threat Intelligence Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">342</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">MALICIOUS IPs BLOCKED</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">67</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">THREAT ACTORS IDENTIFIED</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">1,234</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">IOCs PROCESSED</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">15</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">ACTIVE CAMPAIGNS</p>
        </div>
        """, unsafe_allow_html=True)
    
elif page == "Reports":
    st.title("📄 Reports")
    st.write("Security reports and analytics")
    
    # Reports Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">48</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">REPORTS GENERATED</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">98%</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">COMPLIANCE SCORE</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">12</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">INCIDENTS RESOLVED</p>
        </div>
        """, unsafe_allow_html=True)
    
elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("Configure dashboard settings and preferences")
    
    # Settings Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">5</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">ACTIVE INTEGRATIONS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 2px solid #8b0000; text-align: center;">
            <h1 style="color: #8b0000; margin: 0;">8</h1>
            <p style="color: #ccc; font-size: 12px; margin: 10px 0 0 0;">CONFIGURED WORKFLOWS</p>
        </div>
        """, unsafe_allow_html=True)

