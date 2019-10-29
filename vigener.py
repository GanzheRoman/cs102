def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    new_keyword = ''
    for i in range(len(plaintext)):
        num_word = ord(plaintext[i])
        while len(plaintext) > len(new_keyword):
            new_keyword += keyword
        num_key = ord(new_keyword[i])
        if num_key <= 90:
            num_key -= 65
        elif num_key >= 97:
            num_key -= 97
        if num_word <= 90:
            if (num_key+num_word) > 90:
                num_word -= 26
        else:
            if (num_key+num_word) > 122:
                num_word -= 26
        ciphertext += chr(num_word+num_key)
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    new_keyword = ''
    for i in range(len(ciphertext)):
        num_word = ord(ciphertext[i])
        while len(ciphertext) > len(new_keyword):
            new_keyword += keyword
        num_key = ord(new_keyword[i])
        if num_key <= 90:
            num_key -= 65
        elif num_key >= 97:
            num_key -= 97
        if num_word <= 90:
            if (num_word-num_key) < 65:
                num_word += 26
        else:
            if (num_word-num_key) < 97:
                num_word += 26
        plaintext += chr(num_word-num_key)
    return plaintext