# import the requests library so we can use it to make REST calls (http://docs.python-requests.org/en/latest/index.html)
import requests

# import the json library.  This library provides handy features for formatting, displaying
# and manipulating json.
import json

# This is the text file with a list of email addresses to add as room members, one per line
fname = "/Users/ecoen/Desktop/ecoen.txt"

# This is the name of the Room that we want to add Members to
the_room = "Test Room"

# All of our REST calls will use the API URL for Cisco Spark as the base URL
# So lets define a variable for the Spark URL so we don't have to keep typing it
spark_url = "https://api.ciscospark.com/"

# This is your personal Spark API Access Token from your profile at:
# https://developer.ciscospark.com/?utm_source=Llab1&utm_medium=step2&utm_campaign=spark#
auth_token = "Bearer " + "this-would-be-your-really-long-access-token"

# These are the headers used for GET and POST for Spark
headers_get = {"Authorization": auth_token}
headers_post = {"Authorization": auth_token,"content-type": "application/json"}

# Thes URLs will be used later to GET the rooms list and to POST new memberships
get_spark_url = spark_url + "v1/rooms"
post_members_url = spark_url + "v1/memberships"

# Perform GET on get_spark_url and load response into a json object
get_rooms_response = requests.get(get_spark_url, headers=headers_get)
get_rooms_json = get_rooms_response.json()

# Now let's read some specific information from the json

# Set our parent as the top level response object
rooms_parent = get_rooms_json["items"]

# Look through each room returned for our specific Room and return the_room_id
for item in rooms_parent:
    if item["title"] == the_room:
        the_room_id = item["id"]
        break
else:
    raise ValueError("The room was not found!")

# Read our text file of email addresses into an array 
with open(fname, "r") as f:
    content = f.readlines()

# POST a Member Add to the_room_id in Spark for each email address in the array
for line in content:
    post_data = {"roomId": the_room_id,
               "personEmail": line[:len(line)-1],
               "isModerator": False
               }
    post_member_response = requests.post(post_members_url, data=json.dumps(post_data), headers=headers_post)
    print (line[:len(line)-1], post_member_response)

