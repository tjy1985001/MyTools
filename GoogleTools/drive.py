#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import httplib2

from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    FLAGS = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    FLAGS = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-tools.json
SCOPES = 'https://www.googleapis.com/auth/drive.file'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'MyTools'


class GoogleDrive(object):
    def __init__(self):
        credentials = self.__get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.__google_service = discovery.build('drive', 'v3', http=http)

    def __get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'drive-tools.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if FLAGS:
                credentials = tools.run_flow(flow, store, FLAGS)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print 'Storing credentials to ' + credential_path
        return credentials

    def upload(self, folder_id, file_path, mime_type):
        'upload file'
        file_metadata = {
            'name': os.path.basename(file_path),
            'mimeType': mime_type,
            'parents': [folder_id] if folder_id else None
        }
        # print file_metadata
        media = MediaFileUpload(file_path, resumable=True)
        uploaded_file = self.__google_service.files().create(
            body=file_metadata, media_body=media, fields='id').execute()
        print 'File ID: %s' % uploaded_file.get('id')


def main():
    google_drive = GoogleDrive()
    folder_id = None
    file_path = './test.csv'
    mime_type = 'application/vnd.google-apps.spreadsheet'
    google_drive.upload(folder_id, file_path, mime_type)


if __name__ == '__main__':
    main()
