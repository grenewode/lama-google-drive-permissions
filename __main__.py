from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import argparse
from appdirs import AppDirs
import os

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

DIRS = AppDirs('lama-gdrive-get-owners', 'Lama')

def main():
    parser = argparse.ArgumentParser(description='list files owned by a user in a google drive')
    parser.add_argument('user', type=str, help='the user email you want to search for')
    parser.add_argument('-C', '--credentials', default=os.path.join(os.getcwd(), 'credentials.json'), help='the credentials file the application should use to authenticate with github') 

    args = parser.parse_args()

    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    token_file = os.path.join(DIRS.user_cache_dir, 'token.pickle')
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                args.credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        os.makedirs(os.path.dirname(token_file), exist_ok=True)
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    page_token = None

    while True:
        response = service.files().list(q=f"'{args.user}' in readers",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name, webViewLink, owners)',
                                            pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            id, name, webViewLink, owners = file.get('id'), file.get('name'), file.get('webViewLink'), file.get('owners')

            print(f"> {name}")
            print(f"\t url:\t{webViewLink}")
            for owner in owners:
                print(f"\t owner:\t{owner.get('displayName')}")
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

if __name__ == '__main__':
    main()
