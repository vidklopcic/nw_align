import numpy as np

DIR_D = 1
DIR_H = 2
DIR_V = 3


# pythran export align(float[:,:], int[], float[], float[], int)
def align(
        probs: np.ndarray,
        text: np.ndarray,
        h_gap_penalty_for_len: np.ndarray,
        v_gap_penalty_for_len: np.ndarray,
        h_penalty_exempt=None
):
    """
    Implementation of Needleman-Wunsch intended for alignment of text to the raw output from ASR models.

    :param probs: list of logprob vectors from the ASR model
    :param text: list of corresponding indexes of tokens/characters (eg. i-th probability from the logprob vector)
    :param h_gap_penalty_for_len: for gap in text of length x, min(x, last)-th penalty will be taken from this list
    :param v_gap_penalty_for_len: for gap in probs of length y, min(y, last)-th penalty will be taken from this list
    :param h_penalty_exempt: if equals text[i], do not add the corresp. h_gap_penalty_for_len
    :return: alignment_score, aligned_probs, aligned_text
    """

    def gen_mat():
        len_text = text.shape[0]
        len_probs = probs.shape[0]

        # fill with small value, so when index = -1 (first row / col), initial prob is the lowest
        m_score = np.zeros((len_text + 1, len_probs + 1))

        for i_char in range(1, len_text + 1):
            i_v_gap = min(i_char - 1, v_gap_penalty_for_len.size - 1)
            m_score[i_char, 0] = m_score[i_char - 1, 0] + v_gap_penalty_for_len[i_v_gap]

        for i_frame in range(1, len_probs + 1):
            i_h_gap = min(i_frame - 1, h_gap_penalty_for_len.size - 1)
            m_score[0, i_frame] = m_score[0, i_frame - 1] + h_gap_penalty_for_len[i_h_gap]

        m_trace = np.zeros((len_text + 1, len_probs + 1), dtype=np.int8)
        m_trace[0] = [DIR_H] * (len_probs + 1)
        m_trace[:, 0] = [DIR_V] * (len_text + 1)
        m_trace[0, 0] = 0

        lens_v_gap = np.zeros(len_probs + 1, dtype=np.int32)

        for i_char in range(1, len_text + 1):
            len_h_gap = 0
            for i_frame in range(1, len_probs + 1):
                char = text[i_char - 1]
                p_char = probs[i_frame - 1][char]
                p_above = m_score[i_char - 1][i_frame]
                p_left = m_score[i_char][i_frame - 1]
                p_diag = m_score[i_char - 1][i_frame - 1]
                len_v_gap = lens_v_gap[i_frame - 1]

                if p_left <= p_diag >= p_above:
                    m_score[i_char][i_frame] = p_diag + p_char
                    m_trace[i_char][i_frame] = DIR_D
                    len_h_gap = 0
                    lens_v_gap[i_frame] = 0
                elif p_left >= p_above:
                    if char == h_penalty_exempt:
                        gap = 0
                    else:
                        i_h_gap = min(len_h_gap, h_gap_penalty_for_len.size - 1)
                        gap = h_gap_penalty_for_len[i_h_gap]
                    m_score[i_char][i_frame] = p_left + gap
                    m_trace[i_char][i_frame] = DIR_H
                    len_h_gap += 1
                    lens_v_gap[i_frame] = 0
                else:
                    i_v_gap = min(len_v_gap, v_gap_penalty_for_len.size - 1)
                    m_score[i_char][i_frame] = p_above + v_gap_penalty_for_len[i_v_gap]
                    m_trace[i_char][i_frame] = DIR_V
                    lens_v_gap[i_frame] = len_v_gap + 1
                    len_h_gap = 0
        return m_score, m_trace

    score, trace = gen_mat()

    traceback_probs = []
    traceback_text = []
    i_trace = [trace.shape[0] - 1, trace.shape[1] - 1]
    while trace[i_trace[0], i_trace[1]]:
        dir = trace[i_trace[0], i_trace[1]]
        if dir == DIR_D:
            traceback_probs.append(list(probs[i_trace[1] - 1]))
            traceback_text.append(text[i_trace[0] - 1])
            i_trace[0] -= 1
            i_trace[1] -= 1
        if dir == DIR_H:
            traceback_probs.append(list(probs[i_trace[1] - 1]))
            traceback_text.append(None)
            i_trace[1] -= 1
        if dir == DIR_V:
            traceback_probs.append(None)
            traceback_text.append(text[i_trace[0] - 1])
            i_trace[0] -= 1

    traceback_text.reverse()
    traceback_probs.reverse()
    return score[-1, -1], traceback_text, traceback_probs
