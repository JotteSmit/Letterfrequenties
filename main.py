import os
import sys
from create_matrix_algorithm import create_language_matrix
from create_maximum_entropy import get_language_counts

from pyspark import SparkContext

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

if __name__ == "__main__":
    sc = SparkContext()
    english_matrix = create_language_matrix(sc, 'alice_en.txt')
    dutch_matrix = create_language_matrix(sc, 'gutenberg_nl.txt')
    language_counts = get_language_counts(sc, dutch_matrix, english_matrix).collect()
    print(language_counts)
