import sys
import os
from os import listdir, remove
from os.path import isfile, join
from audio_analysis import AudioFile, OnsetExtractor
from video_edit import MoviePyEditor

def re_encode(video_path, target_dir, target_name):
    # Resize and rencode the video and store result in the target_dir

    # resize the video
    os.system(f"ffmpeg -i {video_path} -vf scale=720:480 resized.mp4")

    target_path = os.path.join(target_dir, target_name)
    # re-encode
    os.system(f"ffmpeg  -i resized.mp4 -c:v libx264 -preset ultrafast -crf 22 -c:a copy {target_path}")

    os.remove("resized.mp4")

def prepare_session(video_dir, session_dir):
    # if session directory does not exist, make it
    if  os.path.isdir(session_dir) is False:
        os.mkdir(session_dir)
    
    # if final_edit directory does not exist, make it
    final_dir = os.path.join(session_dir, "final_edit")
    if os.path.isdir(final_dir) is False:
        os.mkdir(final_dir)

    # Resize and re-encode all videos in the video_dir, place the standardized videos in session_dir 
    # remove videos from the previous session
    for f in listdir(session_dir) :  
        if isfile(join(session_dir, f)) : os.remove(os.path.join(session_dir, f))
    # Re-encode all videos from video_dir to the same encoding and place them in the session folder
    for i, video in enumerate(video_paths): re_encode(video, session_dir, f"{i}.mp4")

if __name__ == '__main__':
    audio_filename = sys.argv[1]

    audio_path = f"./audio/{audio_filename}"
    print("Loading audio: ", audio_path)
    audio_file = AudioFile(audio_path)

    oe = OnsetExtractor()
    
    print("Using onset extractor to create an edit list")
    edit_list = oe.extract_onsets(audio_file)
    print("The onset extractor found musical onsets at seconds:\n " , edit_list)

    # Get the list of videos in the video folder
    video_dir = "./video"
    video_paths = [join(video_dir, f) for f in listdir(video_dir) if isfile(join(video_dir, f))]

    # Directory of re-encoded videos used to create the final edit
    session_dir = "./video/session"
    # For debugging, prepare_session not needed if videos in video_dir have not changed...
    # prepare_session(video_dir, session_dir)

    # list of re-encoded video paths
    session_video_paths = [join(session_dir, f) for f in listdir(session_dir) if isfile(join(session_dir, f))]

    # create the final edit
    # list of ffmpeg input videos

    moviepy_editor = MoviePyEditor(session_video_paths)
    moviepy_editor.create_edit(session_video_paths, edit_list, audio_path)
    


    

    
