import os

audio_dir = "audio"
video_dir = "video"                 # user input videos
session_dir = "video/session"       # videos used to make the final edit
output_dir = "video/session/output" # dir for final video edits


INPUT_EXT = ".mp4" # user input format
INTER_EXT = ".mp4" # intermediate format (resizing)
OUTPUT_EXT = ".mp4" # output format (transcode)

ffmpeg_loglevel = 'panic'

_output_path = os.path.join(output_dir, f"output{OUTPUT_EXT}")
last_output_path = _output_path

def is_video_file(path):
    return os.path.isfile(path) and path.endswith((INPUT_EXT, INTER_EXT, OUTPUT_EXT))

def clear_videos_from_dir(directory):
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if is_video_file(path): os.remove(path)

def prepare_dir(directory):
    if  os.path.isdir(directory) is False:
        os.mkdir(directory)
    else: clear_videos_from_dir(directory)

def path_in_same_dir(file_path, new_file_name):
    file_dir = os.path.dirname(file_path)
    return os.path.join(file_dir, new_file_name)

def resize_video(video_path, scale= '720:480'):
    name = os.path.basename(video_path)
    target_path = path_in_same_dir(video_path, f"r_{name}{INTER_EXT}") 
    
    os.system(f"ffmpeg -loglevel {ffmpeg_loglevel} -i {video_path} -vf scale={scale} {target_path}")        

    return target_path

def transcode(video_path, target_name = None, target_dir = session_dir, codec = 'libx264', preset = 'ultrafast',
              crf = 22, ext = OUTPUT_EXT):
    if target_name == None:
        video_name = os.path.basename(video_path)
        target_name = f"{video_name}_{codec}_{crf}"
    
    target_path = os.path.join(target_dir, f"{target_name}{ext}")

    os.system(f"ffmpeg -loglevel {ffmpeg_loglevel} -i {video_path} -c:v {codec} -preset {preset} -crf {crf} -c:a copy {target_path}")
    
def list_videos_in(directory):
    videos = []
    print(os.listdir(directory))
    for f in os.listdir(directory):
        path = os.path.join(directory, f)
        if is_video_file(path):
            videos.append(path)
    print("Found videos: ", videos)
    return videos


def prepare_session():
    prepare_dir(session_dir)
    prepare_dir(output_dir)

    for i, video in enumerate(list_videos_in(video_dir)):
        path = os.path.join(video_dir, video)
        print("Resize ", path)
        resized_path = resize_video(path)
        print("Transcode", resized_path, " into ", "session_dir")
        transcode(resized_path, i, session_dir)
        os.remove(resized_path)

def write_moviepy_video(moviepy_video, audio_path, output_path = _output_path):
    without_audio_path = os.path.join(output_dir, f"temp{OUTPUT_EXT}")
    moviepy_video.write_videofile( f'{without_audio_path}',
                                audio=False, # TODO Fix moviepy bug
                                preset='ultrafast', 
                                threads=4)

    # moviepy bug : resort to ffmpeg 
    if os.path.isfile(output_path): os.remove(output_path)
    print(f"Writing moviepy video to disk at {output_path}")
    os.system(f"ffmpeg -i {without_audio_path} -i {audio_path} -c:v copy -map 0:v:0 -map 1:a:0 -c:a aac -b:a 192k {output_path}")

    os.remove(without_audio_path)


    return output_path











