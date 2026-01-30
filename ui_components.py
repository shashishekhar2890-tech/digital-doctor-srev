import streamlit as st
import time
import random
import plotly.graph_objects as go

def apply_styles():
    """Reads and applies the CSS file."""
    try:
        with open("style.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def render_header():
    """Renders the branded header of the app."""
    col1, col2 = st.columns([1, 5])
    with col1:
        try:
            st.image("srev_logo.png", width=100)
        except Exception:
            st.markdown("### SREV")
    with col2:
        st.markdown("<h1 style='margin-bottom: 0; padding-top: 10px;'>SREV Digital Health Biopsy</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #4A5568; margin-top: -10px;'>Advanced Diagnostic System for Medical Practices</p>", unsafe_allow_html=True)
    st.markdown("---")

def render_scanning_animation():
    """Plays the scanning animation."""
    placeholder = st.empty()
    bar = st.progress(0)
    
    steps = [
        "Initializing Sterile Environment...",
        "Scanning SEO Vital Signs...",
        "Measuring Social Engagement Pulse...",
        "Analyzing Reputation Reflexes...",
        "Checking Website Response Time...",
        "Synthesizing Diagnostic Report..."
    ]
    
    for i, step in enumerate(steps):
        placeholder.markdown(f"<div class='scanning-text'>🩺 {step}</div>", unsafe_allow_html=True)
        progress = int((i + 1) / len(steps) * 100)
        bar.progress(progress)
        time.sleep(random.uniform(0.6, 1.2))
        
    placeholder.empty()
    bar.empty()

def render_guage_chart(score, title="Overall Health Score"):
    """Renders a Gauge Chart using Plotly."""
    
    # Determine Color
    if score > 80: color = "#38A169" # Green
    elif score > 50: color = "#DD6B20" # Orange
    else: color = "#E53E3E" # Red

    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 24, 'color': "#004A99"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#2D3748"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#E2E8F0",
            'steps': [
                {'range': [0, 50], 'color': '#FFF5F5'},
                {'range': [50, 80], 'color': '#FFFAF0'},
                {'range': [80, 100], 'color': '#F0FFF4'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", font = {'color': "#2D3748", 'family': "Inter"})
    st.plotly_chart(fig, use_container_width=True)

def render_section(title, data):
    """Renders a specific section of the report."""
    st.markdown(f"<div class='section-header'><h3>{title}</h3></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Section Score", f"{data.get('score', 0)}/100")
        # Show Proof of Life if available
        if 'page_title' in data.get('metrics', {}):
             title = data['metrics']['page_title']
             if title != "MISSING":
                 st.caption(f"✅ Verified & Scanned: *{title[:30]}...*")
             else:
                 st.error("⚠️ URL Access Failed")
        
    with col2:
        st.markdown("#### 🩺 Symptoms Detected")
        
        # Social CTA (UI Version)
        if "Pulse" in title or "Social" in title:
             st.error("⚠️ Profile not optimized to Meta Algorithms - Consult immediately for Content Analysis.")
        
        if data.get('symptoms'):
            for s in data['symptoms']:
                st.markdown(f"- 🔴 {s}")
        else:
            st.success("No critical symptoms detected in this system.")

    # Details Expander
    with st.expander("View Diagnostic Details"):
        st.json(data.get('metrics', {}))

def render_cta():
    """Renders the main CTA."""
    st.markdown("---")
    st.info("💡 **Treatment Plan Available**")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        **Condition Status: LOCKED**
        
        To access the full treatment plan including:
        - ✅ Specific code fixes for Speed
        - ✅ Content calendar for Socials
        - ✅ Reputation management scripts
        
        **Call +91-8860800507 to unlock.**
        """)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Request Immediate Consult", key="cta_btn"):
             st.success("Priority Ticket #9921 created.")

