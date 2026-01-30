import streamlit as st
import utils.audit_logic as audit
import json

# import utils.firebase_handler as fb
import ui_components as ui

# Page Config
st.set_page_config(
    page_title="SREV Evolution | Digital Health Audit",
    page_icon="🩺",
    layout="centered"
)

# Apply Styles
ui.apply_styles()

# Header
ui.render_header()

# State Management
if 'audit_results' not in st.session_state:
    st.session_state.audit_results = None

if 'audit_submitted' not in st.session_state:
    st.session_state.audit_submitted = False

# Main Form
if not st.session_state.audit_submitted:
    with st.container():
        st.markdown("### 📋 Patient Intake Form")
        st.write("Enter your practice details below for a comprehensive digital biopsy.")
        
        with st.form("intake_form"):
            hospital_name = st.text_input("Name of Practice / Hospital", placeholder="e.g. City Dental Care")
            website_url = st.text_input("Website URL", placeholder="https://www.example.com")
            
            col1, col2 = st.columns(2)
            with col1:
                gmb_link = st.text_input("Google Maps Link", placeholder="https://maps.app.goo.gl/...")
                insta_link = st.text_input("Instagram URL", placeholder="https://instagram.com/...")
            with col2:
                fb_link = st.text_input("Facebook URL", placeholder="https://facebook.com/...")
            
            submit_button = st.form_submit_button("🏥 Run Digital Biopsy")
            
            if submit_button:
                if hospital_name and website_url:
                    st.session_state.audit_submitted = True
                    # Store inputs temporarily in state if needed, but we pass them directly
                    st.session_state.inputs = {
                        "name": hospital_name,
                        "url": website_url,
                        "gmb": gmb_link,
                        "fb": fb_link,
                        "insta": insta_link
                    }
                    st.rerun()
                else:
                    st.error("Please provide at least a Practice Name and Website URL.")

# Audit Execution & Report Display
if st.session_state.audit_submitted and not st.session_state.audit_results:
    # Run Animation
    ui.render_scanning_animation()
    
    # Perform Audit
    inputs = st.session_state.inputs
    results = audit.perform_audit(
        inputs['name'], 
        inputs['url'], 
        inputs['gmb'], 
        inputs['fb'], 
        inputs['insta']
    )
    
    # Save to Backend (DISABLED)
    # fb.save_patient_file(results.copy())
    # fb.trigger_admin_email(results)
    
    # Update State
    st.session_state.audit_results = results
    st.rerun()

# Results View
if st.session_state.audit_results:
    res = st.session_state.audit_results
    
    display_score = res['health_score']
    
    # Score Dashboard
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("## Diagnosis Complete")
    ui.render_guage_chart(display_score)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Report Card
    if display_score > 80:
        st.success("Condition: STABLE. Minimal intervention required.")
    elif display_score > 50:
        st.warning("Condition: CRITICAL. Several vitals are weak.")
    else:
        st.error("Condition: EMERGENCY. Immediate structural resuscitation needed.")
    
    # Detailed Sections
    biopsy = res['digital_biopsy']
    ui.render_section("1. Structural Integrity (SEO & Speed)", biopsy['structural_integrity'])
    ui.render_section("2. Public Pulse (Reputation)", biopsy['public_pulse'])
    ui.render_section("3. Conversion Circulation (Leads)", biopsy['conversion_circulation'])
    ui.render_section("4. Meta Profile (Analytics)", biopsy['meta_profile'])
    
    # CTA & Download
    ui.render_cta()
    
    # Download Logic
    st.markdown("---")
    res_json = json.dumps(res, indent=4)
    st.download_button(
        label="📥 Download Full Report (JSON)",
        data=res_json,
        file_name=f"audit_report_{res['hospital_info']['name'].replace(' ', '_')}.json",
        mime="application/json"
    )
    
    if st.button("Start New Scan"):
        st.session_state.audit_submitted = False
        st.session_state.audit_results = None
        st.rerun()
