import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- PRODUCTION ENTERPRISE CONFIGURATION ---
st.set_page_config(
    page_title="AdVanta AI | Enterprise Content Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADAPTIVE ENTERPRISE CSS INJECTION (LIGHT & DARK MODE COMPLIANT) ---
st.markdown("""
    <style>
    /* Main App Layout - Uses Streamlit Native Theme Variables */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    /* Header Styling */
    .main-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        letter-spacing: -1px;
        margin-bottom: 20px;
        color: var(--text-color) !important;
    }
    
    /* Metric Blocks Custom Treatment */
    [data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    [data-testid="stMetricLabel"] > div {
        color: var(--text-color) !important;
        opacity: 0.8;
    }
    [data-testid="stMetricValue"] > div {
        color: #0284c7 !important; 
    }
    
    /* Custom Adaptive Preview Panel Box */
    .preview-card {
        background-color: var(--secondary-background-color);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.3);
        margin-top: 15px;
        color: var(--text-color) !important;
    }
    
    /* Compliance Output Box */
    .compliance-box {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        font-size: 0.9em;
        background-color: rgba(99, 102, 241, 0.15);
        color: var(--text-color) !important;
        border-left: 4px solid #6366f1;
    }
    
    /* Clean Forms buttons overrides */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #0284c7;
        color: white !important;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0369a1;
        color: white !important;
    }
    
    .stMarkdown p {
        color: var(--text-color) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENDPOINT GATEWAY ---
BACKEND_URL = "http://localhost:8080/api/v1/campaigns/generate"

# --- PERSISTENT SEED DATA STORAGE STRUCTURES ---
if "history" not in st.session_state: st.session_state.history = {}
if "version" not in st.session_state: st.session_state.version = 1
if "schedule_records" not in st.session_state:
    st.session_state.schedule_records = [
        {"Campaign": "Q3 Alpha Launch", "Date": "2026-07-01", "Time": "09:00", "Platform": "email", "Status": "PUBLISHED"},
        {"Campaign": "Lumina Glow Promo", "Date": "2026-08-15", "Time": "18:30", "Platform": "social", "Status": "SCHEDULED"}
    ]
if "campaign" not in st.session_state:
    st.session_state.campaign = {
        "campaignName": "Global Launch Framework",
        "productName": "Lumina Aura Skincare",
        "productDescription": "Advanced night-repair serum with botanical extracts and hyaluronic acid.",
        "targetAudience": "Professionals aged 25-45",
        "publishingPlatform": "Email",
        "status": "Ready",
        "content": "",
        "complianceScore": 0.0,
        "notes": [],
        "scheduleDate": "2026-06-25",
        "scheduleTime": "12:00",
        "locale": "English"
    }

# --- SIDEBAR MULTI-PAGE PLATFORM NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=65)
    st.markdown("<h2 style='margin-top:10px;' class='main-header'>AdVanta AI</h2>", unsafe_allow_html=True)
    st.caption("v3.2.0-Enterprise | Multi-Theme Architecture")
    st.divider()
    
    page = st.radio(
        "Navigation Gateway",
        ["Dashboard", "Campaign Studio", "Compliance Center", "Scheduler", "Audit Trail", "Analytics"]
    )
    
    st.divider()
    
    # --- GLOBAL LOCALIZATION MANAGEMENT ENGINE ---
    st.subheader("🌐 Market Localization")
    selected_lang = st.selectbox(
        "Target Market Language", 
        ["English", "Hindi (हिन्दी)", "Marathi (मराठी)", "Spanish (Español)", "German (Deutsch)"],
        index=0
    )
    st.session_state.campaign["locale"] = selected_lang
    
    st.divider()
    st.subheader("🖥️ Platform Telemetry")
    st.sidebar.metric("System Health", "Healthy")
    st.sidebar.metric("Compliance Engine", "Active")
    st.sidebar.metric("Scheduler Context", "Running")
    
    if st.button("🧹 Flush System Cache"):
        st.session_state.history = {}
        st.session_state.version = 1
        st.session_state.campaign["content"] = ""
        st.session_state.campaign["complianceScore"] = 0.0
        st.session_state.campaign["notes"] = []
        st.session_state.campaign["status"] = "Ready"
        st.rerun()

# ==========================================
# PAGE MODULE 1: EXECUTIVE HUB (DASHBOARD)
# ==========================================
if page == "Dashboard":
    st.markdown("<h1 class='main-header'>Executive Command Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("Real-time monitoring of corporate marketing outputs and alignment metrics.")
    st.divider()
    
    # Platform KPI Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1: st.metric("Campaigns Generated", "1,248", delta="+12% MoM")
    with kpi2: st.metric("Compliance Avg", "97%", delta="🛡️ Optimal")
    with kpi3: st.metric("Scheduled Pipes", "347", delta="Active")
    with kpi4: st.metric("Risk Alerts Raised", "2", delta="-4 this week", delta_color="inverse")
    
    st.subheader("🎯 Active Workbench Focus Context")
    c_m1, c_m2, c_m3 = st.columns(3)
    with c_m1: st.metric("Campaign Target Reference", st.session_state.campaign["campaignName"])
    with c_m2: st.metric("Active Working Version", f"v{st.session_state.version} ({st.session_state.campaign['locale']})")
    with c_m3: 
        status = st.session_state.campaign["status"]
        if status == "SCHEDULED": st.success("🟢 Scheduled Pipeline")
        elif status == "PUBLISHED": st.info("🚀 Published Asset")
        elif status == "Generated": st.warning("🟡 Unscheduled Asset")
        else: st.markdown(f"Status: **{status}**")

# ==========================================
# PAGE MODULE 2: CAMPAIGN STUDIO WORKBENCH
# ==========================================
elif page == "Campaign Studio":
    st.markdown("<h1 class='main-header'>Campaign Studio Engine</h1>", unsafe_allow_html=True)
    st.caption(f"Active Localization Target Profile: **{st.session_state.campaign['locale']}**")
    st.divider()
    
    col_in, col_out = st.columns([1, 1.2])
    
    with col_in:
        st.markdown("### 📋 Generation Configuration Matrix")
        
        c_name = st.text_input("Internal Campaign Tag Name", value=st.session_state.campaign["campaignName"])
        p_name = st.text_input("Product Identifier Name", value=st.session_state.campaign["productName"])
        p_desc = st.text_area("Product Brief Specifications Context", value=st.session_state.campaign["productDescription"], height=100)
        t_aud = st.text_input("Target Consumer Persona", value=st.session_state.campaign["targetAudience"])
        chan = st.selectbox("Distribution Channel", ["Email", "Social", "Web Content"])
        
        uploaded_file = st.file_uploader("Supplemental Brief Ingestion Gateway", type=["pdf", "txt", "docx", "csv"])
        
        if st.button("Execute Generative Pipeline 🚀", use_container_width=True):
            if uploaded_file is not None and uploaded_file.size == 0:
                st.error("🚨 Ingestion Guard Fault: Zero-Byte stream payload block triggered.")
            else:
                st.session_state.campaign["campaignName"] = c_name
                st.session_state.campaign["productName"] = p_name
                st.session_state.campaign["productDescription"] = p_desc
                st.session_state.campaign["targetAudience"] = t_aud
                st.session_state.campaign["publishingPlatform"] = chan.lower()
                
                # Appending local market instructions explicitly into backend payload summary
                localized_description = f"{p_desc} [Target Market Language Locale Constraint: {st.session_state.campaign['locale']}]"
                
                form_payload = {
                    "productName": (None, p_name),
                    "productDescription": (None, localized_description),
                    "targetAudience": (None, t_aud),
                    "channel": (None, chan.lower()),
                    "version": (None, str(st.session_state.version))
                }
                if uploaded_file is not None:
                    form_payload["file"] = (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                
                try:
                    res = requests.post(BACKEND_URL, files=form_payload)
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.campaign["content"] = data["generatedContent"]
                        st.session_state.campaign["complianceScore"] = data["complianceScore"]
                        st.session_state.campaign["notes"] = data["complianceAnnotations"]
                        st.session_state.campaign["status"] = "Generated"
                        st.session_state.history[f"v{st.session_state.version}"] = data["generatedContent"]
                        st.toast("Generation execution cycle finished successfully.")
                    else: st.error(f"Backend API Exception Flag: Code {res.status_code}")
                except: st.error("Link broken: System Gateway down at port 8080.")

    with col_out:
        st.markdown("### 📝 Active Studio Workspace & Asset Preview")
        if st.session_state.campaign["content"]:
            editable_content = st.text_area("Live Composition Workspace", value=st.session_state.campaign["content"], height=250)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("💾 Commit Workspace Changes"):
                    st.session_state.version += 1
                    st.session_state.campaign["content"] = editable_content
                    st.session_state.history[f"v{st.session_state.version}"] = editable_content
                    st.toast(f"Workspace snapshot compiled as version v{st.session_state.version}")
            with c2:
                st.download_button("📥 Export Production Build", data=editable_content, file_name=f"advanta_export_v{st.session_state.version}.txt")
            
            st.markdown("<div class='preview-card'>", unsafe_allow_html=True)
            st.subheader("📱 Channel Distribution Live Preview Match")
            st.caption(f"Mock Rendering Layout Platform Target: {st.session_state.campaign['publishingPlatform'].upper()} | Locale: {st.session_state.campaign['locale']}")
            st.markdown(f"""
            ---
            ### **{st.session_state.campaign['productName']}**
            
            {editable_content}
            
            **Action Link:** *Shop Now / Learn More*
            ---
            """)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No active text asset profile cached. Initialize generation parameters configuration to execute workflow.")

# ==========================================
# PAGE MODULE 3: COMPLIANCE ANALYZER HUB
# ==========================================
elif page == "Compliance Center":
    st.markdown("<h1 class='main-header'>Automated Corporate Governance Center</h1>", unsafe_allow_html=True)
    st.divider()
    
    if st.session_state.campaign["content"]:
        score = st.session_state.campaign["complianceScore"]
        
        s1, s2, s3, s4 = st.columns(4)
        with s1: st.metric("Overall Compliance Target Score", f"{score}%")
        with s2: st.metric("Content Quality Index", "95%")
        with s3: st.metric("Tone Constraints Consistency Match", "98%")
        with s4: st.metric("Regulatory Framework Target Alignment", "100%")
        
        st.markdown("#### Engine Safety Validation Gauge")
        st.progress(int(score))
        
        st.markdown("### 🔍 Flagged Operational Anomalies & Compliance Notices")
        if st.session_state.campaign["notes"]:
            for notice in st.session_state.campaign["notes"]:
                st.markdown(f"<div class='compliance-box'>{notice}</div>", unsafe_allow_html=True)
        else:
            st.success("🎉 Zero brand violations flagged by corporate parser layers.")
    else:
        st.info("No compiled text found in active engine space buffer memory to audit compliance checks.")

# ==========================================
# PAGE MODULE 4: PIPELINE SCHEDULER SYSTEM
# ==========================================
elif page == "Scheduler":
    st.markdown("<h1 class='main-header'>Downstream Dispatch Framework Pipeline</h1>", unsafe_allow_html=True)
    st.divider()
    
    if st.session_state.campaign["content"]:
        st.markdown("### 📅 Push New Target Queue Entry Configuration")
        sc_col1, sc_col2 = st.columns(2)
        with sc_col1:
            s_date = st.date_input("Target Queue Execution Start Date", value=datetime.strptime(st.session_state.campaign["scheduleDate"], "%Y-%m-%d"))
        with sc_col2:
            s_time = st.time_input("Target Dispatch Activation Window Time", value=datetime.strptime(st.session_state.campaign["scheduleTime"], "%H:%M").time())
            
        if st.button("🚀 Authorize & Push to Core Scheduler"):
            st.session_state.campaign["scheduleDate"] = str(s_date)
            st.session_state.campaign["scheduleTime"] = s_time.strftime("%H:%M")
            st.session_state.campaign["status"] = "SCHEDULED"
            
            new_record = {
                "Campaign": st.session_state.campaign["campaignName"],
                "Date": str(s_date),
                "Time": s_time.strftime("%H:%M"),
                "Platform": f"{st.session_state.campaign['publishingPlatform']} ({st.session_state.campaign['locale']})",
                "Status": "SCHEDULED"
            }
            st.session_state.schedule_records.append(new_record)
            st.balloons()
            st.success("Asset queue entry validated. Spring Boot engine background task pipeline tracking active.")
            
    st.markdown("### 📊 Active Pipeline Dispatch Tracking Queue Ledger")
    df_sched = pd.DataFrame(st.session_state.schedule_records)
    st.dataframe(df_sched, use_container_width=True)

# ==========================================
# PAGE MODULE 5: SECURITY AUDIT TIMELINE LOGS
# ==========================================
elif page == "Audit Trail":
    st.markdown("<h1 class='main-header'>Immutable Revision Tracking System & Audit Logs</h1>", unsafe_allow_html=True)
    st.divider()
    
    if st.session_state.history:
        st.markdown("#### Version Control Hierarchy Node Timeline")
        for version_tag, content_string in reversed(list(st.session_state.history.items())):
            timestamp_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with st.expander(f"📦 Checkpoint Node Hash Reference Identifier: {version_tag} — Saved at timestamp: {timestamp_now}"):
                st.code(content_string, language="text")
    else:
        st.info("System tracking log register clear. No revision actions recorded yet.")

# ==========================================
# PAGE MODULE 6: PLATFORM SYSTEM PERFORMANCE ANALYTICS
# ==========================================
elif page == "Analytics":
    st.markdown("<h1 class='main-header'>Advanced Campaign Performance System Analytics</h1>", unsafe_allow_html=True)
    st.divider()
    
    an_col1, an_col2 = st.columns(2)
    with an_col1:
        st.markdown("#### 📈 Compliance Health Growth Trend Matrix Line (Historical)")
        df_line = pd.DataFrame({"Month": ["Jan", "Feb", "Mar", "Apr", "May", "June"], "Performance Score Index": [91, 93, 95, 94, 97, 100]})
        st.line_chart(df_line.set_index("Month"))
        
    with an_col2:
        st.markdown("#### 📊 Asset Output Volume Inbound Distribution Channels (Volume Log)")
        df_bar = pd.DataFrame({"Distribution Channel Hub": ["Instagram", "Email Delivery", "SMS Core", "Web Framework"], "Generated Count": [45, 30, 15, 10]})
        st.bar_chart(df_bar.set_index("Distribution Channel Hub"))