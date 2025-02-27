import gensim.downloader as api
import re

class AI:
    def __init__(self):
        """Initialize the AI class with pre-trained GloVe models."""

        print("Loading GloVe Wikipedia (300D) model ~1.6 GB - Average ETA: 45s")
        self.glove_wiki_300 = api.load('glove-wiki-gigaword-300')
        print("GloVe Wikipedia (300D) model loaded successfully.")
        self.database_path_file = "C:\\Temp\\ContextoSolver\\database.txt"

    def return_all_words_from_database_no_duplicates_alphabetically(self):
        """
        Return all unique words from the database file, sorted alphabetically as a list.
        """
        # Initialize a set for unique words
        unique_words = set()

        # Regular expression to match words (letters only, no numbers or special characters)
        word_pattern = re.compile(r'\b[a-zA-Z]+\b')

        try:
            # Open and read the file
            with open(self.database_path_file, 'r', encoding='utf-8') as file:
                for line in file:
                    # Find all words in the current line
                    words = word_pattern.findall(line)
                    for word in words:
                        # Convert word to lowercase for case-insensitivity
                        unique_words.add(word.lower())

            # Sort the unique words alphabetically
            sorted_words = sorted(unique_words)

            # Return the sorted list of words
            return sorted_words

        except FileNotFoundError:
            print(f"Error: The file '{self.database_path_file}' was not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None



    def get_similar_words(self, word, topn=10):
        """Return a list of similar words to the input word using the GloVe Wikipedia (300D) model."""

        if word in self.glove_wiki_300:
            # Retrieve the `topn` most similar words to the input word
            similar_words = self.glove_wiki_300.most_similar(word, topn=topn)

            # Extract only the words from the tuples returned by `most_similar` (ignoring similarity scores)
            similar_words_list = [word for word, _ in similar_words]

            # Return the list of similar words
            return similar_words_list
        else:
            # If the input word is not found in the vocabulary, print an error message
            print(f"'{word}' not found in the GloVe Wikipedia (300D) vocabulary.")

            # Return an empty list since no similar words can be found
            return []

