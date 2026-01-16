import json
import os
from datetime import datetime
import re
from scrapers.living_scraper import LivingScraper
from scrapers.caa_scraper import CAAScraper
from scrapers.portal_scraper import PortalScraper

def normalize(name):
    return name.lower().replace("university", "").replace("college", "").strip()

def normalize_name(text):
    """Convert to lowercase, underscores, no punctuation"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    text = re.sub(r'^_+|_+$', '', text)
    return text

def extract_institution_status(university_name):
    """Extract ACTIVE, REVOKED, or MERGED status from name"""
    name_upper = university_name.upper()
    if "REVOKED" in name_upper:
        return "REVOKED"
    elif "MERGED" in name_upper:
        return "MERGED"
    else:
        return "ACTIVE"

def extract_institution_type(university_name):
    """Extract institution type: University, College, Institute, Academy, School"""
    name_upper = university_name.upper()
    if "UNIVERSITY" in name_upper:
        return "University"
    elif "COLLEGE" in name_upper:
        return "College"
    elif "INSTITUTE" in name_upper:
        return "Institute"
    elif "ACADEMY" in name_upper:
        return "Academy"
    elif "SCHOOL" in name_upper:
        return "School"
    else:
        return "University"

def clean_whitespace(text):
    """Clean double spaces and unicode whitespace"""
    return " ".join(text.split())

def main():
    print("=== GradPilots UAE Education Intelligence Scraper ===")

    living = LivingScraper().scrape()
    caa = CAAScraper().scrape()
    portal = PortalScraper().scrape()

    output = {
        "metadata": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "scraper_version": "v1.0.0",
            "update_frequency": "Quarterly",
            "region_focus": "United Arab Emirates",
            "data_sources": {
                "government_accreditation": "https://www.caa.ae/Pages/Institutes/All.aspx",
                "course_catalogue": "https://www.bachelorsportal.com/search/universities/bachelor/united-arab-emirates",
                "cost_of_living": "https://www.universityliving.com/blog/student-finances/cost-of-living-in-dubai/"
            }
        },
        "country": {
            "name": "United Arab Emirates",
            "currency": "AED",
            "cost_of_living": living
        },
        "universities": []
    }

    index = {}

    for uni in caa:
        clean_name = clean_whitespace(uni["name"])
        status = extract_institution_status(clean_name)
        
        obj = {
            "university_name": clean_name,
            "normalized_name": normalize_name(clean_name),
            "institution_type": extract_institution_type(clean_name),
            "institution_status": status,
            "is_accredited_caa": False if status == "REVOKED" else True,
            "data_confidence": "HIGH",
            "confidence_reason": "Verified against official CAA accreditation list",
            "source_trace": {
                "caa_listed": True,
                "bachelorsportal_listed": False
            },
            "courses": []
        }
        output["universities"].append(obj)
        index[normalize(clean_name)] = obj

    for portal_uni, courses in portal.items():
        key = normalize(portal_uni)
        if key in index:
            index[key]["source_trace"]["bachelorsportal_listed"] = True
            index[key]["courses"].extend(courses)
        else:
            clean_name = clean_whitespace(portal_uni)
            status = extract_institution_status(clean_name)
            
            output["universities"].append({
                "university_name": clean_name,
                "normalized_name": normalize_name(clean_name),
                "institution_type": extract_institution_type(clean_name),
                "institution_status": status,
                "is_accredited_caa": False if status == "REVOKED" else True,
                "data_confidence": "MEDIUM",
                "confidence_reason": "Found on course portal, not verified with CAA",
                "source_trace": {
                    "caa_listed": False,
                    "bachelorsportal_listed": True
                },
                "courses": courses
            })

    os.makedirs("data", exist_ok=True)
    with open("data/uae_education_data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print("[SUCCESS] Scraping completed.")

if __name__ == "__main__":
    main()
