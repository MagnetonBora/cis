
import string

FILE_NAME = 'names.txt'

with open(FILE_NAME) as file_handler:
    lines = file_handler.readlines()

words = set(lines)
words = list(words)

capital_letters = set(string.ascii_uppercase)

names = [word for word in words if word[0] in capital_letters]

with open('names.dat', 'w') as out_file:
    out_file.writelines(names)

if __name__ == '__main__':
    pass
