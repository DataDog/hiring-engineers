import requests
import json

"""
This is a very simple wrapper script for
Riot Games' API. Here I will demonstrate 
how to gather a specific match information
for a specific user.

If you'd like to run this yourself, just make
sure to pip install requests and create an account
with Riot Games, it's a quick process. Their API
client can be found here https://developer.riotgames.com/
"""

API_KEY = "<REDACTED>"

# Going to use my friend's account for the data

summoner_name = "TinyKittens" # Yeah their in game name is TinyKittens :)

# We use the following endpoint with an API key 
# to get the summoner's data, more specifically
# Their PUUID which is used to query for their 
# match history

summoner_url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={API_KEY}"
summoner_response = requests.get(summoner_url)
summoner_data = summoner_response.json()

# The reponse is returned in json format, 
# from which I can extract a "puuid" to then 
# find the summoner's match list

summoner_puuid = summoner_data["puuid"]

# For simplicity's sake we'll only retrieve
# one of their matches.

match_list_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{summoner_puuid}/ids?start=0&count=1&api_key={API_KEY}"
match_list_response = requests.get(match_list_url)
match_list_data = match_list_response.json()
match_id = match_list_data[0]

# Now that we have a match_id, let's see
# what kind of data we can obtain from it!

match_timeline_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={API_KEY}"
match_timeline_reponse = requests.get(match_timeline_url)
match_timeline = match_timeline_reponse.json()

# Okay we have an entire json full of details
# from the match. Let's see what's in it

print(match_timeline.keys()) # dict_keys(['metadata', 'info'])

# Okay so we have the json's metadata and info.
# Let's see what we can find in the info tab

match_info = match_timeline["info"]
print(match_info.keys())
match_frames = match_info["frames"]
print(len(match_frames))

for frame in match_frames:
    print(frame.keys())

# It seems that the match information is broken down
# into frames. We have 17 of these intervals. Let's 
# now see what an interval looks like. I will output the 
# info from this interval into a .json file, since I now
# it's a lot of data.

frame = match_frames[7]
frame_1 = frame['participantFrames']
event_list1 = frame['events']

with open("frame_interval.json", "w") as file:
    json.dump(frame_1, file)

# If we now look at the file frame_interval.json, we can
# see all the data that just 1 frame out of the 17 looks
# like. We can also obtain ALL sorts of data from this,
# including even a player position on the map! Using Datadog
# we could certainly gather this data from millions of matches
# and be able to monitor for statistical anomalies for all of
# the hundreds of champions, items, and spells in the game.

with open("event_interval.json", "w") as file:
    json.dump(event_list1, file)

# We could also model the likelyhood of a victory or loss
# by analyzing specific, but important, events that happen
# in a match. For example a team is able to capture X objective
# at Y timestamp, suddenly their odds of winning might increase
# by 15%. Even further, it could also recommend courses of 
# action for the team based on historical data from these
# matches. The possibilities are endless.