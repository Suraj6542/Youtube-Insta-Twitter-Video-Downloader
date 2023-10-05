from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

def download_progress_hook(d):
    #print(d)
    if d['status'] == 'downloading':
        progress = {
            'status': 'downloading',
            'percent': d['_percent_str'],
            'eta': d['_eta_str']
        }
        # Send progress to the client using Flask-SSE or WebSocket
        # For simplicity, let's use a global variable as an example
        global last_progress
        last_progress = progress

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    try:
        info_dict = yt_dlp.YoutubeDL().extract_info(video_url, download=False)
        video_title = info_dict.get('title', 'video')
        video_ext = info_dict.get('ext', 'mp4')
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'C:\\Users\\hp\\Downloads\\{video_title}.{video_ext}',
            'progress_hooks': [download_progress_hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return jsonify({'status': 'completed'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
