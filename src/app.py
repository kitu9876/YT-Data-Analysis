from flask import Flask , render_template , request , send_file
import requests
from ytutils import YT
from vars import KEY
from mongo_operation import MongoOperation


app= Flask(__name__)
channel_ids = ['UCNU_lfiiWBdtULKOw6X0Dig', 'UCb1GdqUqArXMQ3RS86lqqOw', 'UCDrf0V4fcBr5FlCtKwvpfwA']
mo = MongoOperation()
ytu = YT()

@app.route("/")
def home():
    channels = []
   
    for id in channel_ids:
        channel = ytu.get_channel_details(id)
        channels.append(channel)
    mo.save_channels(channels)
    return render_template("index.html", channels=channels)

@app.route("/find", methods=('POST',))
def find():
    if request.method == "POST":
       url = request.form.get("url")
       video_id = url.split("=")[-1]
       video_details = mo.get_video_details(video_id)
       if video_details is None:
        video_details = ytu.get_video_details(video_id)
        if video_details is not None:
            mo.save_video(video_details)
        else:
            video_details = False
       
    return render_template("video_details.html", video=video_details)



#@app.route("/", methods =['GET'])
#def homepage():
 # channel_details = ytu.get_channel_stats(youtube,channel_ids)
  #return render_template("index.html", channel_details)


if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
'''
if __name__ == '__main__':
    app.debug = True
    app.run()
'''










      

      