import sys
import os
from os import listdir, remove
from os.path import isfile, join
from audio_analysis import AudioFile, Filter, AudioProcessingChain, OnsetExtractor
from video_edit import MoviePyEditor, MoviePyClipPlayer
import file_structure

if __name__ == '__main__':
    if len(sys.argv) == 1:
        audio_filename = "trap_loop_2.wav"
    else:
        sys.argv[1]

    audio_path = f"./audio/{audio_filename}"

    print("Loading audio: ", audio_path)
    audio_file = AudioFile(audio_path)

    lowpass = Filter()
    pre_process_chain = AudioProcessingChain()
    pre_process_chain.set_next(lowpass)

    oe = OnsetExtractor()
    print("Applying pre-processing to the audio...")
    samples = pre_process_chain.process(audio_file.samples)
    
    print("Using onset extractor to create an edit list")
    edit_list = oe.extract_onsets(samples)
    print("The onset extractor found musical onsets at seconds:\n " , edit_list)

    # load videos in session dir into the editor
    video_paths = file_structure.list_videos_in(file_structure.session_dir)
    mpy_editor = MoviePyEditor(video_paths)
    # cut the videos at the edit list markers, get the concatenated result
    mpy_video = mpy_editor.create_edit(edit_list)


    output_video_path = file_structure.write_moviepy_video(mpy_video, audio_path)

    moviepy_player = MoviePyClipPlayer()
    moviepy_player.play_video(output_video_path)
    


    

    
