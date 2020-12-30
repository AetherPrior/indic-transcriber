import os
import glob
import argparse
import pandas as pd


def get_transcripts(transcript_path):
    if not os.path.exists(transcript_path):
        return None
    transcripts = list()
    with open(transcript_path, 'r') as file:
        for line in file:
            transcripts.append(line)

    assert len(transcripts) == 720, "[ERROR] The number of unique transcripts is not sufficient"
    return transcripts

def process_dataset(data_path, transcript_path):
    data = []
    transcripts = get_transcripts(transcript_path)
    assert transcripts is not None, "[ERROR] The transcript file does not exist"
    if not os.path.exists(data_path) or not os.path.isdir(data_path):
        print('[ERROR] The specified data path does not exist')

    data_path = data_path + "/**/*.wav"
    for sound in glob.glob(data_path, recursive=True):
        name = os.path.basename(sound)
        name = name.split('.')[0]
        req_transcript = int(name.split('_')[-1])
        data.append([sound, transcripts[req_transcript]])

    df = pd.DataFrame(data, columns=['path', 'transcript'])
    df.to_csv('./dataset.csv')

    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--datapath', type=str, required=True,
                        help='Path to folder containing sound files')
    parser.add_argument('-t', '--transcript', type=str, default='./transcripts.txt',
                        help='Path to text file containing transcripts in sequential order.')
    args = vars(parser.parse_args())
    
    process_dataset(data_path=args['datapath'],
                    transcript_path=args['transcript'])