#from main import 
import os
from flask import Flask, render_template, json, url_for, request
import main

app = Flask(__name__)
@app.route('/song')
def song():

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static", "static/mySongs.json")
    currentSong = main.getCurrentTrack()
    print(currentSong)
    dataMine = json.load(open(json_url))
    return render_template('song.html', dataMine = dataMine )

if __name__ == "__main__":
    app.run()
