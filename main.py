from wordytaire import Wordytaire

wt = Wordytaire()

def score(request):
    request_json = request.get_json(silent=True)

    if request_json and 'submission' in request_json:
        message, score = wt.score_submission(request_json['submission'])

        return f'Score: {score}. Message: {message}'
    else:
        return 'Invalid submission format!'