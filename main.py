import datetime
from re import sub

from flask import Flask, flash, redirect, render_template, request
from google.auth.transport import requests
from google.cloud import datastore
from hashlib import sha256
from wordytaire import Wordytaire

import google.oauth2.id_token

app = Flask(__name__)
firebase_request_adapter = requests.Request()
wt = Wordytaire()


def hash_submission(submission):
    return sha256('\n'.join(submission).encode('utf-8')).hexdigest()


@app.route('/upload_submission', methods=['POST'])
def upload_submission():
    score = 0
    
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if not file.filename:
        flash('No selected file')
        return redirect(request.url)

    submission = [line.decode('utf-8') for line in file.readlines()]
    hash = hash_submission(submission)
    
    existing_score = fetch_score(hash)

    if existing_score:
        print('Known submission')
        score = existing_score
    else:
        print('New submission')
        score = wt.score_submission(submission)[1]
        store_score(hash, score)


@app.route('/', methods=['GET', 'POST'])
def root():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    score = 0

    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)
    
    return render_template(
        'index.html',
        user_data=claims, error_message=error_message, score=score)

datastore_client = datastore.Client()


def fetch_score(hash):
    key = datastore_client.key("Score", hash)
    
    score = datastore_client.get(key)

    return score


def store_score(hash, score):
    key = datastore_client.key("Score", hash)

    score = datastore.Entity(key=key)

    score.update(
        {
            "score": score
        }
    )

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)