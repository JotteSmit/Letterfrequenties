import string
import sys


def get_alphabet_array():
    alphabet_string = string.ascii_lowercase
    alphabet_array = list(alphabet_string)
    alphabet_array.extend([' '])
    alphabet_array.extend(['%'])
    return alphabet_array


def matrix_mapper(input_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        alphabet_array = get_alphabet_array()
        for line in f:
            if len(line) > 1:
                line = line.strip()
                line = ''.join([i for i in line if not i.isdigit()])
                for index, letter in enumerate(line):
                    sentence_length = len(line)
                    if index < sentence_length - 1:
                        letter = letter.lower()
                        if letter not in alphabet_array:
                            letter = '%'
                        letter_next = line[index + 1].lower()
                        if letter_next not in alphabet_array:
                            letter_next = '%'
                        yield f'{letter}{letter_next}', 1


def matrix_reducer(mapper_count):
    dict = {}
    for key, value in mapper_count:
        if key not in dict:
            dict[key] = value
        else:
            dict[key] += value
    return dict


def matrix_probability_mapper_total(matrix_count):
    for key in matrix_count:
        yield key, matrix_count[key]


def matrix_probability_reducer_total(mapper_total):
    dict = {}
    for key, value in mapper_total:
        first_letter = key[0]
        if first_letter not in dict:
            dict[first_letter] = value
        else:
            dict[first_letter] += value
    return dict


def matrix_probability_mapper(matrix_count, matrix_total):
    for key in matrix_count:
        yield key, matrix_count[key] / matrix_total[key[0]]


def matrix_probability_reducer(mapper_probability):
    dict = {}
    for key, value in mapper_probability:
        if key not in dict:
            dict[key] = value
    return dict


def get_language_from_sentence(matrix_nl, matrix_en, value):
    dutch_probability = matrix_nl[value] if value in matrix_nl else 0
    english_matrix = matrix_en[value] if value in matrix_en else 0
    if dutch_probability > english_matrix:
        return "dutch"
    else:
        return "english"


def language_mapper_per_sentence(input_file_path, matrix_nl, matrix_en):
    with open(input_file_path, 'r', encoding='utf-8') as f:
        alphabet_array = get_alphabet_array()
        for line in f:
            if len(line) > 1:
                line = line.strip()
                line = ''.join([i for i in line if not i.isdigit()])
                for index, letter in enumerate(line):
                    sentence_length = len(line)
                    if index < sentence_length - 1:
                        letter = letter.lower()
                        if letter not in alphabet_array:
                            letter = '%'
                        letter_next = line[index + 1].lower()
                        if letter_next not in alphabet_array:
                            letter_next = '%'
                        value = get_language_from_sentence(matrix_nl, matrix_en, f'{letter}{letter_next}')
                        yield line, value


def language_reducer_per_sentence(mapper_language):
    dict = {}
    for key, value in mapper_language:
        if key not in dict:
            dict[key] = {"english": 0,
                         "dutch": 0}
            dict[key][value] = 1
        else:
            dict[key][value] += 1
    return dict


def language_mapper(sentence_counts):
    for key in sentence_counts.keys():
        if sentence_counts[key]["english"] > sentence_counts[key]["dutch"]:
            yield "english", 1
        else:
            yield "dutch", 1


def language_reducer(mapper_language):
    dict = {}
    for key, value in mapper_language:
        if key not in dict:
            dict[key] = value
        else:
            dict[key] += 1
    return dict


if __name__ == "__main__":
    train_path_dutch = sys.argv[1]
    train_path_english = sys.argv[2]
    test_path = sys.argv[3]

    # Map Reduce Dutch Matrix
    mapper_count_nl = matrix_mapper(train_path_dutch)
    initial_matrix_nl = matrix_reducer(mapper_count_nl)
    mapper_total_nl = matrix_probability_mapper_total(initial_matrix_nl)
    total_matrix_nl = matrix_probability_reducer_total(mapper_total_nl)
    mapper_probability_nl = matrix_probability_mapper(initial_matrix_nl, total_matrix_nl)
    matrix_probabilities_nl = matrix_probability_reducer(mapper_probability_nl)

    # Map Reduce English Matrix
    mapper_count_en = matrix_mapper(train_path_english)
    initial_matrix_en = matrix_reducer(mapper_count_en)
    mapper_total_en = matrix_probability_mapper_total(initial_matrix_en)
    total_matrix_en = matrix_probability_reducer_total(mapper_total_en)
    mapper_probability_en = matrix_probability_mapper(initial_matrix_en, total_matrix_en)
    matrix_probabilities_en = matrix_probability_reducer(mapper_probability_en)

    # Map Reduce Language Counts
    mapper_language_per_sentence = language_mapper_per_sentence(test_path, matrix_probabilities_nl,
                                                                matrix_probabilities_en)
    counts_per_sentence = language_reducer_per_sentence(mapper_language_per_sentence)
    mapper_language_total = language_mapper(counts_per_sentence)
    counts_per_language = language_reducer(mapper_language_total)
    print(counts_per_language)


    
    

