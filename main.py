from flask import Flask, render_template, request, redirect, send_file
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        stream.download()
        filename = yt.title + ".mp4"
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
