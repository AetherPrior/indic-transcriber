import os
import sys
import subprocess


def get_subs_webm(dir):
    for root, dirs, files in os.walk(dir):

        for subtitle in files:

            if(subtitle.split('.')[-1] == 'vtt'):
                stampslist = {'file': subtitle, 'data': []}

                with open(os.path.join(dir, subtitle)) as timestamps:
                    # skip header
                    start = 0
                    linelist = timestamps.readlines()

                    while(linelist[start].find('-->') == -1):
                        start += 1

                    i = start
                    while(i < len(linelist)):
                        print(linelist[i])
                        startstamp, endstamp = linelist[i].split('-->')
                        caption = ""

                        i += 1
                        while(i < len(linelist) and (linelist[i].find('-->') == -1)):
                            caption += linelist[i]
                            i += 1

                        stampslist.append({'timestamp': [startstamp, endstamp],
                                           'captions': caption})
                yield stampslist


def convert_to_wav(dir):
    os.chdir(dir)
    for roots, dirs, files in os.walk('.'):
        for sub in files:
            if(sub.split('.')[-1] == 'webm'):
                name = sub.split('.')[0]
                subprocess.Popen(
                    ['ffmpeg', '-i', f'./nptel/DSA/\'{sub}\'', '-c:a pcm_f32le', f'.nptel/DSA/\'{name}\'.wav'])


def get_audio_from_subs(stampslist):
    audio = stampslist['file'].split('.')[0]+".webm"
    # TODO


if __name__ == '__main__':
    convert_to_wav('./nptel/DSA')
    # lis = get_subs_webm('./nptel/DSA')
    # print(next(lis))
