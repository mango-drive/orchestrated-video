import os
from os import listdir, remove
from os.path import isfile, join
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import ffmpeg

def clear_output_file():
    if isfile('out.mp4'): remove('out.mp4')

class MoviePyEditor:
    def __init__(self, video_paths):
        self.video_clips = [VideoFileClip(path) for path in video_paths]

    def create_edit(self, video_paths, edit_list, audio_path):
        clear_output_file()

        subclips = self.extract_subclips(self.video_clips, edit_list)

        self.write_final_edit(subclips, audio_path)

    def extract_subclips(self, clips, edit_list):
        video_i = 0
        prev_loc = 0
        subclips = []

        for i, loc in enumerate(edit_list):
            # Cycle through the video list with integer that wraps around
            # the list's length
            video_i =  i % (len(clips))

            # Create a subclip of the video, between the previous and current edit
            # locations
            print("Making edit: {} {}".format(prev_loc, loc))
            subclips.append(self.video_clips[video_i].subclip(prev_loc, loc))

            prev_loc = loc
        
        return subclips
    
    def write_final_edit(self, subclips, audio_path):
        final_edit = concatenate_videoclips(subclips, 
                                            method='compose')
        audio = AudioFileClip(audio_path)
        final_edit.set_audio(audio)

        out_file = 'out_movie_py.mp4'
        final_edit.write_videofile( out_file,
                                    audio=False, # TODO Fix moviepy bug
                                    preset='ultrafast', 
                                    threads=4)

        # moviepy bug : resort to ffmpeg 
        if isfile('output.mp4'): remove('output.mp4')
        os.system(f"ffmpeg -i {out_file} -i {audio_path} -c:v copy -map 0:v:0 -map 1:a:0 -c:a aac -b:a 192k output.mp4")
        

