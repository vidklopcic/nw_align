import argparse
import numpy as np
import bottleneck as bn

parser = argparse.ArgumentParser(description='Align text to the raw probs output from the ASR model')
parser.add_argument('text', type=str, help='text file')
parser.add_argument('--probs', type=str, required=True, help='Numpy probabilities tensor from the ASR model')
parser.add_argument('--character-ms', type=int, default=600)
parser.add_argument('--frame-ms', type=int, default=40)
parser.add_argument('--labels', type=list,
                    default=[' ', 'a', 'b', 'c', 'č', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                             'p', 'r', 's', 'š', 't', 'u', 'v', 'z', 'ž', 'blank'],
                    help='labels')
args = parser.parse_args()
labels = {args.labels[i]: i for i in range(len(args.labels))}


def align(words):
    for word in words:
        w_len = len(word)
        if w_len < 5:
            continue

        n_frames = (w_len * args.character_ms) // args.frame_ms
        print('processing word', word, 'n frames =', n_frames)

        sums = []
        for o in range(p_len - n_frames):
            top_20_n = 5
            window = probs[o:o + n_frames]
            char_top_map = {}
            char_probs_map = {}
            last_top_20_i = []
            for char_i in range(w_len):
                from_i = char_top_map.get(char_i - 1, [-1])[0]
                char_probs = window[:, labels[word[char_i]]]
                top_20_i = np.sort(bn.argpartition(char_probs, top_20_n)[:top_20_n])
                last_top_20_i = top_20_i[np.where(top_20_i > from_i)]
                char_top_map[char_i] = last_top_20_i
                char_probs_map[char_i] = char_probs
                if not len(last_top_20_i):
                    break
            if not len(last_top_20_i):
                continue

            def best_sum(char_i=0, csum=0, t_pos=-1):
                if char_i == w_len:
                    return csum

                bsum = -1e10
                for top_i in char_top_map[char_i]:
                    if top_i < t_pos:
                        continue
                    bsum = max(bsum, best_sum(char_i + 1, csum + char_probs_map[char_i][top_i], top_i))
                return bsum

            bs = best_sum()
            sums.append([o, bs])
        best_pos = sorted(sums, key=lambda x: x[1], reverse=True)[:5]
        print('best position:', [((pos[0] * args.frame_ms) / 1000, pos[1]) for pos in best_pos], 's')


probs = np.load(args.probs)
p_len = len(probs)
with open(args.text, 'r', encoding='utf-8') as f:
    words = ''.join([c for c in f.read().lower() if c in args.labels]).split(' ')

align(words)
