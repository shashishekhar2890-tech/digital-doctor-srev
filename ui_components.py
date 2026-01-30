import streamlit as st
import time
import random

def apply_styles():
    """Reads and applies the CSS file."""
    try:
        with open("style.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

def render_header():
    """Renders the header of the app."""
    col1, col2 = st.columns([1, 4])
    with col1:
        # Placeholder for Logo
        st.write("🏥") # You could replace with st.image
    with col2:
        st.title("SREV Evolution")
        st.markdown("**Digital Health Audit System**")

def render_scanning_animation():
    """Plays the scanning animation."""
    placeholder = st.empty()
    bar = st.progress(0)
    
    steps = [
        "Initializing Sterile Environment...",
        "Checking SEO Vital Signs...",
        "Analyzing GMB Reflexes...",
        "Measuring Social Pulse...",
        "Examining Conversion Circulation...",
        "Finalizing Diagnosis..."
    ]
    
    for i, step in enumerate(steps):
        # Update text
        placeholder.markdown(f"<div class='scanning-text'>{step}</div>", unsafe_allow_html=True)
        # Update bar
        progress = int((i + 1) / len(steps) * 100)
        bar.progress(progress)
        time.sleep(random.uniform(0.5, 1.2)) # Random delay for realism
        
    placeholder.empty()
    bar.empty()

def render_guage_chart(score):
    """Renders a simple metric for the health score (Gauge future improvement)."""
    # Using simple metric for now, could use Plotly indicator later
    st.metric(label="Overall Health Score", value=f"{score}%", delta=None)

def render_section(title, data):
    """Renders a specific section of the report."""
    st.markdown(f"<h3 class='section-header'>{title}</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.metric("Section Score", f"{data['score']}/100")
        
    with col2:
        # Show Symptoms
        st.markdown("#### 🩺 Symptoms Detected")
        symptoms = data.get('symptoms', [])
        if symptoms:
            for s in symptoms:
                st.markdown(f"<div class='symptom-item'>{s}</div>", unsafe_allow_html=True)
        else:
            st.success("No critical symptoms detected in this area.")

        # Gated Cures
        st.markdown("#### 💊 Prescribed Cure")
        st.markdown("<div class='blur-content'>1. Fix H1 Tags on Home...<br>2. Optimize Image Sizes...<br>3. Add Schema Markup...</div>", unsafe_allow_html=True)
        st.info("🔒 Unlock full prescription by booking a consult.")

def render_cta():
    """Renders the main CTA."""
    st.markdown("---")
    st.markdown("### 📥 Download Your Full Prescription")
    st.write("Get the detailed step-by-step fix for all your digital symptoms.")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Book A Consult To Unlock"):
            st.balloons()
            st.success("Consultation Request Sent! Admin will contact you shortly.")
