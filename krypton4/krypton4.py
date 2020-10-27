import datetime

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
maxScore = 0

def decryptChar(c,s):
    p = ord(c) - ord(s)
    if p < 0:
        p += 26
    return chr(p + ord('A'))

def decryptText(secret):
    ln = len(secret)
    plaintext = ""
    for i,c in enumerate(encrypted):
        s = secret[i%ln]
        plainchar = decryptChar(c,s)
        plaintext += plainchar
    return plaintext


def isKey(s):
    return len(s) == 6

def calculateScore(secret):
    the = "THE"
    score = 0

    # Decipher
    plaintext = decryptText(secret)

    # Count "THE"
    score = str(plaintext).count(the)

    return score

def backtrack(secret):
    global maxScore
    if isKey(secret):
        score = calculateScore(secret)
        if score > maxScore:
            maxScore = score
            solution = secret
            print(score, secret)
            print(decryptText(secret))
        return
    else:
        for c in alphabet:
            backtrack(secret+c)

# Main
print(datetime.datetime.now())
f = open("./found1")
encrypted = f.readline()
encrypted = encrypted.replace(" ", "")
backtrack("")
print(datetime.datetime.now())

