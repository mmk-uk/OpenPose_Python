from __future__ import division

import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from multiprocessing import Value, Array, Process
import pyaudio
from six.moves import queue
import pyxel

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

def changechannel(now,x):
    if x == 1:
        now+=1
    if x == -1:
        now-=1
    return now%8


def channelToImage(c):
    if c == 1:
        return 8
    if c == 2:
        return 3
    if c == 3:
        return 8
    if c == 4:
        return 9
    if c == 5:
        return 14
    if c == 6:
        return 12
    if c == 7:
        return 10
    if c == 8:
        return 6
    if c == 9:
        return 2
def volumeChange(vol,x):
    if x == 1:
        if vol<30:
            vol += 1

    if x == -1:
        if 0<vol:
            vol -= 1

    return vol

class TV:
    def __init__(self,onoff,vol,volcon,now):
        self.channel = [1,2,4,5,6,7,8,9]
        self.volcon = volcon
        self.range = 0
        self.onoff = onoff
        print(type(self.onoff))
        self.vol = vol
        self.now = now
        pyxel.init(60, 45)
        pyxel.run(self.update,self.draw)


    def update(self):

        if self.onoff.value == 1:

            if pyxel.btnr(pyxel.KEY_RIGHT):
                self.now.value = changechannel(self.now.value,1)
            if pyxel.btnr(pyxel.KEY_LEFT):
                self.now.value = changechannel(self.now.value,-1)
            if pyxel.btnr(pyxel.KEY_UP):
                pyxel.cls(channelToImage(self.channel[self.now.value]))
                pyxel.text(int(pyxel.width)-5, 5, str(self.channel[self.now.value]), 0)
                self.vol.value = volumeChange(self.vol.value,1)
                self.volcon.value = 50


            if pyxel.btnr(pyxel.KEY_DOWN):
                pyxel.cls(channelToImage(self.channel[self.now.value]))
                pyxel.text(int(pyxel.width)-5, 5, str(self.channel[self.now.value]), 0)
                self.vol.value = volumeChange(self.vol.value,-1)
                self.volcon.value = 50

        if pyxel.btnr(pyxel.KEY_O) and self.onoff.value==1:
            self.onoff.value = False
            self.range = int(pyxel.height/2)
            self.volcon.value = 0

        if pyxel.btnr(pyxel.KEY_I) and self.onoff.value==0:
            self.onoff.value = True
            self.range = 0
            print(self.onoff.value)

    def draw(self):

        if self.onoff.value == 1:
            pyxel.cls(channelToImage(self.channel[self.now.value]))
            if self.range < int(pyxel.height/2):
                pyxel.rect(0, int(pyxel.height/2)-self.range, pyxel.width, self.range*2, 7)
                self.range += 5
            pyxel.text(5, 5, str(self.channel[self.now.value]), 0)

        else:
            pyxel.cls(0)
            if 0 < self.range:
                pyxel.rect(0, int(pyxel.height/2)-self.range, pyxel.width, self.range*2, 7)
                self.range -= 5


        if self.volcon.value > 0:
            pyxel.text(int(pyxel.width/2), int(pyxel.height)-5, "vol:{}".format(self.vol.value), 0)
            self.volcon.value -= 1

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

def listen_print_loop(responses,onoff,vol,volcon,now):
    num_chars_printed = 0
    ts_before = ""
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        #transcriptに
        transcript = result.alternatives[0].transcript

        if (transcript.endswith("テレビをつけて") or transcript.endswith("テレビつけて"))and ts_before != transcript:
            print("TVON!")
            onoff.value = 1
        if (transcript.endswith("テレビを消して") or transcript.endswith("テレビ消して")) and ts_before != transcript:
            print("TVOFF!")
            onoff.value = 0
        if transcript.endswith("次のチャンネルにして") and ts_before != transcript:
            print("channel up!")
            now.value = changechannel(now.value,1)
        if transcript.endswith("前のチャンネルにして") and ts_before != transcript:
            print("channel down!")
            now.value = changechannel(now.value,-1)
        if (transcript.endswith("音量を上げて") or transcript.endswith("音量上げて")) and ts_before != transcript:
            print("volume up!")
            vol.value = volumeChange(vol.value,1)
            volcon.value = 50
        if (transcript.endswith("音量を下げて") or transcript.endswith("音量下げて")) and ts_before != transcript:
            print("volume down!")
            vol.value = volumeChange(vol.value,-1)
            volcon.value = 50

        ts_before = transcript

        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)
            #print(transcript)
            #print(overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0

def main(onoff,vol,volcon,now):
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'ja-JP'  # a BCP-47 language tag

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses,onoff,vol,volcon,now)

if __name__ == '__main__':
    onoff = Value('i', 0)
    vol = Value('i', 10)
    volcon = Value('i', 0)
    now = Value('i', 0)

    th1 = Process(target=main,args=[onoff,vol,volcon,now])
    th1.start()

    TV(onoff,vol,volcon,now)
