from flask import Flask, render_template, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json
from dotenv import load_dotenv
import io
from googleapiclient.http import MediaIoBaseDownload


load_dotenv()

info = json.loads(os.environ['GOOGLE_CREDENTIALS'])

creds = service_account.Credentials.from_service_account_info(
    info,
    scopes=["https://www.googleapis.com/auth/drive.readonly"]
)

drive_service = build('drive', 'v3', credentials=creds)
FOLDER_ID = '190UY56-VYS5Tzmd_u8GAO5XRQk6upp54'

query = f"'{FOLDER_ID}' in parents and trashed = false"




app = Flask(__name__)
app.static_folder = 'static'


@app.route('/files')
def list_files():
    folder_id = FOLDER_ID
    results = drive_service.files().list(
        q=query,
        fields="files(id, name)"
    ).execute()
    files = results.get('files', [])
    
    file_contents = []
    for file in files:
        file_id = file['id']
        file_name = file['name']
        # Download file content
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        content = fh.getvalue().decode('utf-8')
        file_contents.append({
            'name': file_name,
            'content': content
        })
    
    return jsonify(file_contents)




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/docs/core")
def docs1():
    return render_template("docs-functionality.html")
@app.route("/docs/guide")
def docs2():
    return render_template("docs-qsg.html")
@app.route("/docs/")
def docs3():
    return render_template("docs-main.html")
@app.route("/gmodedit")
def gmewin():
    return render_template("gmodwin/modulator-editor.html")
if __name__ == "__main__":
    app.run(debug=True)
