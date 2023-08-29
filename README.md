'''

Install your driver
python -m pip install pymongo

'''

'''
Connection url
"mongodb+srv://<username>:<password>@cluster0.busb95b.mongodb.net/?retryWrites=true&w=majority"

'''

'''
pip install --upgrade google-api-python-client

from googleapiclient.discovery import build
youtube_service = build('youtube','v3',developerKey=KEY)         ==> created a youtube service 


Documentation :
"https://developers.google.com/youtube/v3/getting-started"

curl \
  'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=UC_x5XG1OV2P6uZZ5FSM9Ttw&key=[YOUR_API_KEY]' \
  --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
  --header 'Accept: application/json' \
  --compressed



'''