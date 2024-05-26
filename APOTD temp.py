import pytumblr
import requests

# Defining blog info
blog_name = 'BLOG_NAME_HERE' #Tumblr blog name
blog_identifier = 'BLOG_IDENTIFIER_HERE' # Obtain this from the Tumblr API Console and sending a request, should appear under 'uuid'
API_key = 'NASA_API_KEY_HERE' # Obtain by registering for an API key on the NASA API website
params = {
    'api_key': API_key,
    'concept_tags': True
}

# Defines the keys so values aren't necessarily hard-coded
# All can be obtained from the Tumblr API Console at 'Show Keys'
consumer_key = 'CONSUMER_KEY_HERE'
consumer_secret = 'CONSUMER_SECRET_KEY_HERE'
oauth_token = 'OAUTH_TOKEN_HERE'
oauth_token_secret = 'OAUTH_TOKEN_SECRET_HERE'

# Tumblr's OAuth authentication using the keys given by them when registering
client = pytumblr.TumblrRestClient(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
client.info()

# Get the relevant data from NASA's API
def get_info():
    GET_DATA = f'https://api.nasa.gov/planetary/apod?api_key={API_key}'
    response = requests.get(GET_DATA, params=params)
    if response.status_code == 200:
        result = response.json()
        concept_tags = result.get("concept_tags", [])
        title = result["title"]
        date = result["date"]
        caption = result["explanation"]
        image = result["url"]
        return title, date, caption, image, concept_tags

# Get APOD data
title, date, caption, image, concept_tags = get_info()

# Setting the post's tags
tags = ['astronomy', 'space', 'physics', 'STEM', 'NASA', 'APOTD', 'Astronomy Picture Of The Day']
for tag in tags:
   concept_tags.append(tag)

# Formats the post's caption appropriately
NASA_credit = "Credits: NASA's 'Astronomy Picture Of The Day.'"
post_caption = f"""
<div style="font-size: 30px;"><b>{title}, {date}</b></div>
<blockquote>{caption}</blockquote>
<p>{NASA_credit}</p> 
"""

# Create the post data
post_data = {
    'type': 'photo',
    'caption': post_caption,
    'source': image,
    'tags': concept_tags,
    'state': 'published'
}

# Actually posts to Tumblr
response = client.create_photo(blog_name, **post_data)

# Check if the request was successful
if response.get('id'):
    print('Post published successfully!')
else:
    print('Failed to publish post.')
    print('Response:', response)

