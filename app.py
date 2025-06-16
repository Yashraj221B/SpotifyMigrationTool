""" 
This is a simple application to migrate spotify playlists from one account to another.
The application uses the Spotify API to get the playlists from the source account and add them to the destination account.
The application uses the requests library to interact with the Spotify API.
The application uses the json library to parse the JSON responses from the Spotify API.
The application uses the base64 library to encode the client_id and client_secret for the Spotify API.

By: Yashraj221B
Date: 2024-03-28
Last Updated: 2024-11-27
Email: developer221b@gmail.com
"""

import html
import json
import time
import base64
import colorama
import requests
import webbrowser
from inspect import getframeinfo, currentframe
# import tqdm

class Logger:
    """
    A class that provides logging functionality for the server.
    """
    def __init__(self) -> None:
        colorama.init()
        self.BLUE = colorama.Fore.BLUE
        self.RED = colorama.Fore.RED
        self.YELLOW = colorama.Fore.YELLOW
        self.GREEN = colorama.Fore.GREEN
        self.WHITE = colorama.Fore.WHITE

    def logInfo(self, msg):
        """
        Logs an informational message.

        Args:
        - msg (str): The message to log.
        """
        print(self.BLUE + "[ℹ️INFO] " + self.WHITE + msg)

    def logError(self, msg):
        """
        Logs an error message.

        Args:
        - msg (str): The message to log.
        """
        print(self.RED + "[❌ERROR] " + self.WHITE + msg)

    def logWarning(self, msg):
        """
        Logs a warning message.

        Args:
        - msg (str): The message to log.
        """
        print(self.YELLOW + "[⚠️WARNING] " + self.WHITE + msg)

    def logSuccess(self, msg):
        """
        Logs a success message.

        Args:
        - msg (str): The message to log.
        """
        print(self.GREEN + "[✅SUCCESS] " + self.WHITE + msg)
        

def getAccessToken(client_id: str, client_secret: str, code: str) -> dict:
    """
    This function gets an access token from the Spotify API using the client_id and client_secret.
    The access token is used to authenticate requests to the Spotify API.
    The access token is returned as a dictionary with the access_token, token_type, and expires_in keys.
    """
    
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic " + base64.b64encode((client_id + ":" + client_secret).encode()).decode()}
    data = {"grant_type": "authorization_code", "code": code, "redirect_uri": "http://127.0.0.1:8731/callback"}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        frameinfo = getframeinfo(currentframe())
        logger.logError("Unable to get access token | " + f"[{response.status_code}]" +str(response.json()))
        logger.logError("Exiting...")
        print(frameinfo.filename, frameinfo.lineno, frameinfo.function)
        exit(-1)
    logger.logSuccess("Access token received successfully.")
    return response.json().get("access_token")
    
def authorizeUser(client_id: str, scopes: str) -> dict:
    """
    This function gets the authorization code from the Spotify API using the client_id and scopes.
    The authorization code is used to authenticate requests to the Spotify API.
    The authorization code is returned as a dictionary with the code key.
    """
    url = "https://accounts.spotify.com/authorize?" 
    url += "client_id=" + client_id
    url += "&response_type=code"
    url += "&redirect_uri=http://127.0.0.1:8731/callback"
    url += "&scope=" + scopes
    webbrowser.open(url)
    logger.logInfo("Please authorize the application to access your Spotify account. You will be redirected to a page with an authorization code.")
    

def getPlaylistsInfo(access_token: str) -> dict:
    """
    This function gets the playlists from the Spotify API using the access_token.
    The playlists are returned as a dictionary with the items key containing a list of playlists.
    returns {
        "playlists": [
            {
                "name": "playlist_name",
                "id": "playlist_id",
                "description": "playlist_description",
                "images": ["image_url"],
                "public": "True/False",
                "tracks": {"href": "tracks_href", "total": "tracks_total"}
            }...
        ]
    }
    """
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        frameinfo = getframeinfo(currentframe())
        logger.logError("Unable to get playlists | " + f"[{response.status_code}]" + str(response.json()))
        logger.logError("Exiting...")
        print(frameinfo.filename, frameinfo.lineno, frameinfo.function)
        exit(-1)
    logger.logSuccess("Playlists received successfully.")
    response = json.loads(response.text)
    items = {"playlists": []}
    for playlist in response["items"]:
        items["playlists"].append(
            {
                "name": playlist["name"],
                "id": playlist["id"],
                "description": playlist["description"],
                "images": [image["url"] for image in playlist["images"]],
                "public": playlist["public"],
                "tracks": {"href": playlist["tracks"]["href"], "total": playlist["tracks"]["total"]}
            }
        )
    logger.logInfo(f"{len(items['playlists'])} playlists received successfully.")
    return items

def getPlaylistTracks(access_token: str, playlist_id: str) -> dict:
    """
    This function gets the tracks from a playlist using the access_token and playlist_id.
    The tracks are returned as a dictionary with the items key containing a list of tracks.
    returns {
        "tracks": [
            {
                "name": "track_name",
                "id": "track_id",
                "uri": "track_uri",
                "artists": ["artist_name"],
                "album": "album_name",
                "duration": "duration_ms",
                "popularity": "popularity",
            }
        ]
    }
    """
    url = "https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks"
    headers = {"Authorization": "Bearer " + access_token}
    # response = requests.get(url, headers=headers)
    # if response.status_code != 200:
    #     # raise Exception("[FAILED] Unable to get playlist tracks\n\t", response.json())
    #     print("[ERROR] Unable to get playlist tracks |", response.json())
    #     print("Exiting...")
    #     exit(-1)
    # response = json.loads(response.text)
    items = {"tracks": []}
    next = url
    while True:
        response = requests.get(next, headers=headers)
        if response.status_code != 200:
            # print("[ERROR] Unable to get playlist tracks |", response.json())
            # print("Exiting...")
            frameinfo = getframeinfo(currentframe())
            logger.logError("Unable to get playlist tracks | " + f"[{response.status_code}]" + str(response.json()))
            logger.logError("Exiting...")
            print(frameinfo.filename, frameinfo.lineno, frameinfo.function)
            exit(-1)
        response = json.loads(response.text)
        for track in response["items"]:
            track = track["track"]
            items["tracks"].append(
                {
                    "name": track["name"],
                    "id": track["id"],
                    "uri": track["uri"],
                    "artists": [artist["name"] for artist in track["artists"]],
                    "album": track["album"]["name"],
                    "duration": track["duration_ms"],
                    "popularity": track["popularity"],
                }
            )
        logger.logInfo("Fetching tracks "+next)
        next = response["next"]
        if next is None:
            break
    logger.logInfo(f"{len(items['tracks'])} tracks received successfully.")
    return items

def createPlaylist(access_token: str, user_id: str, name: str, description: str, public: bool) -> dict:
    """
    This function creates a playlist using the access_token, user_id, name, description, and public.
    The playlist is returned as a dictionary with the id key.
    """
    url = "https://api.spotify.com/v1/users/" + user_id + "/playlists"
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    data = json.dumps({"name": name, "description": description, "public": public})
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 201:
        # raise Exception("[FAILED] Unable to create playlist\n\t", response.json())
        frameinfo = getframeinfo(currentframe())
        logger.logError("Unable to create playlist | " + f"[{response.status_code}]" + str(response.json()))
        logger.logError("Exiting...")
        print(frameinfo.filename, frameinfo.lineno, frameinfo.function)
        exit(-1)
    logger.logSuccess("Playlist created successfully.")
    return response.json()

def addTracksToPlaylist(access_token: str, playlist_id: str, track_ids: list) -> dict:
    """
    This function adds tracks to a playlist using the access_token, playlist_id, and track_ids.
    The response is returned as a dictionary with the snapshot_id key.
    """
    url = "https://api.spotify.com/v1/playlists/" + playlist_id + "/tracks"
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "application/json"}
    response = requests.post(url, headers=headers)
    start = 0
    step = 50
    for i in range(start, len(track_ids), step):
        data = json.dumps({"uris": track_ids[i:i+step]})
        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 201 and response.status_code != 200:
            frameinfo = getframeinfo(currentframe())
            logger.logError("Unable to add tracks to playlist | " + f"[{response.status_code}]" + str(response.json()))
            logger.logError("Exiting...")
            print(frameinfo.filename, frameinfo.lineno, frameinfo.function)
            exit(-1)
        logger.logInfo(f"Adding tracks {i+1} to {i+step}")
    logger.logSuccess("Tracks added to playlist successfully.")
    return response.json()

def changeCoverImage(access_token: str, playlist_id: str, image_url: str) -> dict:
    """
    This function changes the cover image of a playlist using the access_token, playlist_id, and image_url.
    The response is returned as a dictionary with the snapshot_id key.
    """
    url = "https://api.spotify.com/v1/playlists/" + playlist_id + "/images"
    headers = {"Authorization": "Bearer " + access_token, "Content-Type": "image/jpeg"}
    b64_image = base64.b64encode(requests.get(image_url).content).decode()
    
    for attempt in range(3):
        response = requests.put(url, headers=headers, data=b64_image)
        if response.status_code == 202:
            logger.logSuccess("Cover image changed successfully.")
            return response
        else:
            logger.logError(f"Attempt {attempt + 1}: Unable to change cover image | " + f"[{response.status_code}]" + str(response.json()))
            logger.logInfo("Retrying in 3 seconds...")
            time.sleep(3)
    
    logger.logError("Failed to change cover image after 3 attempts. Moving on...")
    return response

def getUserInfo(access_token: str) -> dict:
    """
    This function gets the user information from the Spotify API using the access_token.
    The user information is returned as a dictionary with the id, display_name, email, and images keys.
    """
    url = "https://api.spotify.com/v1/me"
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        frameinfo = getframeinfo(currentframe())
        logger.logError("Unable to get user info | " + f"[{response.status_code}]" + str(response.json()))
        logger.logError("Exiting...")
        print(frameinfo.filename, frameinfo.lineno, frameinfo.function)
        exit(-1)
    logger.logSuccess("User info received successfully.")
    response = json.loads(response.text)
    if response["email"] is None:
        logger.logWarning("Email not provided by user.")
        response["email"] = "Not Provided"
    return {
        "id": response["id"],
        "display_name": response["display_name"],
        "email": response["email"],
        "images": [image["url"] for image in response["images"]]
    }

if __name__ == "__main__":
    # Testing Phase ======================================================
    logger = Logger()
    # logger.logInfo("This is an informational message.")
    # logger.logError("This is an error message.")
    # logger.logWarning("This is a warning message.")
    # logger.logSuccess("This is a success message.")

    # primary account
    primary_client_id = "YOUR_CLIENT_ID"
    primary_client_secret = "YOUR_CLIENT_SECRET"

    # secondary account
    secondary_client_id = "YOUR_CLIENT_ID"
    secondary_client_secret = "YOUR_CLIENT_SECRET"

    # Authorization Scopes
    primary_client_scopes = "playlist-read-private user-read-email"
    secondary_client_scopes = "ugc-image-upload playlist-modify-public playlist-modify-private user-read-email"

    authorizeUser(primary_client_id, primary_client_scopes)
    primary_authorization_code = input("Enter the authorization code: ")
    primary_access_token = getAccessToken(primary_client_id, primary_client_secret, primary_authorization_code)
    
    logger.logInfo("Primary Account Access Token: " + primary_access_token)

    authorizeUser(secondary_client_id, secondary_client_scopes)
    secondary_authorization_code = input("Enter the authorization code: ")
    secondary_access_token = getAccessToken(secondary_client_id, secondary_client_secret, secondary_authorization_code)

    logger.logInfo("Secondary Account Access Token: " + secondary_access_token)

    primary_playlists = getPlaylistsInfo(primary_access_token)

    for primary_playlist in primary_playlists["playlists"]:
        print("\n==============================================================================")
        primary_playlist["description"] = html.unescape(primary_playlist["description"])
        logger.logInfo("Playlist ID: " + str(primary_playlist["id"]))
        logger.logInfo("Playlist Name: " + str(primary_playlist["name"]))
        logger.logInfo("Playlist Description: " + str(primary_playlist["description"]))
        logger.logInfo("Playlist Images: " + str(primary_playlist["images"]))
        logger.logInfo("Playlist Public: " + str(primary_playlist["public"]))
        logger.logInfo("Playlist Tracks: " + str(primary_playlist["tracks"]))

        
        primary_playlist_tracks = getPlaylistTracks(primary_access_token, primary_playlist["id"])

        track_uris = [track["uri"] for track in primary_playlist_tracks["tracks"]]

        user_info = getUserInfo(secondary_access_token)

        secondary_playlist = createPlaylist(access_token=secondary_access_token, user_id=user_info["id"], name=primary_playlist["name"], description=primary_playlist["description"], public=primary_playlist["public"])

        addTracksToPlaylist(secondary_access_token, secondary_playlist["id"], track_uris)

        changeCoverImage(secondary_access_token, secondary_playlist["id"], primary_playlist["images"][0])
        print("==============================================================================\n")