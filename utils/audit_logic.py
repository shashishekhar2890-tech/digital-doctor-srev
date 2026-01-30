import requests
from bs4 import BeautifulSoup
import random
import time
import re
from fake_useragent import UserAgent
from datetime import datetime
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import concurrent.futures

# Suppress InsecureRequestWarning if using verify=False (common in scraping)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_session():
    """Creates a session with retry logic to improve stability."""
    session = requests.Session()
    # Reduced retries for SPEED, but keep backoff for stability
    retry = Retry(connect=2, read=2, redirect=2, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504, 429])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_random_header():
    """Generates a random User-Agent header."""
    try:
        ua = UserAgent()
        return {
            'User-Agent': ua.random, 
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://www.google.com/'
        }
    except:
        return {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def fetch_real_html_timed(url, retries=1):
    """Fetches real HTML and returns (soup, duration_seconds)."""
    if not url: return None, 0
    if not url.startswith('http'): url = 'https://' + url
    
    session = get_session()
    start_time = time.time()
    
    for i in range(retries + 1):
        try:
            # Minimal sleep for speed
            if i > 0: time.sleep(0.5) 
            response = session.get(url, headers=get_random_header(), timeout=5, verify=False)
            duration = time.time() - start_time
            if response.status_code == 200:
                return BeautifulSoup(response.content, 'html.parser'), duration
            elif response.status_code == 404:
                return None, duration # Page definitely doesn't exist
        except Exception as e:
            print(f"Attempt {i+1} failed for {url}: {e}")
            
    return None, time.time() - start_time

def fetch_pagespeed_data(url):
    """
    REAL LOGIC: Resource Analysis + Real TTFB (Server Response Time).
    """
    soup, duration = fetch_real_html_timed(url)
    
    if not soup:
        return _mock_pagespeed() 
        
    scripts = len(soup.find_all('script', src=True))
    images = len(soup.find_all('img'))
    styles = len(soup.find_all('link', rel='stylesheet'))
    total_requests = scripts + images + styles
    
    # Calculate Speed Score
    # Duration < 1.0s = Excellent, < 2.5s = Good, > 2.5s = Poor
    speed_score = 100
    if duration > 2.5: speed_score -= 40
    elif duration > 1.0: speed_score -= 15
    
    # Bloat penalty
    if total_requests > 80: speed_score -= 20
    
    return {
        "score": int(max(10, speed_score)),
        "metrics": {
            "server_response_time": f"{duration:.2f}s",
            "total_resources": total_requests,
            "scripts": scripts,
            "images_loaded": images
        }
    }

def _mock_pagespeed():
    return {
        "score": 0,
        "metrics": {"total_requests": "Unknown", "error": "Site Unreachable"}
    }

def analyze_seo(url):
    """Real SEO Analysis."""
    soup, _ = fetch_real_html_timed(url)
    symptoms = []
    score = 100
    metrics = {}
    
    if not soup:
        return {
            "score": 0, 
            "metrics": {"status": "Site access failed"}, 
            "symptoms": ["Could not access website (Check URL or Firewall)"]
        }
        
    # Title
    title = soup.title.string.strip() if soup.title and soup.title.string else None
    if title:
        metrics['page_title'] = title[:50] + "..." if len(title) > 50 else title
        if len(title) < 10 or len(title) > 65:
             symptoms.append(f"Title length improper ({len(title)} chars). Ideal: 30-65.")
             score -= 5
    else:
        symptoms.append("CRITICAL: Missing Title Tag.")
        score -= 30
        metrics['page_title'] = "MISSING"

    # Meta Description
    meta_desc = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    if meta_desc and meta_desc.get("content"):
        desc_len = len(meta_desc["content"])
        metrics['meta_desc_len'] = desc_len
        if desc_len < 50:
             symptoms.append("Meta Description too short.")
             score -= 5
    else:
        symptoms.append("CRITICAL: Missing Meta Description.")
        score -= 20
        metrics['meta_desc_len'] = 0

    # H-Tags
    h1s = soup.find_all('h1')
    h2s = soup.find_all('h2')
    metrics['h1_count'] = len(h1s)
    metrics['h2_count'] = len(h2s)
    
    if len(h1s) == 0:
        symptoms.append("CRITICAL: No H1 Tag found.")
        score -= 30
    elif len(h1s) > 1:
        symptoms.append(f"Multiple H1 Tags ({len(h1s)}) found. Confusing.")
        score -= 10
        
    if len(h2s) < 2:
        symptoms.append("Weak Content Structure (Few H2 headings).")
        score -= 5

    return {
        "score": max(0, score),
        "metrics": metrics,
        "symptoms": symptoms
    }

def analyze_social(links):
    """
    REAL SCRAPING with 'SOFT FAIL'.
    If scraping fails but page exists (200 OK), give 'Active' partial score.
    """
    score = 0
    metrics = {}
    symptoms = []
    
    # Instagram
    if links.get('insta'):
        url = links['insta']
        if not url.startswith('http'): url = 'https://www.instagram.com/' + url.replace('@', '')
        
        soup, _ = fetch_real_html_timed(url, retries=1)
        if soup:
            meta = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
            if meta and meta.get("content"):
                content = meta['content'] 
                metrics['ig_meta_data'] = content.split('-')[0].strip()
                
                followers_match = re.search(r'([\d\.,kKmM]+)\s+Followers', content)
                posts_match = re.search(r'([\d\.,kKmM]+)\s+Posts', content)
                
                followers = followers_match.group(1) if followers_match else "0"
                posts = posts_match.group(1) if posts_match else "0"
                
                metrics['ig_followers'] = followers
                metrics['ig_posts'] = posts
                
                if followers != "0": # Success
                    score += 50
                    if posts == "0": 
                         symptoms.append("Instagram exists but has 0 posts.")
                         score -= 10
                else:
                    # Partial Success (Page loaded but regex failed - likely private)
                    metrics['ig_status'] = "Active (Private)"
                    score += 40 
            else:
                # Page loaded, no meta (Login Wall) - Soft Fail
                metrics['ig_status'] = "Active (Login Block)"
                score += 40 
        else:
            symptoms.append("Instagram Link Unreachable.")
    else:
        symptoms.append("Missing Instagram Profile.")

    # Facebook
    if links.get('fb'):
        url = links['fb']
        soup, _ = fetch_real_html_timed(url, retries=1)
        if soup:
            meta = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
            title = soup.title.get_text() if soup.title else ""
            
            if meta and meta.get("content"):
                 text = meta['content']
                 metrics['fb_meta_data'] = text[:50] + "..."
                 score += 50
            elif "Facebook" in title:
                 # Soft Fail
                 metrics['fb_status'] = "Verified Page (Hidden Stats)"
                 score += 45
            else:
                 metrics['fb_status'] = "Page Accessible (Stats Hidden)"
                 score += 40
        else:
             symptoms.append("Facebook Page Unreachable.")
    else:
        symptoms.append("Missing Facebook Page.")
        
    score = min(score, 100)
    
    return {
        "score": score,
        "metrics": metrics,
        "symptoms": symptoms
    }

def analyze_gmb(link):
    """
    REAL GMB ANALYSIS.
    """
    score = 0
    symptoms = []
    metrics = {}
    
    if link:
        soup, _ = fetch_real_html_timed(link, retries=1)
        if soup:
            title = soup.title.get_text() if soup.title else "Unknown"
            metrics['gmb_name_found'] = title.replace(" - Google Maps", "")
            
            text = soup.get_text()
            rating_match = re.search(r'(\d\.\d)\s+stars', text)
            
            if rating_match:
                rating = float(rating_match.group(1))
                metrics['gmb_rating'] = rating
                if rating < 4.0:
                    symptoms.append(f"Low Reputation: {rating} Stars.")
                    score = 40
                else:
                    score = 95
            else:
                # Soft Fail
                if "Google Maps" in title:
                    metrics['status'] = "Verified (Ratings Hidden)"
                    score = 70 # Allow good score for just existing
                    symptoms.append("Rating hidden from public scan.")
                else:
                    score = 0
        else:
            symptoms.append("GMB Link Unreachable.")
            score = 0
    else:
        symptoms.append("No GMB Link provided.")
        
    return {
        "score": score,
        "metrics": metrics,
        "symptoms": symptoms
    }

def analyze_conversion(url):
    """CONVERSION INFRASTRUCTURE CHECK"""
    soup, _ = fetch_real_html_timed(url)
    if not soup:
        return {"score": 0, "metrics": {}, "symptoms": ["Site unreachable"]}
    
    html = str(soup).lower()
    score = 40 
    symptoms = []
    metrics = {}
    
    if 'tel:' in html:
        metrics['phone_link'] = "Detected"
        score += 20
    else:
        symptoms.append("Missing Click-to-Call Link.")
        
    if "book" in html or "appointment" in html or "schedule" in html:
        metrics['booking_keywords'] = "Detected"
        score += 20
    else:
        symptoms.append("No clear 'Book Appointment' wording.")
        
    if "whatsapp" in html or "chat" in html:
        metrics['chat_widget'] = "Detected"
        score += 20
    else:
        symptoms.append("No Live Chat/WhatsApp widget.")
        
    return {
        "score": min(100, score),
        "metrics": metrics,
        "symptoms": symptoms
    }

def analyze_meta_profile(url):
     """Checks Pixel, Analytics."""
     soup, _ = fetch_real_html_timed(url)
     if not soup: return {"score": 0, "metrics": {}, "symptoms": []}
     
     html_str = str(soup).lower()
     metrics = {}
     score = 50
     symptoms = []
     
     has_pixel = "fbq(" in html_str
     metrics['facebook_pixel'] = has_pixel
     if has_pixel: score += 25
     else: symptoms.append("No Facebook Pixel.")
     
     has_ga = "gtag(" in html_str
     metrics['google_analytics'] = has_ga
     if has_ga: score += 25
     else: symptoms.append("No Google Analytics.")
     
     return {
         "score": score,
         "metrics": metrics,
         "symptoms": symptoms
     }

def perform_audit(hospital_name, website_url, gmb_link, fb_link, insta_link):
    """
    PARALLEL EXECUTION.
    Runs scans concurrently to minimize wait time < 3s.
    """
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit all tasks
        social_links = {'insta': insta_link, 'fb': fb_link}
        
        # Web scan needs only one fetch really, but our logic splits them.
        # To optimize, we call 'audit_all_web' if we refactored, but for now parallelize the existing functions.
        # Note: fetch_real_html is called inside each. They will run in parallel.
        
        future_pagespeed = executor.submit(fetch_pagespeed_data, website_url)
        future_seo = executor.submit(analyze_seo, website_url)
        future_social = executor.submit(analyze_social, social_links)
        future_gmb = executor.submit(analyze_gmb, gmb_link)
        future_conversion = executor.submit(analyze_conversion, website_url)
        future_meta = executor.submit(analyze_meta_profile, website_url)
        
        # Gather Results
        pagespeed = future_pagespeed.result()
        seo = future_seo.result()
        public_pulse = future_social.result()
        gmb_data = future_gmb.result()
        conversion = future_conversion.result()
        meta = future_meta.result()
        
    structural_score = int((pagespeed['score'] + seo['score']) / 2)
    structural_details = {**pagespeed['metrics'], **seo['metrics']}
    
    pulse_score = int((public_pulse['score'] + gmb_data['score']) / 2)
    pulse_symptoms = public_pulse['symptoms'] + gmb_data['symptoms']
    pulse_metrics = {**public_pulse['metrics'], **gmb_data['metrics']}
    
    health_score = (
        (structural_score * 0.3) +
        (pulse_score * 0.3) +
        (conversion['score'] * 0.2) +
        (meta['score'] * 0.2)
    )
    
    return {
        "hospital_info": {
            "name": hospital_name,
            "website": website_url,
            "socials": social_links,
            "gmb": gmb_link
        },
        "health_score": int(health_score),
        "digital_biopsy": {
            "structural_integrity": {
                "score": structural_score,
                "metrics": structural_details,
                "symptoms": seo['symptoms']
            },
            "public_pulse": {
                "score": pulse_score,
                "metrics": pulse_metrics,
                "symptoms": pulse_symptoms
            },
            "conversion_circulation": conversion,
            "meta_profile": meta
        }
    }
