import requests
from yturls import get_channel_url


class YT: 

    
    def get_channel_id(self,video_id,key):     
        channel_url = get_channel_url(video_id,key)         # Construct the channel URL based on the video ID

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
            data = dict(ChannelNname= response['items'][i]['snippet']['title'],
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

    def get_video_details(youtube,video_ids):
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
