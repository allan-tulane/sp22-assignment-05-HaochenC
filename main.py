
####### Problem 3 #######

test_cases = [('book', 'back'), ('kookaburra', 'kookybird'), ('elephant', 'relevant'), ('AAAGAATTCA', 'AAATCA')]
alignments = [('book', 'back'), ('kookaburra', 'kookybird-'), ('relev-ant','-elephant'), ('AAAGAATTCA', 'AAA---T-CA')]

def MED(S, T):
    # TO DO - modify to account for insertions, deletions and substitutions
    if (S == ""):
        return(len(T))
    elif (T == ""):
        return(len(S))
    else:
        if (S[0] == T[0]):
            return(MED(S[1:], T[1:]))
        else:
            return(1 + min(MED(S, T[1:]), MED(S[1:], T), MED(S[1:], T[1:]))) # done

def fast_MED(S, T, MED={}):
    # TODO -  implement memoization
    if S == "" or T == "":
        return max(len(T), len(S))
    else:
        if (S, T) in MED:
            return MED[(S, T)]
        else:
            if S[0] == T[0]:
                MED[(S, T)] = fast_MED(S[1:], T[1:])
            else:
                MED[(S, T)] = 1 + min(fast_MED(S, T[1:]), fast_MED(S[1:], T), fast_MED(S[1:], T[1:]))
            return MED[(S, T)]


def fast_align_MED(S, T, MED={}):
    # TODO - keep track of alignment
    if S == "":
        MED[(S, T)] = ['-'*len(T), T, len(T)]
        return '-'*len(T), T
    if T == "":
        MED[(S, T)] = [S, '-'*len(S), len(S)]
        return S, '-'*len(S)
    else:
        if (S, T) in MED:
            return MED[(S, T)][0], MED[(S, T)][1]
        else:
            if S[0] == T[0]:
                X, Y =  fast_align_MED(S[1:], T[1:])
                MED[(S, T)] = [S[0] + X, T[0] + Y, MED[(S[1:], T[1:])][2]]
            else:
                Xadd, Yadd = fast_align_MED(S, T[1:])
                Xdel, Ydel = fast_align_MED(S[1:], T)
                Xsub, Ysub = fast_align_MED(S[1:], T[1:])
                cost = 1 + min(MED[(S, T[1:])][2], MED[(S[1:], T)][2], MED[(S[1:], T[1:])][2])
                if cost - 1 == MED[(S[1:], T[1:])][2]:
                    MED[(S, T)] = [S[0] + Xsub, T[0] + Ysub, cost]
                elif cost - 1 == MED[(S, T[1:])][2]:
                    MED[(S, T)] = ['-' + Xadd, T[0] + Yadd, cost]
                else:
                    MED[(S, T)] = [S[0] + Xdel, '-' + Ydel, cost]
            return MED[(S, T)][0], MED[(S, T)][1]

def test_MED():
    for S, T in test_cases:
        assert fast_MED(S, T) == MED(S, T)
                                 
def test_align():
    for i in range(len(test_cases)):
        S, T = test_cases[i]
        align_S, align_T = fast_align_MED(S, T)
        assert (align_S == alignments[i][0] and align_T == alignments[i][1])

if __name__ == '__main__':
    test_align()