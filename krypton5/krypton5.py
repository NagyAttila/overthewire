import datetime

FILE_NAMES = ['./found1','./found2', './found3', './krypton6']
MAX_CYPHER_LENGTH = 20

# English Letter Frequency
# Based on: https://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html
gt_freq = dict()
gt_freq['E'] = 12.02
gt_freq['T'] = 9.10
gt_freq['A'] = 8.12
gt_freq['O'] = 7.68
gt_freq['I'] = 7.31
gt_freq['N'] = 6.95
gt_freq['S'] = 6.28
gt_freq['R'] = 6.02
gt_freq['H'] = 5.92
gt_freq['D'] = 4.32
gt_freq['L'] = 3.98
gt_freq['U'] = 2.88
gt_freq['C'] = 2.71
gt_freq['M'] = 2.61
gt_freq['F'] = 2.30
gt_freq['Y'] = 2.11
gt_freq['W'] = 2.09
gt_freq['G'] = 2.03
gt_freq['P'] = 1.82
gt_freq['B'] = 1.49
gt_freq['V'] = 1.11
gt_freq['K'] = 0.69
gt_freq['X'] = 0.17
gt_freq['Q'] = 0.11
gt_freq['J'] = 0.10
gt_freq['Z'] = 0.07

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def decrypt_char(c, s):
    p = ord(c) - ord(s)
    if p < 0:
        p += len(alphabet)
    return chr(p + ord('A'))

def decrypt_text(encrypted, secret):
    ln = len(secret)
    plaintext = ""
    for i,c in enumerate(encrypted):
        s = secret[i%ln]
        plainchar = decrypt_char(c,s)
        plaintext += plainchar
    return plaintext


def is_key(s):
    global PART_SIZE
    return len(s) == PART_SIZE

def get_freq(text):

    freq = dict()
    for c in alphabet:
        freq[c] = 0

    total = 0
    for c in text:
        freq[c] += 1
        total += 1

    for k,v in freq.items():
        freq[k] = (v/total) * 100

    return freq

def sum_diff(a, b):
    total = 0
    for c in alphabet:
        total += abs(a[c] - b[c])
    return total

def calculate_score(part_index, secret):
    score = 0

    plaintext = ""
    for text in texts:
        part = get_part(text, part_index)
        plaintext += decrypt_text(part, secret)

    text_freq = get_freq(plaintext)

    score = sum_diff(gt_freq, text_freq)

    return score

def get_secrets(secret):
    secrets = []
    if is_key(secret):
        secrets = [secret]
    else:
        for c in alphabet:
            secrets += get_secrets(secret+c)
    return secrets

def get_part(encrypted, i):
    global SECRET_SIZE
    global N_PARTS
    global PART_SIZE

    n = len(encrypted)
    froms = range(i*PART_SIZE, n-1, SECRET_SIZE)
    tos = range(i*PART_SIZE+PART_SIZE, n, SECRET_SIZE)
    ranges = zip(froms, tos)

    part = ""
    for start, end in ranges:
        part += encrypted[start:end]

    return part


# Main
if __name__ == '__main__':
    print(datetime.datetime.now())

    texts = []
    for file_name in FILE_NAMES:
        f = open(file_name)
        text = f.readline()
        text = text.replace(" ", "")
        texts.append( text )

    finalSolution = ''
    finalMinScore = 1000
    for secret_size in range(1,MAX_CYPHER_LENGTH):

        N_PARTS = secret_size
        SECRET_SIZE = secret_size
        PART_SIZE = int(SECRET_SIZE / N_PARTS)

        secrets = get_secrets("")
        solution = ''

        for i in range(N_PARTS):
            sub_solution = ''
            minScore = 1000
            for secret in secrets:
                score = calculate_score(i, secret)
                if score < minScore:
                    minScore = score
                    sub_solution = secret
            solution += sub_solution
        print("\nKey: " + solution + "\nPassword: " + decrypt_text(text, solution) + "\nScore: " + str(minScore))

        if minScore < finalMinScore:
            finalMinScore = minScore
            finalSolution = solution

print("\n\n### Final Solution:")
print("\nKey: " + finalSolution + "\nPassword: " + decrypt_text(text, finalSolution) + "\nScore: " + str(finalMinScore))
for name, text in zip(FILE_NAMES, texts):
    print("\n" + name + ":\n " + decrypt_text(text, finalSolution))
