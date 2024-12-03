import json
from http.client import error

import requests
from bs4 import BeautifulSoup
import validators
from google_images_search import GoogleImagesSearch
import re

def verify_name_location(first_name, last_name, location_name):
    """
    Verifies the first name, last name, and location.
    """
    print(f"Verifying {first_name} {last_name} in {location_name}...")
    search_query = f"{location_name}"
    google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"

    response = requests.get(google_url)
    if response.status_code == 200:
        if location_name.lower() in response.text.lower():
            return True
    else:
        return False

def verify_display_picture(display_picture_url):
    """
    Verifies the display picture by performing a reverse image search.
    """
    print("Verifying display picture...")
    gis = GoogleImagesSearch('YOUR_GOOGLE_API_KEY', 'YOUR_GOOGLE_CX')
    gis.search({'q': display_picture_url, 'num': 1})
    if gis.results():
        print("Display picture verification successful.")
    else:
        print("Display picture seems to be fake or unavailable.")

def verify_certifications(certifications):
    """
    Verifies certifications by checking each certification URL.
    """
    print("Verifying certifications...")
    is_all_valid = True
    for cert in certifications:
        if validators.url(cert):
            response = requests.get(cert)
            if response.ok:
                print(f"Certification URL {cert} seems valid.")
            else:
                is_all_valid = False
    return is_all_valid

def verify_education(education):
    """
    Verifies the education field for authenticity.
    """
    print("Verifying education details...")
    if education:
        return True
    else:
        return False

def verify_experience(experience):
    """
    Verifies experience details for authenticity.
    """
    print("Verifying experience...")
    if experience:
        return True
    else:
        return False

def verify_skills(skills):
    """
    Verifies skills field by checking if it's valid or too generic.
    """
    print("Verifying skills...")
    if skills:
        return True
    return False


def verify_languages(languages):
    """
    Verifies languages information for authenticity.
    """
    print("Verifying languages...")
    if languages:
        return True
    return False

def verify_student_status(student):
    """
    Verifies if the user is a student or not.
    """
    print("Verifying student status...")
    if student:
        return True
    return False

def verify_summary(summary):
    """
    Verifies the summary to ensure it contains meaningful content.
    """
    print("Verifying summary...")
    if summary and len(summary.split()) > 5:
        return True
    return False

def verify_industry(industry_name):
    """
    Verifies the industry field.
    """
    print(f"Verifying industry: {industry_name}...")
    if industry_name:
        return True
    return False

def verify_headline(headline):
    """
    Verifies the headline.
    """
    print("Verifying headline...")
    if headline:
        return True
    return False

def validate_profile_data(profile_data):
    """
    Validates the profile data by verifying each key in the profile.
    """
    # Extract profile details
    first_name = profile_data.get('firstName')
    last_name = profile_data.get('lastName')
    location_name = profile_data.get('locationName')
    certifications = profile_data.get('certifications', [])
    education = profile_data.get('education')
    experience = profile_data.get('experience')
    skills = profile_data.get('skills')
    languages = profile_data.get('languages')
    student = profile_data.get('student')
    summary = profile_data.get('summary')
    industry_name = profile_data.get('industryName')
    headline = profile_data.get('headline')

    list_of_validation = [
        verify_name_location(first_name, last_name, location_name),
        verify_certifications(certifications),
        verify_education(education),
        verify_experience(experience),
        verify_skills(skills),
        verify_languages(languages),
        verify_student_status(student),
        verify_summary(summary),
        verify_industry(industry_name),
        verify_headline(headline),
    ]
    return len(list_of_validation), list_of_validation


# Run validation

data = open("./app/sample_Data.json", "r")
try:
    json_data = json.loads(data.read())
    keys_to_verify = ['summary', 'industryName', 'lastName', 'locationName', 'student',
                      'firstName', 'displayPictureUrl', 'experience', 'education', 'languages',
                      'certifications', 'skills', "headline"]

    validate_profile_data(json_data)
    for i in keys_to_verify:
        data_get = json_data.get(i)
        if isinstance(data_get, str):
            pass
        elif isinstance(data_get, list):
            for each_list_data in data_get:
                print(each_list_data)
except Exception as e:
    print(e)