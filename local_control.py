import subprocess
from flask import Flask, request, jsonify, requests
import psutil

app = Flask(__name__)

# 计算机的VLC路径和视频路径
VLC_PATH = "C:\\Path\\To\\VLC\\vlc.exe"  # 替换为实际的VLC路径
VIDEO_PATH = "C:\\Path\\To\\Video\\video.mp4"  # 替换为实际的视频路径

def is_vlc_running():
    """检查是否有 VLC 进程正在运行"""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'vlc.exe':
            return True
    return False

@app.route('/control', methods=['POST'])
def control():
    action = request.json.get('action')
    print(f"Received action: {action}")

    if action == 'play':
        if not is_vlc_running():
            subprocess.Popen([
                VLC_PATH, VIDEO_PATH, '--fullscreen', '--loop', '--no-video-title-show'
            ])
    elif action == 'pause':
        # 暂停逻辑
        requests.get('http://localhost:8080/requests/status.xml?command=pl_pause', auth=('', '123'))
    elif action == 'forward':
        # 快进逻辑
        requests.get('http://localhost:8080/requests/status.xml?command=seek&val=+10', auth=('', '123'))
    elif action == 'backward':
        # 后退逻辑
        requests.get('http://localhost:8080/requests/status.xml?command=seek&val=-10', auth=('', '123'))
    elif action == 'close':
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'vlc.exe':
                proc.terminate()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
