from flask import Flask, request
from wordytaire import Wordytaire

app = Flask(__name__)
wt = Wordytaire()


@app.route('/', methods=['POST'])
def handle_submission():
    score = 0
    
    if 'file' not in request.files:
        return ('No payload', 400)

    file = request.files['file']

    if not file.filename:
        return ('No filename', 400)
        
    submission = [line.decode('utf-8') for line in file.readlines()]
    
    score = wt.score_submission(submission)

    return score   


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)