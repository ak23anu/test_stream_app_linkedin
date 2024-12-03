from linkedin_api import Linkedin
import getpass

print("Please enter your LinkedIn credentials first (2FA must be disabled)")
username = "lirow18058@bflcafe.com"
password = "Simform@123"

public_id = "akash-suthar-43aba576"

api = Linkedin(username, password)

my_public_id = public_id

my_posts = api.get_profile_posts(public_id=public_id)
import ipdb

ipdb.set_trace()
# get_profile_contact_info
# get_profile_skills
# get_profile
data = ['summary', 'industryName', 'lastName', 'locationName', 'student',
        'firstName', 'displayPictureUrl', 'experience', 'education', 'languages',
        'certifications', 'skills']
api.get_current_profile_views()
for post in my_posts:
    post_urn = post['socialDetail']['urn'].rsplit(':', 1)[1]
    print('POST:' + post_urn + '\n')
    comments = api.get_post_comments(post_urn, comment_count=100)
    for comment in comments:
        commenter = comment['commenter']['com.linkedin.voyager.feed.MemberActor']['miniProfile']
        print(f"\t{commenter['firstName']} {commenter['lastName']}: {comment['comment']['values'][0]['value']}\n")
