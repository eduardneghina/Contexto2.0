import time
from WebController import *
import gensim.downloader as api
import random
import re

# Load the GloVe models
print("Loading GloVe models...")
glove_wiki_300 = api.load('glove-wiki-gigaword-300')  # Wikipedia + Gigaword, 300 dimensions
glove_twitter_200 = api.load('glove-twitter-200')     # Twitter, 200 dimensions
print("GloVe models loaded.")

# Define the target word
target_word = "mango"

# Number of top matches to retrieve
top_n = 10

# Function to get and display similar words
def get_similar_words(model, model_name, target_word, top_n):
    try:
        # Get the top N most similar words
        similar_words = model.most_similar(target_word, topn=top_n)
        # Extract the words (ignore the similarity scores for simplicity)
        related_words = [word for word, _ in similar_words]
        # Display the results
        print(f"Words related to '{target_word}' using {model_name}:")
        print(", ".join(related_words))
    except KeyError:
        print(f"Word '{target_word}' not found in the vocabulary of {model_name}.")

# Compare outputs from both models
get_similar_words(glove_wiki_300, "glove-wiki-gigaword-300", target_word, top_n)
print()  # Add a blank line for readability
get_similar_words(glove_twitter_200, "glove-twitter-200", target_word, top_n)

#pineapple, guava, papaya, pear, coconut, plum, pomegranate, avocado, peach, apricot for 50
#papaya, pineapple, guava, avocado, coconut, pear, apricot, peach, tomato, citrus - for 100
