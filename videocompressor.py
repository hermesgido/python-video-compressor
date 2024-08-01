import ffmpeg
import os


def compress_video(input_file, output_file, target_size):
    try:
        probe = ffmpeg.probe(input_file)
        duration = float(probe['format']['duration'])

        min_bitrate = 500000  # in bits per second

        target_bitrate = max(
            (target_size * 1024 * 1024 * 8) / duration, min_bitrate)
        # Convert to kbps for ffmpeg
        target_bitrate_k = int(target_bitrate / 1000)

        video_codec = 'libx264'
        audio_codec = 'aac'

        ffmpeg.input(input_file).output(
            output_file,
            **{
                'b:v': f'{target_bitrate_k}k',
                'c:v': video_codec,
                'c:a': audio_codec,
                'strict': 'experimental'
            }
        ).overwrite_output().run()

        compressed_size = os.path.getsize(output_file) / (1024 * 1024)
        if compressed_size > target_size:
            print(
                f"Warning: Compressed video size ({compressed_size:.2f} MB) exceeds target size ({target_size} MB).")
        else:
            print(f"Compressed video size: {compressed_size:.2f} MB")
    except ffmpeg.Error as e:
        print(f"An error occurred: {e.stderr.decode()}")


# Input video file
input_video = '/home/hermes/now.mkv'

# Output video file
output_video = '/home/hermes/output.mp4'

# Target size in MB
target_size_mb = 200

compress_video(input_video, output_video, target_size_mb)
