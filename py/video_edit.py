import os
from os import listdir, remove
from os.path import isfile, join
from moviepy.editor import  VideoClip,                  \
                            VideoFileClip,              \
                            AudioFileClip,              \
                            concatenate_videoclips,     \
                            CompositeVideoClip
import ffmpeg


class MoviePyEditor:
    def __init__(self, video_paths):
        print(video_paths)
        self.video_clips = [VideoFileClip(path) for path in video_paths]

    def create_edit(self, edit_list):
        subclips = self.extract_subclips(self.video_clips, edit_list)

        print("Concatenating clips")
        final_edit = concatenate_videoclips(subclips, 
                                            method='compose')

        return final_edit

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
        

class MoviePyClipPlayer:
    def play_video(self, path):
        clip = VideoFileClip(path)
        clip.preview()





