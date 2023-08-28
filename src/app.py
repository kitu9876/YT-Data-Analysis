from flask import Flask , render_template , request , jsonify
from flask_cors import CORS , cross_origin
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bs
import requests
import os
import logging

from scrapper import get_channel_stats,get_video_ids,get_video_details

logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app= Flask(__name__)
@app.route("/", methods =['GET'])
def homepage(self,_video_url):

    return render_template("index.html")

@app.route("/scrap",methods=['POST'])
def scrap():
  if request.method=='POST':
    searchUrl= request.form['url']
    video_id = searchUrl.split("=")[-1]

    






      

      