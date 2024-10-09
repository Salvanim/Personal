from moviepy.editor import *

def audio_to_video_with_black_bg(audio_path, output_path, resolution=(1920, 1080), fps=24):
    # Load audio file
    audio = AudioFileClip(audio_path)

    # Create a black video clip with the same duration as the audio
    black_clip = ColorClip(size=resolution, color=(0, 0, 0), duration=audio.duration)

    # Set the audio to the black video clip
    video_clip = black_clip.set_audio(audio)

    # Set frames per second (FPS)
    video_clip = video_clip.set_fps(fps)

    # Write the video file to the output path
    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Example usage:
audio_path = r"C:\Users\dylan\OneDrive\Desktop\combined_audio.wav"
output_path = r"C:\Users\dylan\OneDrive\Desktop\combined_audio.mp4"

audio_to_video_with_black_bg(audio_path, output_path)
