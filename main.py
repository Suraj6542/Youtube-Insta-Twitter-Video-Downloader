from flask import Flask, render_template, request, redirect, send_file
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST','GET'])
def download():
    video_url = request.form['video_url']
    try:
        info_dict = yt_dlp.YoutubeDL().extract_info(video_url, download=False)
        video_title = info_dict.get('title', 'video')
        video_ext = info_dict.get('ext', 'mp4')
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'C:\\Users\\hp\\Downloads\\{video_title}.{video_ext}',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            return render_template('index.html')

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
