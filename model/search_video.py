# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import googleapiclient.errors

def searchVideo(query, youtube, max_result=5):

    request = youtube.search().list(
        part="snippet",
        maxResults=max_result,
        q=query
    )
    response = request.execute()

    titles = []
    urls = []

    for item in response["items"]:
        titles.append(item["snippet"]["title"])
        urls.append(f"https://www.youtube.com/watch?v={item['id']['videoId']}")

    return titles, urls

if __name__ == "__main__":
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

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

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

    query = "Europa Universalis 4"
    titles, urls = searchVideo(query, youtube)
    print(titles, urls)