from create_matrix_algorithm import get_alphabet_listed_with_white_space


#  return probability of a sentence
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


#  get probability of English or Dutch sentence and return highest probability
def get_language_from_sentence(dutch_matrix, english_matrix, sentence):
    dutch_probability = get_probability_from_matrix(dutch_matrix, sentence)
    english_probability = get_probability_from_matrix(english_matrix, sentence)
    if dutch_probability > english_probability:
        return "dutch", 1
    else:
        return "english", 1


#  return amount of English and Dutch sentences in a file
def get_language_counts(sc, dutch_matrix, english_matrix):
    mixed_sentences = sc.textFile("mixed_sentences.txt")
    return mixed_sentences.map(lambda sentence: get_language_from_sentence(dutch_matrix, english_matrix, sentence)) \
        .reduceByKey(lambda a, b: a + b)



