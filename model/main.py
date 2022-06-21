from get_video_content import getVideoContent
from nlp_parsing import getGameTitle
from search_video import searchVideo
from get_game_type import getSteamGenre
import re

# Get YouTube Data API creds
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def processUrl(video_url):
    # Regex for YouTube url2id
    # Source: https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
    video_id = re.findall(r"^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*",video_url)
    return video_id[0][1]

def main(video_url):
    scopes = ["https://www.googleapis.com/auth/youtube.readonly","https://www.googleapis.com/auth/youtube.force-ssl"]
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "model/client_secret.json"

    # Get credentials and create an API client
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('model/token.json'):
        creds = Credentials.from_authorized_user_file('model/token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('model/token.json', 'w') as token:
            token.write(creds.to_json())

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

    video_id = processUrl(video_url)
    title, description = getVideoContent(video_id, youtube)
    game_title = getGameTitle(title)
    print(game_title)
    game_cats = getSteamGenre(game_title)
    titles, urls = searchVideo(game_title, youtube)

    return titles[0], game_cats, urls[0]

if __name__ == "__main__":
    video_url = input("Video URL: ")
    result = main(video_url)
    print(result)