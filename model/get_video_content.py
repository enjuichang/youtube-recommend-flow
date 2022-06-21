# Get YouTube Data API creds
import os
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import googleapiclient.discovery
import googleapiclient.errors

def getVideoContent(video_id, youtube):

    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
  
    response = request.execute()

    title = response["items"][0]["snippet"]["title"]
    description = response["items"][0]["snippet"]["description"]
    return title, description

if __name__ == "__main__":

    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
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
    if os.path.exists('token.json'):
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
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build service
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

    video_id = input("Input id: ")
    title, description = getVideoContent(video_id, youtube)
    print(title, description)