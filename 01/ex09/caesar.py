import sys

def is_latin_character(char):
    return ('a' <= char <= 'z') or ('A' <= char <= 'Z')

def shift_char(char, shift, decode=False):
    if not is_latin_character(char):
        return char
    shift = -shift if decode else shift
    if char.islower():
        return chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
    else:
        return chr((ord(char) - ord('A') + shift) % 26 + ord('A'))

def caesar_cipher(text, shift, decode=False):
    allowed_punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    result = []
    for char in text:
        if not is_latin_character(char) and not char.isdigit() and not char.isspace() and char not in allowed_punctuation:
            raise Exception("The script does not support your language yet")
        result.append(shift_char(char, shift, decode))
    return ''.join(result)

def main():
    if len(sys.argv) != 4:
        raise Exception("Invalid number of arguments")

    action, text, shift = sys.argv[1], sys.argv[2], int(sys.argv[3])

    if action not in ['encode', 'decode']:
        raise Exception("Invalid action. Use 'encode' or 'decode'.")

    if action == 'encode':
        result = caesar_cipher(text, shift)
    else:
        result = caesar_cipher(text, shift, decode=True)

    print(result)

if __name__ == "__main__":
    main()
