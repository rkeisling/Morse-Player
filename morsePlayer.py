import string
import math
import wave
import struct

def main():
  pseudoMessage = "hello my name is -what- my name is -who- my name is -chicka chicka slim shady-"
  built_audio = buildAudio(translateMessageToMorse(pseudoMessage))
  save_wav("output.wav", built_audio)

def makeListRemovePunctuationLower(message):
  list_of_words = message.split(' ')
  # just removes all special characters efficiently
  # list_of_words = list_of_words.translate(None, string.punctuation)
  new_list = []
  exclude = set(string.punctuation)
  for word in list_of_words:
      new_word = ''.join(ch for ch in word if ch not in exclude)
      new_list.append(new_word)
  new_list = [word.lower() for word in new_list]
  return new_list

def buildAudio(morseMessage):
  audio = []
  charList = morseMessage.split()
  for char in charList:
    if char == "-":
      audio = append_sinewave(audio, volume=0.25)
    elif char == ".":
      audio = append_sinewave(audio, volume=0.25, duration_milliseconds=1500)
    else:
      audio = append_silence(audio)
  return audio

def translateMessageToMorse(message):
  morseTransList = {
    'a':'.-',
    'b':'-...',
    'c':'-.-.',
    'd':'-..',
    'e':'.',
    'f':'..-.',
    'g':'--.',
    'h':'....',
    'i':'..',
    'j':'.---',
    'k':'-.-',
    'l':'.-..',
    'm':'--',
    'n':'-.',
    'o':'---',
    'p':'.--.',
    'q':'--.-',
    'r':'.-.',
    's':'...',
    't':'-',
    'u':'..-',
    'v':'...-',
    'w':'.--',
    'x':'-..-',
    'y':'-.--',
    'z':'--..',
    '0':'-----',
    '1':'.----',
    '2':'..---',
    '3':'...--',
    '4':'....-',
    '5':'.....',
    '6':'-....',
    '7':'--...',
    '8':'---..',
    '9':'----.'
  }
  ableList = makeListRemovePunctuationLower(message)
  message = []
  for word in ableList:
    trans_word = []
    for letter in word:
        trans_word.append(morseTransList[letter])
        print(letter)
    message.append(' '.join(trans_word))
  finalMorse = "..--".join(message)
  return finalMorse

def append_silence(audio):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    sample_rate = 44100.0
    duration_milliseconds=500
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        audio.append(0.0)

    return audio


def append_sinewave(
        audio,
        freq=440.0,
        duration_milliseconds=500,
        volume=1.0):
    """
    The sine wave generated here is the standard beep.  If you want something
    more aggresive you could try a square or saw tooth waveform.   Though there
    are some rather complicated issues with making high quality square and
    sawtooth waves... which we won't address here :)
    """
    sample_rate = 44100.0
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        audio.append(volume * math.sin(2 * math.pi * freq * ( x / sample_rate )))

    return audio


def save_wav(file_name, audio):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")

    # wav params
    nchannels = 1
    sample_rate = 44100.0
    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

    return

if __name__ == '__main__':
    main()
