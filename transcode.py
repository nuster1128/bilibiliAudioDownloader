import ffmpeg
import os


def get_info(file_path):
	print(file_path)
	full_info = dict(ffmpeg.probe(file_path))
	return full_info.get("format").get("bit_rate")


if __name__ == '__main__':
	default_root_path = "download"
	if not os.path.exists("download/output"):
		os.mkdir("download/output")
	for file in os.listdir(default_root_path):
		if not (file.endswith(".mp3") or file.endswith(".flac")):
			continue
		path = os.path.join(default_root_path, file)
		outputPath = os.path.join("download/output", file)
		print(outputPath)
		bitrate = get_info(path)
		print(bitrate)
		a_codec = ffmpeg.probe(path)['streams'][0]['codec_name']
		if a_codec == "aac":
			a_codec = "mp3"
		print(a_codec)
		try:
			(
				ffmpeg
				.input(path)
				.output(outputPath, audio_bitrate=bitrate, acodec=a_codec)
				.overwrite_output()
				.run(capture_stderr=True)
			)
		except ffmpeg.Error as e:
			print(e.stderr.decode('utf-8'))