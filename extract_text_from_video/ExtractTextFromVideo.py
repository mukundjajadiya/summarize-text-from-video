import os
import moviepy.editor as mp
from pydantic import DirectoryPath
import speech_recognition as sr
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import en_core_web_sm
from .Cleaner import Cleaner


class ExtractTextFromVideo:
    def __init__(self, videoFilePath, summurisePercentage=0.25, writeOutputText = False):
        self.videoFilePath = videoFilePath
        self.summurisePercentage = summurisePercentage
        self.videoFileName = self.videoFilePath.split("/")[-1].split(".")[0]
        self.outputAudioDirectory = os.path.join("", "audio")

        self.outputAudioFileName = self.videoToAudio(
            videoFilePath=self.videoFilePath, audioDirectoryPath=self.outputAudioDirectory)
        self.videoText = self.audioToText(self.outputAudioFileName)
        self.textSummary = self.summuriseText(
            self.videoText, self.summurisePercentage)

        if writeOutputText:
            self.writeTextToFile(
                text=self.videoText, fileName=f"{self.videoFileName}_text.txt"
            )
            self.writeTextToFile(
                text=self.textSummary, fileName=f"{self.videoFileName}_text_summary.txt"
            )
            
        # delete all unnecessary files
        Cleaner(directoryPath = self.outputAudioDirectory)

    def videoToAudio(self, videoFilePath, audioDirectoryPath="audio"):
        try:

            videoFilename = videoFilePath.split("/")[-1].split(".")[0]
            outputAudioFileName = f"{videoFilename}_output.wav"

            outputAudioFilePath = os.path.join(
                audioDirectoryPath, outputAudioFileName)

            if os.path.exists(outputAudioFilePath):
                print(
                    f"[INFO] Audio file of ({videoFilePath}) already exists.")
                return outputAudioFilePath

            if not os.path.exists(audioDirectoryPath):
                os.makedirs(audioDirectoryPath)

            my_clip = mp.VideoFileClip(videoFilePath)
            print(f"[INFO] Audio extracting from video...")
            my_clip.audio.write_audiofile(outputAudioFilePath)
            print(f"[INFO] Done, Audio extracted from video.")

            return outputAudioFilePath

        except Exception as e:
            print(e)

    def audioToText(self, audioFilePath):
        try:
            if not os.path.exists(audioFilePath):
                print(f"[ERROR] Enter valid file path.")
                return

            r = sr.Recognizer()

            with sr.AudioFile(audioFilePath) as source:
                audio_data = r.record(source)
                print(f"[INFO] Generating text from audio...")
                text = r.recognize_google(audio_data)
                print(f"[INFO] Done, Generating text from audio.")
                print(f"[OUTPUT] {self.videoFileName} to text : \n")
                return text

        except Exception as e:
            print(f"[ERROR] {e}")

    def summuriseText(self, text, percentage):
        try:
            print("[INFO] NLP Model is loading...")
            nlp = en_core_web_sm.load()
            print("[INFO] Done.")

            print("[INFO] Summurising text...")
            doc = nlp(text)
            # tokens=[token.text for token in doc]
            word_frequencies = {}
            for word in doc:
                if word.text.lower() not in list(STOP_WORDS):
                    if word.text.lower() not in punctuation:
                        if word.text not in word_frequencies.keys():
                            word_frequencies[word.text] = 1
                        else:
                            word_frequencies[word.text] += 1
            max_frequency = max(word_frequencies.values())
            for word in word_frequencies.keys():
                word_frequencies[word] = word_frequencies[word] / max_frequency
            sentence_tokens = [sent for sent in doc.sents]
            sentence_scores = {}
            for sent in sentence_tokens:
                for word in sent:
                    if word.text.lower() in word_frequencies.keys():
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word.text.lower(
                            )]
                        else:
                            sentence_scores[sent] += word_frequencies[word.text.lower()]
            select_length = int(len(sentence_tokens) * percentage)
            summary = nlargest(select_length, sentence_scores,
                               key=sentence_scores.get)
            final_summary = [word.text for word in summary]
            print("[INFO] Done.")
            summary = "".join(final_summary)
            return summary

        except Exception as e:
            print(f"[ERROR] {e}")

    def writeTextToFile(
        self, text, fileName="videoToText.txt", outputDirectoryPath="output"
    ):
        try:
            if not text:
                return
            filePath = os.path.join(outputDirectoryPath, fileName)

            if not os.path.exists(outputDirectoryPath):
                os.makedirs(outputDirectoryPath)

            print(f"[INFO] Writing text to file ({fileName}) ...")
            with open(filePath, "w") as f:
                f.write(text)

            print(f"[INFO] Done, writing text to file ({fileName}).")

        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    videoPath = "video/video2.mp4"
    ExtractTextFromVideo(videoPath)
