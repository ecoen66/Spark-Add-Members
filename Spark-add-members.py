# import the requests library so we can use it to make REST calls (http://docs.python-requests.org/en/latest/index.html)
import requests

# import the json library.  This library provides handy features for formatting, displaying
# and manipulating json.
import json

# This is the text file with a list of email addresses to add as room members, one per line
fname = "/Users/ecoen/Desktop/ecoen.txt"

# This is the name of the Room that we want to add Members to
the_room = "Test Room"

# All of our REST calls will use the API url for Cisco Spark as the base URL
# So lets define a variable for the Spark URL so we don't have to keep typing it
rooms_url = "https://api.ciscospark.com/"

# This is your personal Spark API Access Token from your profile at:
# https://developer.ciscospark.com/?utm_source=Llab1&utm_medium=step2&utm_campaign=spark#
auth_token = "Bearer " + "this-would-be-your-really-long-access-token"

# These are the headers used for GET and POST for Spark
headers = {"Authorization": auth_token}
headers_put = {"Authorization": auth_token,'content-type': 'application/json'}

# Get Rooms
# This function allows you to view a list of all the rooms that you belong to
get_rooms_url = rooms_url + 'v1/rooms'
post_members_url = rooms_url + 'v1/memberships'

# Perform GET on get_rooms_url and load response into a json object
get_rooms_response = requests.get(get_rooms_url, headers=headers)
get_rooms_json = get_rooms_response.json()

# Now let's read and display some specific information from the json

# set our parent as the top level response object
rooms_parent = get_rooms_json["items"]

# print("Rooms = ")

# for each room returned, print the roomId, and look for a specific Room
for item in rooms_parent:
#    print(item["title"], item["id"])
    if item["title"] == the_room:
        the_room_id = item["id"]

with open(fname) as f:
    content = f.readlines()

for line in content:
    post_data = {"roomId": the_room_id,
               "personEmail": line[:len(line)-1],
               "isModerator": False
               }
    put_member_response = requests.post(post_members_url, data=json.dumps(post_data), headers=headers_put)
    print (line[:len(line)-1], put_member_response)

