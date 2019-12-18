# Install
## Python Audio and Video Backend
### Virtual Environment

In the command line, move into ```/py``` and create a virtual environment for the project:

```
virtualenv env
```

From ```/py```, move into the env folder and call the activate script to activate  the virtual environment:

```
cd env/Scripts/
activate
```

The command line should now indicate that the environment is activated:

```
(env) c:/ ... / Scripts
```

Move up to the ```/py``` directory and install the dependencies defined in ```requirements.txt```:

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
/py
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

5. In the command line, make the sure virtual environment is activated an run:
    ```
    python file_structure.py
    ```
    This will transcode all of the videos in the ```video``` directory to the same format, and place them in a newly created ```video/session``` folder.
    
6. Now run:
```
orchestrated_video.py
```
The final output is stored in ```video/session/output/```

Steps 1-3 are now only necessary if you want to change the input videos in the ```video``` directory.

## Contributions
Contributions are most welcome!

If ever you want to add a module to the project:
1. Make sure the venv is activated.
2. use pip to install the module as you would normally.
3. use  ```pip freeze > requirements.txt``` to save the dependency in ```requirements.txt```.



