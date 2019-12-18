
import os
from os import listdir, remove
from os.path import isfile, join
import time

import moviepy.editor as mp
from moviepy.editor import (
    VideoClip,
    VideoFileClip, 
    AudioFileClip,
)
import ffmpeg


class MoviePyEditor:
    def __init__(self, video_paths):
        print(video_paths)
        self.video_clips = [VideoFileClip(path) for path in video_paths]

    def create_edit(self, edit_list):
        subclips = self.extract_subclips(edit_list)
        edit = mp.concatenate_videoclips(subclips)
        return edit
        
    def extract_subclips(self,  edit_list):
        video_i = 0
        prev_loc = 0
        subclips = []

        for i, loc in enumerate(edit_list):
            # Cycle through the video list with integer that wraps around
            # the list's length
            video_i =  i % len(self.video_clips)

            # Create a subclip of the video, between the previous and current edit
            # locations
            print("Making edit: {} {}".format(prev_loc, loc))
            subclip = self.extract_subclip(video_i, prev_loc, loc)

            subclips.append(subclip)

            prev_loc = loc

        return subclips
    
    def extract_subclip(self, video_i, start, end):
        return self.video_clips[video_i].subclip(start, end)

        

class MoviePyClipPlayer:
    def play_video(self, path):
        clip = VideoFileClip(path)
        clip.preview()
    

