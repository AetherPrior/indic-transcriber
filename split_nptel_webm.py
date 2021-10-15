import os
import subprocess
from datetime import datetime

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
                    ## skip the first occurrence, usually faulty
                    start+=1
                    while(linelist[start].find('-->') == -1):
                        start += 1

                    i = start
                    while(i < len(linelist)):
                        #print(linelist[i])
                        startstamp, endstamp = linelist[i].split('-->')
                        caption = ""

                        i += 1
                        while(i < len(linelist) and (linelist[i].find('-->') == -1)):
                            caption += linelist[i]
                            i += 1

                        stampslist['data'].append({'timestamp': [startstamp.strip(), endstamp.strip()],
                                           'captions': " ".join(caption.split())})
                yield stampslist


def convert_to_wav(dir):
    os.chdir(dir)
    for roots, dirs, files in os.walk('.'):
        for sub in files:
            if(sub.split('.')[-1] == 'webm'):
                name = sub.split('.')[0]
                subprocess.Popen(
                    ['ffmpeg', '-i', f'\"./nptel/DSA/{sub}\"', '-c:a', 'pcm_f32le', f'\".nptel/DSA/{name}\".wav'])


def get_audio_from_subs(stampslist,datadir='./nptel/DSA/'):
    a_prefix = stampslist['file'].split('.')[0]
    audio = a_prefix+".webm"
    outdir = os.path.join(datadir,a_prefix)
    os.makedirs(outdir, exist_ok=True)
    
    for data in stampslist['data']:

        ss = datetime.strptime(data['timestamp'][0],"%H:%M:%S.%f")
        t = datetime.strptime(data['timestamp'][1],"%H:%M:%S.%f") - ss
        
        audiofile = os.path.join(datadir,audio)
        outfile = os.path.join(outdir,a_prefix+data['timestamp'][0]+'.webm')
        
        #append a singular zero to timedelta 
        timed = "0"+str(t)[:-3]

        # split the audio
        subprocess.Popen(['ffmpeg','-i',f'{audiofile}','-ss', f'{datetime.strftime(ss,"%H:%M:%S.%f")}', '-t', f'{timed}',f'{outfile}'])
        
        # store the transcript
        with open(os.path.join(outdir, a_prefix+data['timestamp'][0]+".txt"),'w') as f:
            f.write(data['captions'])



if __name__ == '__main__':
    # convert_to_wav('./nptel/DSA')
    lis = get_subs_webm('./nptel/DSA')
    get_audio_from_subs(next(lis))
