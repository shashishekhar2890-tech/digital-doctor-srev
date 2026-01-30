import requests
from bs4 import BeautifulSoup
import random
import time
import re

def fetch_pagespeed_data(url):
    """
    Fetches PageSpeed data. 
    Uses Google PageSpeed Insights API if key is present, else mocks it.
    """
    # Placeholder for API Key
    api_key = None # os.getenv('PAGESPEED_API_KEY')
    
    if api_key:
        # Real API Implementation
        try:
            endpoint = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&key={api_key}"
            response = requests.get(endpoint)
            data = response.json()
            score = data['lighthouseResult']['categories']['performance']['score'] * 100
            # Extract other metrics...
            return {
                "score": int(score),
                "metrics": {
                    "load_time": "2.4s", # Mock for now as extracting detailed metrics is complex
                    "ttfb": "0.1s"
                }
            }
        except Exception as e:
            print(f"PageSpeed API Error: {e}")
            return _mock_pagespeed()
    else:
        return _mock_pagespeed()

def _mock_pagespeed():
    """Returns realistic mock data for PageSpeed."""
    time.sleep(1) # Simulate network delay
    return {
        "score": random.randint(40, 95),
        "metrics": {
            "load_time": f"{random.uniform(1.5, 5.5):.1f}s",
            "ttfb": f"{random.uniform(0.05, 0.5):.2f}s",
            "first_paint": f"{random.uniform(1.0, 3.0):.1f}s"
        }
    }

def analyze_seo(url):
    """Checks basic SEO tags from the website HTML."""
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        has_title = bool(soup.title and soup.title.string)
        title_length = len(soup.title.string) if has_title else 0
        has_meta_desc = bool(soup.find("meta", attrs={"name": "description"}))
        has_h1 = bool(soup.find("h1"))
        
        score = 0
        symptoms = []
        
        if has_title:
            score += 40
            if title_length < 30 or title_length > 60:
                symptoms.append("Title tag length is suboptimal (Ideal: 30-60 chars)")
        else:
            symptoms.append("Missing Title Tag (Critical Condition)")
            
        if has_meta_desc:
            score += 30
        else:
            symptoms.append("Missing Meta Description")
            
        if has_h1:
            score += 30
        else:
            symptoms.append("Missing H1 Header")
            
        return {
            "score": score,
            "metrics": {
                "title_found": has_title,
                "meta_desc_found": has_meta_desc,
                "h1_found": has_h1
            },
            "symptoms": symptoms
        }
    except Exception as e:
        return {
            "score": 0,
            "metrics": {},
            "symptoms": ["Could not access website for analysis"]
        }

def analyze_social(links):
    """Analyzes social media presence."""
    score = 0
    metrics = {}
    symptoms = []
    
    # Check GMB
    if links.get('gmb'):
        score += 40
        metrics['gmb_found'] = True
    else:
        symptoms.append("No Google My Business link provided")
        
    # Check Socials
    social_count = 0
    if links.get('instagram'): social_count += 1
    if links.get('facebook'): social_count += 1
    
    if social_count > 0:
        score += 30 * social_count
    else:
        symptoms.append("Weak Social Pulse (No FB/Insta)")
        
    # Cap score
    score = min(score, 100)
    
    return {
        "score": score,
        "metrics": {"social_platforms": social_count},
        "symptoms": symptoms
    }

def analyze_conversion(url):
    """Simulates checking for conversion elements."""
    # In a real app, strict scraping. Here we assume some random distribution or simple checks if possible.
    # We'll do a mock check based on randomness for demo purposes or simplistic scraping.
    
    score = 50
    symptoms = []
    
    # Randomly assign issues for demonstration "Diagnosis"
    issues = [
        "No clear 'Book Now' CTA above the fold",
        "Missing chat widget for immediate triage",
        "Phone number not clickable"
    ]
    
    detected_issues = random.sample(issues, k=random.randint(0, 2))
    score -= len(detected_issues) * 20
    
    return {
        "score": max(0, score),
        "metrics": {"conversion_elements": "Moderate"},
        "symptoms": detected_issues
    }

def analyze_meta_profile(url):
     """Simulates checking for pixel/analytics."""
     # Mock implementation
     return {
         "score": 80,
         "metrics": {"fb_pixel": True, "ga4": True},
         "symptoms": [] 
     }

def perform_audit(hospital_name, website_url, gmb_link, fb_link, insta_link):
    """Orchestrates the full audit."""
    
    # 1. Structural Integrity
    pagespeed = fetch_pagespeed_data(website_url)
    seo = analyze_seo(website_url)
    structural_score = (pagespeed['score'] + seo['score']) / 2
    
    # 2. Public Pulse
    social_links = {'gmb': gmb_link, 'facebook': fb_link, 'instagram': insta_link}
    public_pulse = analyze_social(social_links)
    
    # 3. Conversion Circulation
    conversion = analyze_conversion(website_url)
    
    # 4. Meta Profile
    meta = analyze_meta_profile(website_url)
    
    # Calculate Overall Health Score
    # Weights: Structural 30%, Public 30%, Conversion 20%, Meta 20%
    health_score = (
        (structural_score * 0.3) +
        (public_pulse['score'] * 0.3) +
        (conversion['score'] * 0.2) +
        (meta['score'] * 0.2)
    )
    
    return {
        "hospital_info": {
            "name": hospital_name,
            "website": website_url,
            "socials": social_links
        },
        "health_score": int(health_score),
        "digital_biopsy": {
            "structural_integrity": {
                "score": int(structural_score),
                "details": {**pagespeed, **seo}
            },
            "public_pulse": public_pulse,
            "conversion_circulation": conversion,
            "meta_profile": meta
        }
    }
