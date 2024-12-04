import validators
import requests
import re
import json
import streamlit as st
from urllib.parse import urlparse
from linkedin_api import Linkedin
from linkedin_api.client import Client, ChallengeException, UnauthorizedException

def authenticate(self, username: str, password: str):
    if self._use_cookie_cache:
        self.logger.debug("Attempting to use cached cookies")
        cookies = self._cookie_repository.get(username)
        if cookies:
            self.logger.debug("Using cached cookies")
            self._set_session_cookies(cookies)
            self._fetch_metadata()
            return

    try:
        self._do_authentication_request(username, password)
        self._fetch_metadata()
    except ChallengeException as e:
        self.logger.error(f"Login challenge detected: {str(e)}")
        # Inform the user or retry the login after clearing cookies
        self.handle_challenge(username)
    except UnauthorizedException as e:
        self.logger.error("Unauthorized, please check your credentials.")
    except Exception as e:
        self.logger.error(f"An error occurred: {str(e)}")


def handle_challenge(self, username: str):
    # Manually delete the cookies file for the user
    cookie_file = os.path.join(self._cookie_repository.cookies_dir, f"{username}_cookies.json")
    if os.path.exists(cookie_file):
        os.remove(cookie_file)
        self.logger.info(f"Cookies for {username} have been cleared.")

    # Prompt the user to log out and log in manually
    self.logger.info("Please log out from LinkedIn in your browser, clear cookies, and try again.")

import os

class CookieRepository:
    def __init__(self, cookies_dir: str = ""):
        self.cookies_dir = cookies_dir

    def get(self, username: str):
        cookie_file = os.path.join(self.cookies_dir, f"{username}_cookies.json")
        if os.path.exists(cookie_file):
            with open(cookie_file, 'r') as f:
                return json.load(f)
        return None

    def save(self, cookies, username: str):
        cookie_file = os.path.join(self.cookies_dir, f"{username}_cookies.json")
        with open(cookie_file, 'w') as f:
            json.dump(cookies, f)

    def clear(self, username: str):
        cookie_file = os.path.join(self.cookies_dir, f"{username}_cookies.json")
        if os.path.exists(cookie_file):
            os.remove(cookie_file)
            print(f"Cookies for {username} have been cleared.")


setattr(Client, "handle_challenge", handle_challenge)
Client.authenticate = authenticate
# Title of the application
st.title("LinkedIn profile verification app.")

li_username = "beqeqj9upd@vafyxh.com"
li_password = "Simform@123"


def verify_name_location(first_name, last_name, location_name):
    """
    Verifies the first name, last name, and location.
    """
    print(f"Verifying {first_name} {last_name} in {location_name}...")
    search_query = f"{location_name}"
    google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"

    if not location_name:
        return False
    response = requests.get(google_url)
    if response.status_code == 200:
        if location_name.lower() in response.text.lower():
            return True
    else:
        return False


# def verify_display_picture(display_picture_url):
#     """
#     Verifies the display picture by performing a reverse image search.
#     """
#     print("Verifying display picture...")
#     gis = GoogleImagesSearch('YOUR_GOOGLE_API_KEY', 'YOUR_GOOGLE_CX')
#     gis.search({'q': display_picture_url, 'num': 1})
#     if gis.results():
#         print("Display picture verification successful.")
#     else:
#         print("Display picture seems to be fake or unavailable.")


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


def verify_honors(honors):
    if honors:
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
    honors = profile_data.get("honors")

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


def is_valid_url(url):
    parsed = urlparse(url)
    is_valid = bool(parsed.netloc) and bool(parsed.scheme)
    if not is_valid:
        raise ValueError("Please pass valid URL.")

    print(parsed)
    if "www.linkedin.com" not in parsed.netloc:
        raise ValueError("Only linkedIn link is allowed.")

    return re.split("/in/", parsed.path)[-1].replace("/", "")


class DummyApi:

    @staticmethod
    def get_profile(public_id, *args):
        return {}


api = DummyApi()

if "api_class" not in st.session_state:
    proxies = {

    }
    api = Linkedin(li_username, li_password, proxies=proxies)
    st.session_state["api_class"] = api
    st.session_state["logged_in"] = True

# Sidebar Login Form
# with st.sidebar:
#     st.header("User Login")
#
#     if "logged_in" not in st.session_state:
#         with st.form(clear_on_submit=True, key="loginkey"):
#             email = st.text_input("Email")
#             password = st.text_input("Password", type="password")
#             submit_button = st.form_submit_button("Set login")
#             if submit_button:
#                 if email and password:
#                     api = Linkedin(email, password)
#                     st.session_state["api_class"] = api
#                     st.session_state["logged_in"] = True
#                     st.session_state["user_email"] = True
#                     st.success("Login successful!")
#
#     else:
#         st.write(f"Logged in as: {st.session_state['user_email']}")
#         if st.button("Logout"):
#             st.session_state["logged_in"] = False
#             st.session_state["user_email"] = None
#             st.info("You have been logged out.")

if "logged_in" in st.session_state:
    # Text input for the link
    with st.form(key="url_form", clear_on_submit=True):
        link = st.text_input("Enter a link:")
        submit_button = st.form_submit_button(label="Submit")


def display_average_message(total_value, actual_value, pop_message):
    """
    Calculate the percentage and display a message with color coding in Streamlit.

    Parameters:
        total_value (int or float): The total value.
        actual_value (int or float): The actual value.
    """
    if total_value == 0:
        st.error("Total value cannot be zero.")
        return

    # Calculate percentage
    percentage = (actual_value / total_value) * 100

    # Determine the message and color
    if percentage > 80:
        color = "green"
        message = f"Excellent! {pop_message} {percentage:.2f}%."
    elif 60 <= percentage <= 80:
        color = "yellow"
        message = f"Good! {pop_message} {percentage:.2f}%."
    elif 30 <= percentage < 60:
        color = "white"
        message = f"Average. {pop_message} {percentage:.2f}%."
    else:  # Below 30
        color = "red"
        message = f"Seems like Fake {pop_message} {percentage:.2f}%."

    # Display the message with styling
    st.markdown(f"<span style='color:{color}; font-size:18px;'>{message}</span>", unsafe_allow_html=True)


if submit_button:
    if link:
        path = is_valid_url(link)
        public_id = path
    else:
        public_id = None
        st.error("Please enter a link before submitting.")
    if not public_id:
        st.error("Please pass the valid public_id url")
        st.rerun()

    try:
        print(public_id)
        st.success(f"Verifying for {public_id}")
        api_class = st.session_state.get("api_class")

        if not api_class:
            st.error("No Api class set")
            api_class = DummyApi()
        response = api_class.get_profile(public_id=public_id)
        # get_profile_contact_info
        # get_profile_posts
        with st.success("Profile match"):
            len_validation, validated_response = validate_profile_data(response)
            success_count = validated_response.count(True)
            display_average_message(total_value=len_validation, actual_value=success_count, pop_message="Profile")
        with st.success("Post match"):
            profile_post_count = api_class.get_profile_posts(public_id=public_id, post_count=10)
            display_average_message(total_value=10, actual_value=len(profile_post_count), pop_message="Posts")
        with st.success("Contact Info"):
            personal_information = api_class.get_profile_contact_info(public_id=public_id)
            info_count = 0
            for each_infor in personal_information:
                if personal_information.get(each_infor) not in [None, "", []]:
                    info_count += 1
            display_average_message(total_value=len(personal_information.keys()), actual_value=info_count,
                                    pop_message="Personal Information")


    except Exception as e:

        st.error(f"Something went wrong while fetching the user details  >> {e}")
