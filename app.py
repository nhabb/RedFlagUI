# app.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="RedFlag SOC Dashboard", page_icon="🛡️", layout="wide")

# Initialize session state for storing data
if 'threats_detected' not in st.session_state:
    st.session_state.threats_detected = 47
if 'false_positive' not in st.session_state:
    st.session_state.false_positive = 12
if 'true_positive' not in st.session_state:
    st.session_state.true_positive = 35
if 'final_threat_count' not in st.session_state:
    st.session_state.final_threat_count = 35
if 'analysis_data' not in st.session_state:
    st.session_state.analysis_data = None

# Sidebar menu
st.sidebar.title("🌟 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Alert Analysis", "Threat Intelligence", "Reports", "Settings"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")
st.sidebar.metric("Active Alerts", "47", delta="12", delta_color="normal")
st.sidebar.metric("Response Time", "1.8s", delta="-0.5s", delta_color="inverse")
st.sidebar.markdown("---")
st.sidebar.info("💡 Upload a CSV file to analyze security alerts")

# Custom CSS for comforting theme
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Main background with soft gradient */
    .stApp {
        background: linear-gradient(135deg, #1a1f3a 0%, #2d3561 50%, #1a1f3a 100%);
        color: #e8eaf6;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers with soft glow */
    h1, h2, h3, h4, h5, h6 {
        color: #a5b4fc !important;
        text-shadow: 0 0 15px rgba(165, 180, 252, 0.3), 0 2px 4px rgba(0, 0, 0, 0.3);
        font-family: 'Poppins', sans-serif;
        letter-spacing: 2px;
    }
    
    /* Text with better readability */
    p, span, div, label {
        color: #e0e0e0 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* File uploader with enhanced styling */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%);
        border: 2px dashed rgba(165, 180, 252, 0.3);
        border-radius: 16px;
        padding: 30px;
        transition: all 0.4s ease;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.2);
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #a5b4fc;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4), 0 0 20px rgba(165, 180, 252, 0.25);
        transform: translateY(-3px);
    }
    
    [data-testid="stFileUploader"] label {
        color: #a5b4fc !important;
        font-weight: 600;
        font-size: 18px;
        text-shadow: 0 0 10px rgba(165, 180, 252, 0.3);
    }
    
    /* Buttons with glow effect */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 6px 24px rgba(139, 92, 246, 0.5);
    }
    
    /* Text inputs and text areas */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #2d3561;
        color: white;
        border: 2px solid #6366f1;
        border-radius: 12px;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #a5b4fc;
        box-shadow: 0 0 15px rgba(165, 180, 252, 0.3);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #252b47 0%, #2d3561 100%);
        border-right: 2px solid #6366f1;
        box-shadow: 2px 0 20px rgba(99, 102, 241, 0.2);
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] .element-container {
        color: #c7d2fe !important;
    }
    
    /* Metrics in sidebar */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: rgba(99, 102, 241, 0.15);
        padding: 10px;
        border-radius: 12px;
        border: 1px solid rgba(165, 180, 252, 0.3);
    }
    
    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: #6366f1;
        opacity: 0.3;
    }
    
    /* Main content area */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
        background: rgba(37, 43, 71, 0.4);
        border-radius: 24px;
        backdrop-filter: blur(10px);
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%);
        padding: 24px;
        border-radius: 16px;
        border: 1px solid rgba(165, 180, 252, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(165, 180, 252, 0.1);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #a5b4fc;
        box-shadow: 0 12px 48px rgba(99, 102, 241, 0.2), 0 0 0 1px rgba(165, 180, 252, 0.3);
    }
    
    /* Metric labels */
    [data-testid="stMetric"] label {
        color: #c7d2fe !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    
    /* Metric values */
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 32px !important;
        font-weight: 600 !important;
        text-shadow: 0 2px 8px rgba(165, 180, 252, 0.2);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%);
        padding: 30px;
        border-radius: 16px;
        border: 2px dashed rgba(165, 180, 252, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #a5b4fc;
        box-shadow: 0 0 30px rgba(165, 180, 252, 0.15);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 12px;
        font-weight: 500;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(139, 92, 246, 0.4);
    }
    
    /* Info boxes */
    .element-container .stAlert {
        background: rgba(99, 102, 241, 0.15);
        border-left: 4px solid #6366f1;
        color: #c7d2fe;
        border-radius: 8px;
    }
    
    /* Success messages */
    .element-container .stSuccess {
        background: rgba(34, 197, 94, 0.15);
        border-left: 4px solid #22c55e;
        color: #86efac;
        border-radius: 8px;
    }
    
    /* Radio buttons */
    [data-testid="stSidebar"] .row-widget.stRadio > div {
        background: rgba(99, 102, 241, 0.1);
        border-radius: 12px;
        padding: 5px;
    }
    
    /* Radio button labels */
    [data-testid="stSidebar"] .row-widget.stRadio label {
        color: #c7d2fe !important;
        padding: 10px 15px;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio label:hover {
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc !important;
    }
    
    /* Block container padding */
    .block-container {
        padding-top: 3rem;
        max-width: 1400px;
    }
    
    /* Title styling with animation */
    .main-title {
        font-size: 72px;
        font-weight: 700;
        color: #a5b4fc;
        text-align: center;
        text-shadow: 0 0 30px rgba(165, 180, 252, 0.4), 0 4px 8px rgba(0, 0, 0, 0.3);
        margin-bottom: 30px;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Custom card styling */
    .custom-card {
        background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%);
        padding: 28px;
        border-radius: 18px;
        margin: 15px 0;
        border: 1px solid rgba(165, 180, 252, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(165, 180, 252, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .custom-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: #a5b4fc;
        box-shadow: 0 16px 48px rgba(99, 102, 241, 0.3), 0 0 0 1px rgba(165, 180, 252, 0.4);
    }
    
    .custom-card h3 {
        color: #a5b4fc !important;
        margin-bottom: 12px;
        font-weight: 600;
    }
    
    .custom-card p {
        color: #c7d2fe;
        line-height: 1.7;
        margin: 8px 0;
    }
    
    .custom-card .metric-value {
        font-size: 48px;
        font-weight: 700;
        color: #ffffff;
        text-shadow: 0 2px 12px rgba(165, 180, 252, 0.3);
        margin: 15px 0;
    }
    
    /* Pulse animation for important metrics */
    @keyframes soft-pulse {
        0%, 100% {
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(165, 180, 252, 0.1);
        }
        50% {
            box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4), 0 0 24px rgba(165, 180, 252, 0.25);
        }
    }
    
    .pulse-card {
        animation: soft-pulse 4s ease-in-out infinite;
    }
    
    .subtitle {
        text-align: center;
        color: #c7d2fe;
        font-size: 20px;
        margin-bottom: 40px;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 400;
    }
    
    /* Upload section */
    .upload-section {
        background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%);
        border-left: 4px solid #6366f1;
        border-top: 4px solid #6366f1;
        border-radius: 16px;
        padding: 35px;
        margin-bottom: 50px;
        transition: all 0.4s ease;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.25);
    }
    
    .upload-section:hover {
        border-left-color: #a5b4fc;
        border-top-color: #a5b4fc;
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(99, 102, 241, 0.35), 0 0 30px rgba(165, 180, 252, 0.2);
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #6366f1, transparent);
        margin: 30px 0;
        opacity: 0.5;
    }
</style>
""", unsafe_allow_html=True)

# Main content based on selected page
if page == "Dashboard":
    # Main title
    st.markdown('<h1 class="main-title">🛡️ RedFlag SOC</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Advanced Security Operations Center | Real-Time Threat Analysis</p>', unsafe_allow_html=True)

    # Upload section
    st.subheader("📁 Upload logs")
    uploaded_file = st.file_uploader("Upload CSV file containing security alerts", type=['csv'])
    
    # Process file when uploaded
    if uploaded_file is not None:
        st.success('✅ File uploaded successfully!')
        st.info('📊 Analysis will be processed through the workflow')
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Create cards using containers with custom styling
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 25px; border-radius: 18px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center; box-shadow: 0 8px 32px rgba(99, 102, 241, 0.25); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-5px) scale(1.02)'; this.style.boxShadow='0 12px 48px rgba(99, 102, 241, 0.4)'" onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 8px 32px rgba(99, 102, 241, 0.25)'">
            <h1 style="color: #a5b4fc; margin: 0; font-size: 48px; text-shadow: 0 0 10px rgba(165, 180, 252, 0.3);">{st.session_state.threats_detected}</h1>
            <p style="color: #c7d2fe; font-size: 13px; margin: 10px 0 0 0; letter-spacing: 1px; font-weight: 600;">THREATS DETECTED</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 25px; border-radius: 18px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center; box-shadow: 0 8px 32px rgba(99, 102, 241, 0.25); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-5px) scale(1.02)'; this.style.boxShadow='0 12px 48px rgba(99, 102, 241, 0.4)'" onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 8px 32px rgba(99, 102, 241, 0.25)'">
            <h1 style="color: #a5b4fc; margin: 0; font-size: 48px; text-shadow: 0 0 10px rgba(165, 180, 252, 0.3);">{st.session_state.false_positive}</h1>
            <p style="color: #c7d2fe; font-size: 13px; margin: 10px 0 0 0; letter-spacing: 1px; font-weight: 600;">FALSE POSITIVE</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 25px; border-radius: 18px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center; box-shadow: 0 8px 32px rgba(99, 102, 241, 0.25); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-5px) scale(1.02)'; this.style.boxShadow='0 12px 48px rgba(99, 102, 241, 0.4)'" onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 8px 32px rgba(99, 102, 241, 0.25)'">
            <h1 style="color: #a5b4fc; margin: 0; font-size: 48px; text-shadow: 0 0 10px rgba(165, 180, 252, 0.3);">{st.session_state.true_positive}</h1>
            <p style="color: #c7d2fe; font-size: 13px; margin: 10px 0 0 0; letter-spacing: 1px; font-weight: 600;">TRUE POSITIVE</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 25px; border-radius: 18px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center; box-shadow: 0 8px 32px rgba(99, 102, 241, 0.25); transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-5px) scale(1.02)'; this.style.boxShadow='0 12px 48px rgba(99, 102, 241, 0.4)'" onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 8px 32px rgba(99, 102, 241, 0.25)'">
            <h1 style="color: #a5b4fc; margin: 0; font-size: 48px; text-shadow: 0 0 10px rgba(165, 180, 252, 0.3);">{st.session_state.final_threat_count}</h1>
            <p style="color: #c7d2fe; font-size: 13px; margin: 10px 0 0 0; letter-spacing: 1px; font-weight: 600;">FINAL THREAT COUNT</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Add Charts Section
    st.subheader("📊 Threat Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie Chart - Alert Distribution
        fig_pie = go.Figure(data=[go.Pie(
            labels=['True Positive', 'False Positive'],
            values=[st.session_state.true_positive, st.session_state.false_positive],
            marker=dict(colors=['#6366f1', '#a5b4fc']),
            hole=0.4
        )])
        fig_pie.update_layout(
            title="Alert Distribution",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c7d2fe', family='Poppins'),
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar Chart - Weekly Threat Trends
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        threats = [8, 12, 15, 9, 11, 6, 4]
        
        fig_bar = go.Figure(data=[go.Bar(
            x=days,
            y=threats,
            marker=dict(
                color=threats,
                colorscale=[[0, '#6366f1'], [1, '#a78bfa']],
                line=dict(color='#a5b4fc', width=2)
            )
        )])
        fig_bar.update_layout(
            title="Weekly Threat Detection",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c7d2fe', family='Poppins'),
            yaxis=dict(gridcolor='rgba(165, 180, 252, 0.1)'),
            xaxis=dict(gridcolor='rgba(165, 180, 252, 0.1)'),
            height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Line Chart - Threat Timeline
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate sample data for 24 hours
    hours = list(range(24))
    detected = np.random.randint(1, 10, 24)
    resolved = np.random.randint(1, 8, 24)
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=hours, y=detected,
        mode='lines+markers',
        name='Threats Detected',
        line=dict(color='#6366f1', width=3),
        marker=dict(size=8, color='#6366f1')
    ))
    fig_line.add_trace(go.Scatter(
        x=hours, y=resolved,
        mode='lines+markers',
        name='Threats Resolved',
        line=dict(color='#22c55e', width=3),
        marker=dict(size=8, color='#22c55e')
    ))
    
    fig_line.update_layout(
        title="24-Hour Threat Activity",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#c7d2fe', family='Poppins'),
        yaxis=dict(gridcolor='rgba(165, 180, 252, 0.1)', title="Count"),
        xaxis=dict(gridcolor='rgba(165, 180, 252, 0.1)', title="Hour"),
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_line, use_container_width=True)

elif page == "Alert Analysis":
    st.title("📊 Alert Analysis")
    st.write("Detailed analysis of security alerts")
    
    # Alert Analysis Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 20px; border-radius: 16px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center;">
            <h1 style="color: #a5b4fc; margin: 0;">156</h1>
            <p style="color: #c7d2fe; font-size: 12px; margin: 10px 0 0 0;">TOTAL ALERTS THIS WEEK</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 20px; border-radius: 16px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center;">
            <h1 style="color: #a5b4fc; margin: 0;">89%</h1>
            <p style="color: #c7d2fe; font-size: 12px; margin: 10px 0 0 0;">AUTO-TRIAGE SUCCESS RATE</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 20px; border-radius: 16px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center;">
            <h1 style="color: #a5b4fc; margin: 0;">23</h1>
            <p style="color: #c7d2fe; font-size: 12px; margin: 10px 0 0 0;">CRITICAL ALERTS</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Alert Severity Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        severity_data = pd.DataFrame({
            'Severity': ['Critical', 'High', 'Medium', 'Low'],
            'Count': [23, 45, 67, 21]
        })
        
        fig_severity = px.pie(
            severity_data,
            values='Count',
            names='Severity',
            color_discrete_sequence=['#ef4444', '#f97316', '#fbbf24', '#22c55e']
        )
        fig_severity.update_layout(
            title="Alert Severity Distribution",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c7d2fe', family='Poppins'),
            height=400
        )
        st.plotly_chart(fig_severity, use_container_width=True)
    
    with col2:
        # Alert Types
        alert_types = pd.DataFrame({
            'Type': ['Malware', 'Phishing', 'DDoS', 'Intrusion', 'Data Leak'],
            'Count': [34, 28, 19, 42, 12]
        })
        
        fig_types = go.Figure(data=[go.Bar(
            x=alert_types['Type'],
            y=alert_types['Count'],
            marker=dict(
                color=alert_types['Count'],
                colorscale=[[0, '#6366f1'], [1, '#8b5cf6']]
            )
        )])
        fig_types.update_layout(
            title="Alert Types",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c7d2fe', family='Poppins'),
            yaxis=dict(gridcolor='rgba(165, 180, 252, 0.1)'),
            xaxis=dict(gridcolor='rgba(165, 180, 252, 0.1)'),
            height=400
        )
        st.plotly_chart(fig_types, use_container_width=True)

elif page == "Threat Intelligence":
    st.title("🔍 Threat Intelligence")
    st.write("Real-time threat intelligence feeds and indicators")
    
    # Threat Intelligence Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 20px; border-radius: 16px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center;">
            <h1 style="color: #a5b4fc; margin: 0;">342</h1>
            <p style="color: #c7d2fe; font-size: 12px; margin: 10px 0 0 0;">MALICIOUS IPs BLOCKED</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 20px; border-radius: 16px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center;">
            <h1 style="color: #a5b4fc; margin: 0;">67</h1>
            <p style="color: #c7d2fe; font-size: 12px; margin: 10px 0 0 0;">THREAT ACTORS IDENTIFIED</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 20px; border-radius: 16px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center;">
            <h1 style="color: #a5b4fc; margin: 0;">1,234</h1>
            <p style="color: #c7d2fe; font-size: 12px; margin: 10px 0 0 0;">IOCs PROCESSED</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 20px; border-radius: 16px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center;">
            <h1 style="color: #a5b4fc; margin: 0;">15</h1>
            <p style="color: #c7d2fe; font-size: 12px; margin: 10px 0 0 0;">ACTIVE CAMPAIGNS</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Geographical Threat Map Data
    col1, col2 = st.columns(2)
    
    with col1:
        # Top Threat Sources
        countries = ['Russia', 'China', 'North Korea', 'Iran', 'Unknown']
        threat_count = [145, 98, 67, 52, 23]
        
        fig_countries = go.Figure(data=[go.Bar(
            y=countries,
            x=threat_count,
            orientation='h',
            marker=dict(
                color=threat_count,
                colorscale=[[0, '#6366f1'], [1, '#ef4444']]
            )
        )])
        fig_countries.update_layout(
            title="Top Threat Sources by Country",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c7d2fe', family='Poppins'),
            xaxis=dict(gridcolor='rgba(165, 180, 252, 0.1)'),
            height=400
        )
        st.plotly_chart(fig_countries, use_container_width=True)
    
    with col2:
        # Threat Categories
        categories = pd.DataFrame({
            'Category': ['Malware', 'Ransomware', 'Spyware', 'Rootkit', 'Trojan'],
            'Detections': [78, 45, 34, 23, 56]
        })
        
        fig_cat = px.pie(
            categories,
            values='Detections',
            names='Category',
            color_discrete_sequence=px.colors.sequential.Purples_r
        )
        fig_cat.update_layout(
            title="Threat Categories",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c7d2fe', family='Poppins'),
            height=400
        )
        st.plotly_chart(fig_cat, use_container_width=True)

elif page == "Reports":
    st.title("📄 Reports")
    st.write("Security reports and analytics")
    
    # Reports Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 20px; border-radius: 16px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center;">
            <h1 style="color: #a5b4fc; margin: 0;">48</h1>
            <p style="color: #c7d2fe; font-size: 12px; margin: 10px 0 0 0;">REPORTS GENERATED</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 20px; border-radius: 16px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center;">
            <h1 style="color: #a5b4fc; margin: 0;">98%</h1>
            <p style="color: #c7d2fe; font-size: 12px; margin: 10px 0 0 0;">COMPLIANCE SCORE</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 20px; border-radius: 16px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center;">
            <h1 style="color: #a5b4fc; margin: 0;">12</h1>
            <p style="color: #c7d2fe; font-size: 12px; margin: 10px 0 0 0;">INCIDENTS RESOLVED</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Monthly Performance Metrics
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    incidents = [23, 19, 28, 31, 25, 21]
    resolved = [21, 18, 26, 29, 24, 20]
    
    fig_performance = go.Figure()
    fig_performance.add_trace(go.Scatter(
        x=months, y=incidents,
        mode='lines+markers',
        name='Incidents',
        line=dict(color='#f97316', width=3),
        marker=dict(size=10)
    ))
    fig_performance.add_trace(go.Scatter(
        x=months, y=resolved,
        mode='lines+markers',
        name='Resolved',
        line=dict(color='#22c55e', width=3),
        marker=dict(size=10)
    ))
    
    fig_performance.update_layout(
        title="Monthly Incident Performance",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#c7d2fe', family='Poppins'),
        yaxis=dict(gridcolor='rgba(165, 180, 252, 0.1)'),
        xaxis=dict(gridcolor='rgba(165, 180, 252, 0.1)'),
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_performance, use_container_width=True)

elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("Configure dashboard settings and preferences")
    
    # Settings Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 20px; border-radius: 16px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center;">
            <h1 style="color: #a5b4fc; margin: 0;">5</h1>
            <p style="color: #c7d2fe; font-size: 12px; margin: 10px 0 0 0;">ACTIVE INTEGRATIONS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2d3561 0%, #3d4575 100%); padding: 20px; border-radius: 16px; border: 2px solid rgba(165, 180, 252, 0.3); text-align: center;">
            <h1 style="color: #a5b4fc; margin: 0;">8</h1>
            <p style="color: #c7d2fe; font-size: 12px; margin: 10px 0 0 0;">CONFIGURED WORKFLOWS</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("⚙️ System configuration and integration management")
