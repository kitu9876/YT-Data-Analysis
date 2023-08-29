import requests
import logging
from vars import KEY
from yturls import get_channel_url, get_video_url, get_comment_url
from googleapiclient.discovery import build

logging.basicConfig(filename="scrape.log",level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

class YT: 

    def get_channel_details(self, channel_id):
        try:
            ch_url = get_channel_url(channel_id, KEY)
            ch_response = requests.get(ch_url)
            channel_data = ch_response.json()
            channel_info = {
                '_id':channel_id,
                'channelName': channel_data['items'][0]['snippet']['title']
            }
            channel_info.update(channel_data['items'][0]['statistics'])
            return channel_info
        except Exception as e:
            logging.error(str(e))
            return None

    def get_video_details(self, video_id):
        try:
            video_url = get_video_url(video_id, KEY)
            comment_url = get_comment_url(video_id, KEY)
            video_details = {
                '_id': video_id
            }
            video_stat = requests.get(video_url).json()
            if video_stat['pageInfo']['totalResults'] == 0:
                return None
            try:
                video_details['channelName']=video_stat['items'][0]['snippet']['channelTitle']
            except Exception:
                video_details['channelName'] = ''
            try:
                video_details['title'] = video_stat['items'][0]['snippet']['title']
            except Exception:
                video_details['title'] = ''

            try:
                video_details['description'] = video_stat['items'][0]['snippet']['description']
            except Exception:
                video_details['description'] = ''

            try:
                video_details['postedOn'] = video_stat['items'][0]['snippet']['publishedAt']
            except Exception:
                video_details['postedOn'] = ''
            
            try:
                video_details.update(video_stat['items'][0]['statistics'])
            except Exception as e:
                logging(str(e))
                
            try:
                video_details['duration'] = video_stat['items'][0]['contentDetails']['duration']
            except Exception:
                video_details['duration'] = ''

            try:
                video_details['thumbnail'] = video_stat['items'][0]['snippet']['thumbnails']['standard']['url']
            except Exception:
                video_details['thumbnail'] = ''

            try:
                video_details['tags'] = video_stat['items'][0]['snippet']['tags'][1:]
            except Exception:
                video_details['tags'] = []
            
            try:
                video_details['language'] = video_stat['items'][0]['snippet']['defaultAudioLanguage']
            except Exception:
                video_details['language'] = ''

            try:
                comment_data = requests.get(comment_url).json()
                comments = []
                for comment in comment_data["items"]:
                    temp = {
                        'author': comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        'comment': comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                        'time': comment['snippet']['topLevelComment']['snippet']['publishedAt'],
                    }
                    reply =[]
                    if comment.get('replies'):
                        com = comment.get('replies').get('comments')
                        for c in com:
                            reply_temp = {
                                'author': c['snippet']['authorDisplayName'],
                                'comment': c['snippet']['textDisplay'],
                                'time': c['snippet']['publishedAt']
                            }
                            reply.append(reply_temp)
                    temp['reply'] = reply
                    comments.append(temp)
                video_details['comments'] = comments
            except Exception as e:
                logging(str(e))
                video_details['comments'] = []
            return video_details
        except Exception as e:
            logging.error(str(e))
            return None

    # as above functions are based on curl provided
    #All below functions will need a youtube service ,as they are based on python code provided by youtube data api documentation.
    # youtube= build('youtube','v3',developerKey=KEY)         ==> created a youtube service 


    
# Construct the channel URL based on the video ID, using c_url provided by youtube data api
#channel_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet"
    
    def get_channel_id(self,video_id,api_key):     
        channel_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet"
        # Constructing the channel URL based on the video ID
        response = requests.get(channel_url)
        data = response.json()
        try:
            if "items" in data and len(data["items"]) > 0:
                    channel_id = data["items"][0]["snippet"]["channelId"]
                    return channel_id
        except :
            "Channel Id not found"
        
            
    def get_channel_stats(self,_yt_service,_channel_ids):
        all_data=[]
        request = _yt_service.channels().list(
            part="snippet,contentDetails,statistics",
            id=",".join(_channel_ids)
        )
        response= request.execute()
        for i in range(len(response['items'])):
            data = dict(ChannelName= response['items'][i]['snippet']['title'],
                        PlaylistId= response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                        Subscribers=response['items'][i]['statistics']['subscriberCount'],
                        Views=response['items'][i]['statistics']['viewCount'],
                        TotalVideos=response['items'][i]['statistics']['videoCount'])
            all_data.append(data)
        return all_data
    
    def get_video_ids(_yt_service,_playlist_id):
        request = _yt_service.playlistItems().list(
        part='contentDetails',
        playlistId=_playlist_id,
        maxResults=50
        )
        response= request.execute()

        video_ids=[]
        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['contentDetails']['videoId'])

        _nextPageToken= response.get('nextPageToken')
        morePages=True
        while morePages:
            if _nextPageToken is None:
                morePages= False
            else:
                request = _yt_service.playlistItems().list(
                    part='contentDetails',
                    playlistId=_playlist_id,
                    maxResults=50,
                    pageToken=_nextPageToken)
                response= request.execute()

                for i in range(len(response['items'])):
                    video_ids.append(response['items'][i]['contentDetails']['videoId'])
                    
                _nextPageToken= response.get('nextPageToken')

        return video_ids
    
    def get_video_details_for_one(youtube,video_id):
        request= youtube.videos().list(
                part='snippet,statistics',
                id=video_id)
        response = request.execute()
        video_stats=dict(Title=response['items']['snippet']['title'],
                                Published_date= response['items']['snippet']['publishedAt'],
                                Views= response['items']['statistics']['viewCount'],
                                Likes= response['items']['statistics']['likeCount'],
                                Favourites= response['items']['statistics']['favoriteCount'],
                                Comments= response['items']['statistics']['commentCount'])



    def get_video_details_for_multiple(youtube,video_ids):
        all_video_stats=[]
        for i in range(0,len(video_ids),50):
            request= youtube.videos().list(
                part='snippet,statistics',
                id=','.join(video_ids[i:i+50]))
            response = request.execute()

            for video in response['items']:
                video_stats=dict(Title=video['snippet']['title'],
                                Published_date= video['snippet']['publishedAt'],
                                Views= video['statistics']['viewCount'],
                                Likes= video['statistics']['likeCount'],
                                Favourites= video['statistics']['favoriteCount'],
                                Comments= video['statistics']['commentCount'])

                all_video_stats.append(video_stats)
        return all_video_stats
