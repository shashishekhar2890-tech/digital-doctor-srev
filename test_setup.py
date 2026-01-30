import utils.audit_logic as audit
import ui_components as ui
import utils.pdf_generator as pdf_gen

print("Imports successful.")

# Test Scrape (Safe URL)
print("Testing Web Scan on example.com...")
res = audit.analyze_seo("https://example.com")
print(f"SEO Scan Result: {res['score']}")
print(f"Symptoms: {res['symptoms']}")

print("Test complete.")
