# Install
## Python Audio and Video Backend
### Virtual Environment

In the command line, move into ```/pybackend``` and create a virtual environment for the project:

```
virtualenv env
```

From ```/pybackend```, move into the env folder and call the activate script to activate  the virtual environment:

```
cd env/Scripts/
activate
```

The command line should now indicate that the environment is activated:

```
(env) c:/ ... / Scripts
```

Move up to the ```/pybackend``` directory and install the dependencies defined in ```requirements.txt```:

```
cd ../../
pip install -r requirements.txt
```

This should install all of the python modules required.

## FFmpeg
Although video editing features are primarily done with ```moviepy```, ```ffmpeg``` is used to scale and re-encode the videos to a single format before concatenation. 

https://www.ffmpeg.org/download.htmlhttps://www.ffmpeg.org/download.html

## Run

First, make sure the following directory structure is present:

```
/pybackend
    /audio
    /video
    orchestrated_video.py
    ... other src files
```

The ```/audio``` directory should contain audio files that you would like to use to make the final edit. These should be .wav files.

The ```/video``` directory should contain the video files that will be edited. I have only tested this with .mp4 files.

At the moment, running this for the first time requires a bit of set up.

1. Place the audio file in the ```audio``` directory
2. Place the videos in the ```video``` directory
2. Open ```orchestrated_video.py```, 
3. Uncomment the line in ```'__main__'``` :

    ``` py 
    # Creates a session directory in /video to store re-encoded videos
    prepare_session(video_dir, session_dir) 
    ```
5. In the command line, make the sure virtual environment is activated an run:
    ```
    python orchestrated_video.py filename.wav
    ```
    Where ```filename.wav``` is the filename and extension of the audio file in ```/audio``` that you want to use to edit the video.

    You will see ffmpeg logs while it re-encodes the videos and then logs from this project when it makes the final edits.

6. The result file is ```output.mp4```.
    
6. If you don't plan on changing the videos in ```/video```, you can now re-comment the line so that re-encoding does not occur again. Sorry, long winded for now! Re-encoding the videos is not required if you want to change the audio file.

## Contributions
Contributions are most welcome!

If ever you want to add a module to the project:
1. Make sure the venv is activated.
2. use pip to install the module as you would normally.
3. use  ```pip freeze > requirements.txt``` to save the dependency in ```requirements.txt```.



