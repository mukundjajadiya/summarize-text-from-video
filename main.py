from extract_text_from_video import ExtractTextFromVideo

if __name__ == "__main__":
    videoPath = "video/testVideo.mp4"

    # if you want to write output text to a file do EXtractTextFromVideo(writeOutputText=True)
    video_text = ExtractTextFromVideo(videoPath)

    # get entire video text
    text_from_video = video_text.videoText
    print(text_from_video)

    # get entire video text summary
    summary_text_from_video = video_text.textSummary
    print(summary_text_from_video)
