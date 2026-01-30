import streamlit as st
import json
import ui_components as ui

try:
    import utils.audit_logic as audit
    import utils.pdf_generator as pdf_gen
    import utils.firebase_handler as fb
except ImportError as e:
    st.error(f"⚠️ Import Error: {e}")
    st.stop()

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
            col1, col2 = st.columns(2)
            with col1:
                hospital_name = st.text_input("Name of Practice / Hospital", placeholder="e.g. City Dental Care")
                contact_mobile = st.text_input("Contact Mobile", placeholder="+91-0000000000")
                website_url = st.text_input("Website URL", placeholder="https://www.example.com")
            
            with col2:
                gmb_link = st.text_input("Google Maps Link", placeholder="https://maps.app.goo.gl/...")
                insta_link = st.text_input("Instagram Username/URL", placeholder="@citydental")
                fb_link = st.text_input("Facebook Page URL", placeholder="https://facebook.com/citydental")
            
            # Email separate or with others
            contact_email = st.text_input("Email Address", placeholder="doc@clinic.com")

            st.write("")
            submit_button = st.form_submit_button("🏥 RUN DIGITAL BIOPSY", type="primary")
            
            if submit_button:
                if hospital_name and website_url:
                    st.session_state.audit_submitted = True
                    st.session_state.inputs = {
                        "name": hospital_name,
                        "mobile": contact_mobile,
                        "email": contact_email,
                        "url": website_url,
                        "gmb": gmb_link,
                        "fb": fb_link,
                        "insta": insta_link
                    }
                    st.rerun()
                else:
                    st.error("⚠️ Please provide at least a Practice Name and Website URL.")
            
            st.markdown("---")
            st.warning("""
                **DISCLAIMER & CLINICAL NOTE:** This Digital Health Biopsy is an indicative diagnostic report based on current algorithmic signals and publicly available data at the time of the scan. 
                While these findings highlight critical "Digital Leaks" and growth gaps, they do not constitute a complete performance strategy. 
                Digital health is dynamic; for a Full Prescription & Implementation Plan tailored to your clinic's specific revenue goals, a specialist consultation is required.
                
                **Don't leave your growth to chance. Consult the Digital Doctors now. 📞 Call/WhatsApp: +91-8860800507**
            """)
else:
    st.info("👈 Enter patient details in the sidebar to begin biometric scan.")

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
    
    # Save to Backend
    fb.save_patient_file(results.copy())
    fb.trigger_admin_email(results)
    
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
    
    # Generate PDF
    pdf_buffer = pdf_gen.generate_pdf_report(res)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📄 Download Medical Report (PDF)",
            data=pdf_buffer,
            file_name=f"SREV_Biopsy_{res['hospital_info']['name'].replace(' ', '_')}.pdf",
            mime="application/pdf",
            type="primary"
        )
    
    with col2:
        res_json = json.dumps(res, indent=4)
        st.download_button(
            label="📥 Download JSON Data",
            data=res_json,
            file_name=f"audit_raw_{res['hospital_info']['name'].replace(' ', '_')}.json",
            mime="application/json"
        )
    
    st.write("")
    if st.button("Start New Patient Scan"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --- ADMIN PANEL ---
with st.sidebar:
    st.markdown("---")
    with st.expander("🔐 Admin Access"):
        password = st.text_input("Enter Admin Password", type="password")
        
        if password == "srev2025":
            st.success("Access Granted")
            st.subheader("Patient Database")
            records = fb.get_all_records()
            if records:
                # Simplify for display
                display_data = []
                for r in records:
                    info = r.get('hospital_info', {})
                    display_data.append({
                        "Date": r.get('created_at', '')[:10],
                        "Hospital": info.get('name'),
                        "Score": r.get('health_score')
                    })
                
                st.dataframe(display_data)
                
                # Download All Logic
                full_json = json.dumps(records, indent=4)
                st.download_button("📥 Export Full DB", full_json, "srev_master_db.json", "application/json")
            else:
                st.info("No records found in Local DB.")
        elif password:
            st.error("⛔ Access Denied")
