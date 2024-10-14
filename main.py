#我需要一个网页控制端 
# 功能是用网页控制设备 播放视频 要有快进和后退的功能， 
# 设备视频要求全屏播放 并且一直 循环，最好是能用python来写
#是网页控制设备播放视频不是用网页播放视频
#视频播放器位置"C:\Program Files\VideoLAN\VLC\vlc.exe"
#视频位置"C:\Users\qamar\Downloads\148597-794221559_small.mp4"
import subprocess
import requests
from flask import Flask, render_template, request, jsonify
import psutil  # 用于检查进程

app = Flask(__name__)

# VLC 播放器路径
VLC_PATH = "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
VIDEO_PATH = "C:\\Users\\qamar\\Downloads\\148597-794221559_small.mp4"

# 启动 VLC 播放器
vlc_process = None

def is_vlc_running():
    """检查是否有 VLC 进程正在运行"""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'vlc.exe':
            return True
    return False

@app.route('/')
def index():
    return render_template('1.html')

@app.route('/control', methods=['POST'])
def control():
    global vlc_process
    action = request.json.get('action')
    print(f"Received action: {action}")  # 添加调试信息
    
    if action == 'play':
        if not is_vlc_running():
            print("Starting VLC...")
            vlc_process = subprocess.Popen([
                VLC_PATH, VIDEO_PATH, '--fullscreen', '--loop', '--no-video-title-show',
                '--qt-fullscreen-screennumber=0', '--no-qt-privacy-ask', '--no-qt-error-dialogs',
                '--qt-minimal-view', '--no-qt-fs-controller'
            ])
        else:
            print("VLC is already running.")
    elif action == 'pause':
        print("Sending pause command...")
        requests.get('http://localhost:8080/requests/status.xml?command=pl_pause', auth=('', '123'))
    elif action == 'forward':
        print("Sending forward command...")
        requests.get('http://localhost:8080/requests/status.xml?command=seek&val=+10', auth=('', '123'))
    elif action == 'backward':
        print("Sending backward command...")
        requests.get('http://localhost:8080/requests/status.xml?command=seek&val=-10', auth=('', '123'))
    elif action == 'close':
        print("Closing all VLC processes...")
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'vlc.exe':
                proc.terminate()
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
