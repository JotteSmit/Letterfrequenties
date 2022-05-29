import string
from collections import Counter


def get_alphabet_listed_with_white_space():
    alphabet_string = string.ascii_lowercase
    alphabet_list = list(alphabet_string)
    alphabet_list.extend([' '])
    return alphabet_list


def create_matrix():
    alphabet_listed_with_white_space = get_alphabet_listed_with_white_space()
    alphabet_listed_with_white_space.extend(['%'])
    matrix = {key: {key: 0 for key in alphabet_listed_with_white_space} for key in alphabet_listed_with_white_space}
    return matrix


def update_matrix(matrix, sentence):
    sentence = sentence.lower()
    alphabet_listed_with_white_space = get_alphabet_listed_with_white_space()
    sentence_length = len(sentence) - 1
    for index, letter in enumerate(sentence):
        if letter not in alphabet_listed_with_white_space:
            letter = '%'
        if index == sentence_length:
            pass
        else:
            next_letter = sentence[index + 1]
            if next_letter not in alphabet_listed_with_white_space:
                next_letter = '%'
            matrix[letter][next_letter] += 1
    return matrix


def set_probabilities_of_matrix(matrix):
    for letter_from in matrix:
        count = 0
        for letter_to in matrix[letter_from]:
            count += matrix[letter_from][letter_to]
        for letter_to in matrix[letter_from]:
            if matrix[letter_from][letter_to] > 0:
                matrix[letter_from][letter_to] = matrix[letter_from][letter_to] / float(count)
    return matrix


def get_probability_from_matrix(matrix, sentence):
    sentence = sentence.lower()
    alphabet_listed_with_white_space = get_alphabet_listed_with_white_space()
    sentence_length = len(sentence) - 1
    probability = 0
    for index, letter in enumerate(sentence):
        if letter not in alphabet_listed_with_white_space:
            letter = '%'
        if index == sentence_length:
            pass
        else:
            next_letter = sentence[index + 1]
            if next_letter not in alphabet_listed_with_white_space:
                next_letter = '%'
            probability += matrix[letter][next_letter]
    return probability


def train_language_matrix(file_name):
    matrix = create_matrix()
    with open(file_name, encoding='utf8') as f:
        lines = [line.strip() for line in f if line.strip()]
    for line in lines:
        update_matrix(matrix, line)
    matrix_with_probabilities = set_probabilities_of_matrix(matrix)
    return matrix_with_probabilities


def get_language_from_sentence(dutch_matrix, english_matrix, sentence):
    dutch_probability = get_probability_from_matrix(dutch_matrix, sentence)
    english_matrix = get_probability_from_matrix(english_matrix, sentence)
    if dutch_probability > english_matrix:
        return "dutch"
    else:
        return "english"


def main():
    english_matrix = train_language_matrix('alice_en.txt')
    dutch_matrix = train_language_matrix('gutenberg_nl.txt')
    with open('mixed_sentences.txt', encoding='utf8') as f:
        lines = [line.strip() for line in f if line.strip()]
    cnt = Counter()
    for line in lines:
        cls = get_language_from_sentence(dutch_matrix, english_matrix, line)
        cnt[cls] += 1
    print(cnt)


main()
