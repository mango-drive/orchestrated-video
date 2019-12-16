
import os
from os import listdir, remove
from os.path import isfile, join
import time

tload0 = time.time()
import moviepy.editor
from moviepy.editor import  VideoClip,                  \
                            VideoFileClip,              \
                            AudioFileClip,              \
                            CompositeVideoClip
tload1 = time.time()

import ffmpeg
import abc


class VideoEditorComponent(metaclass = abc.ABCMeta):
    video_clips = None
    """
    base video editor component interface for defining methods
    for editing video clips and writing the final edit.
    Will be used as base for moviepy and ffmpeg implementations
    """
    @abc.abstractmethod
    def extract_subclip(self, video_i, start, end):
        pass

    @abc.abstractmethod
    def write_final_edit(self, final_edit, audio_path, output_path):
        pass



class AbstractDecorator(metaclass=abc.ABCMeta):
    _video_editor_component = None
    output_file = 'out.mp3'

    def clear_output_file(self):
        if isfile(self.output_file): remove(self.output_file)

    def __init__(self, component):
        self._component = component
    
    @abc.abstractmethod
    def extract_subclips(self):
        pass

class VideoEditorDecorator(AbstractDecorator):

    def create_edit(self, edit_list):
        self.clear_output_file()
        subclips = self.extract_subclips(edit_list)
        final_edit = self._component.concatenate_videoclips(subclips)
        return final_edit
    
    def write_final_edit(self, final_edit, audio_path, output_path):
        self._component.write_final_edit(final_edit, audio_path, output_path)
    
    def extract_subclips(self,  edit_list):
        video_i = 0
        prev_loc = 0
        subclips = []

        for i, loc in enumerate(edit_list):
            # Cycle through the video list with integer that wraps around
            # the list's length
            video_i =  i % len(self._component.video_clips)

            # Create a subclip of the video, between the previous and current edit
            # locations
            print("Making edit: {} {}".format(prev_loc, loc))
            subclip = self._component.extract_subclip(video_i, prev_loc, loc)

            subclips.append(subclip)

            prev_loc = loc

        return subclips
        
class MoviePyEditor(VideoEditorComponent):

    def __init__(self, session_dir):
        video_paths = [join(session_dir, f) for f in listdir(session_dir) if isfile(join(session_dir, f))]
        self.video_clips = [VideoFileClip(path) for path in video_paths if path.endswith(".mp4")]
    
    def extract_subclip(self, video_i, start, end):
        return self.video_clips[video_i].subclip(start, end)
    
    def concatenate_videoclips(self, subclips):
        return moviepy.editor.concatenate_videoclips(subclips)

    def write_final_edit(self, final_edit, audio_path, output_path):

        print("Writing temp video without audio...")
        final_edit.write_videofile( 'temp.mp4',
                                    audio=False, # TODO Fix moviepy bug
                                    preset='ultrafast', 
                                    threads=4
                                  )

        # moviepy bug : resort to ffmpeg 
        if isfile(output_path): remove(output_path)
        print(f"Writing final video (with audio) to disk at {output_path} using ffmpeg due to moviepy bug...")
        
        os.system(  f"ffmpeg  -loglevel panic                   \
                    -i temp.mp4 -i {audio_path} -c:v copy       \
                    -map 0:v:0 -map 1:a:0 -c:a aac -b:a 192k    \
                    {output_path}"
        )

        os.remove('temp.mp4')
        

class MoviePyClipPlayer:
    def play_video(self, path):
        clip = VideoFileClip(path)
        clip.preview()
    
if __name__ == "__main__":
    video_dir = "./video/session"
    audio_path = "./audio/trap_loop_2.wav"

    t0 = time.time()
    moviepy_editor = MoviePyEditor(video_dir)
    video_decorator = VideoEditorDecorator(moviepy_editor)
    final_edit = video_decorator.create_edit([1, 2, 3, 4, 5, 6, 7])
    video_decorator.write_final_edit(final_edit, audio_path, "output_moviepy.mp4")
    t1 = time.time()

    print(f"Moviepy implementation took {t1-t0} to complete the final edit")
    print(f"Moviepy also took {tload1 - tload0} to load imports including pygame")


