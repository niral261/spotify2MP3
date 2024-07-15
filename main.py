import subprocess
from waitress import serve
from app import app

def main():
    # Step 1: Run app.py with Waitress
    print("Running app.py with Waitress...")
    serve(app, host='0.0.0.0', port=5000)

    # Step 2: Run youtubeMP3.py
    print("Running youtubeMP3.py...")
    subprocess.run(["python", "youtubeMP3.py"], check=True)

if __name__ == '__main__':
    main()
