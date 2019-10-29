def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    i = 0
    ciphertext = ""
    while i < len(plaintext):
        if ord("a") <= ord(plaintext[i]) <= ord("w"):
            x = ord(plaintext[i]) + 3
            y = chr(x)
            ciphertext += y
            i +=1
        elif ord("A") <= ord(plaintext[i]) <= ord("W"):
            x = ord(plaintext[i]) + 3 
            y = chr(x)
            ciphertext += y
            i += 1
        elif ord("x") <= ord(plaintext[i]) <= ord("z"):
            x = ord(plaintext[i]) - 23
            y = chr(x)
            ciphertext += y
            i +=1
        elif ord("X") <= ord(plaintext[i]) <= ord("Z"):   
            x = ord(plaintext[i]) - 23
            y = chr(x)
            ciphertext += y
            i +=1
        else:
            ciphertext += plaintext[i]
            i += 1
    return ciphertext
def decrypt_caesar(ciphertext):
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    i = 0
    plaintext = ""
    while i < len(ciphertext):
        if ord("d") <= ord(ciphertext[i]) <= ord("z"):
            x = ord(ciphertext[i]) - 3
            y = chr(x)
            plaintext += y
            i +=1
        elif ord("D") <= ord(ciphertext[i]) <= ord("Z"):
            x = ord(ciphertext[i]) - 3 
            y = chr(x)
            plaintext += y
            i += 1
        elif ord("a") <= ord(ciphertext[i]) <= ord("c"):
            x = ord(ciphertext[i]) + 23
            y = chr(x)
            plaintext += y
            i +=1
        elif ord("A") <= ord(ciphertext[i]) <= ord("C"):
            x = ord(ciphertext[i]) + 23
            y = chr(x)
            plaintext += y
            i +=1
        else:
            plaintext += ciphertext[i]
            i += 1
    return plaintext