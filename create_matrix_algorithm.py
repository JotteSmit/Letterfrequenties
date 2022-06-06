import string


#  create a list that contains all letters in the alphabet and a whitespace
def get_alphabet_listed_with_white_space():
    alphabet_string = string.ascii_lowercase
    alphabet_list = list(alphabet_string)
    alphabet_list.extend([' '])
    return alphabet_list


#  create a 2D matrix from the alphabet list letters
def create_matrix():
    alphabet_listed_with_white_space = get_alphabet_listed_with_white_space()
    alphabet_listed_with_white_space.extend(['%'])
    matrix = {key: {key: 0 for key in alphabet_listed_with_white_space} for key in alphabet_listed_with_white_space}
    return matrix


#  create a list of bigrams
def get_sequence(sentence):
    sequence_list = []
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
            sequence_list.append((f"{letter}{next_letter}", 1))
    return sequence_list


#  update the matrix with the next sequence
def update_matrix(matrix, sequence):
    matrix[sequence[0][0]][sequence[0][1]] = sequence[1]
    return matrix


#  change numeric values in matrix to probabilities
def set_probabilities_of_matrix(matrix):
    for letter_from in matrix:
        count = 0
        for letter_to in matrix[letter_from]:
            count += matrix[letter_from][letter_to]
        for letter_to in matrix[letter_from]:
            if matrix[letter_from][letter_to] > 0:
                matrix[letter_from][letter_to] = matrix[letter_from][letter_to] / float(count)
    return matrix


#  creates matrix based on a text file (in this case English or Dutch)
#  maps bigram key value pairs and reduces them and then maps the bigrams in the matrix
#  returns matrix with bigram probabilities
def create_language_matrix(sc, filename):
    matrix = create_matrix()

    word_sequence_file = sc.textFile(filename)
    matrix_count = word_sequence_file.flatMap(lambda sentence: get_sequence(sentence)) \
        .reduceByKey(lambda a, b: a + b) \
        .map(lambda sequence: update_matrix(matrix, sequence)).collect()[-1]

    return set_probabilities_of_matrix(matrix_count)
