def get_channel_url(video_id, key):
    return f'https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id={video_id}&key={key}'

