# app.py
from flask import Flask, render_template, request
from translator import analyze_mood_from_text, get_song_from_spotify

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    song = None
    detected_mood = None

    if request.method == "POST":
        user_text = request.form["mood"]
        detected_mood = analyze_mood_from_text(user_text)
        song = get_song_from_spotify(detected_mood)

    return render_template("index.html", song=song, mood=detected_mood)

if __name__ == "__main__":
    app.run(debug=True)
