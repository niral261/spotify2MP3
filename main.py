import subprocess

def main():
    # Step 1: Run app.py with Waitress
    print("Running app.py with Waitress...")
    subprocess.run(["waitress-serve", "--call", "app:app"])

    # Step 2: Run youtubeMP3.py
    print("Running youtubeMP3.py...")
    subprocess.run(["python", "youtubeMP3.py"], check=True)

if __name__ == '__main__':
    main()
