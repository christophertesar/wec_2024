import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance # function used to measure similarity between sentences
import numpy as np #numpy
import networkx as nx #networkx
import scipy

nltk.download('stopwords') # for specifying language stopwords, will use english

# Function to read input text file
def read_file(file_name):

    sentences = []
    
    with open(file_name, 'r') as file:
        for line in file:
            # Split the line into sentences based on the period followed by a space
            split_data = line.split('. ')
            for sentence in split_data:
                # Replace characters in the specified range and split the sentence into words
                words = sentence.replace('[a^zA-Z]', ' ').split(' ')
                sentences.append(words)
    sentences.pop()    

    return sentences



# Function to calculate the similarity between two input strings
def similarities(input_str1, input_str2, stopwords=None):

    if stopwords is None:
        stopwords = []
    
    # Convert input strings to lowercase and tokenize them into lists of words
    sentence1 = [word.lower() for word in input_str1] 
    sentence2 = [word.lower() for word in input_str2]
    
    # Combine words from both sentences and create a list of unique words
    total_words = list(set(sentence1 + sentence2))
    
    # Initialize two vectors with zeros for word counts
    input1 = [0] * len(total_words)
    input2 = input1  # Reference to the same list, not a copy

    # Count occurrences of each word in sentence1, excluding stopwords
    for word in sentence1:
        if word in stopwords:
            continue
        input1[total_words.index(word)] += 1
    
    # Count occurrences of each word in sentence2, excluding stopwords
    for word in sentence2:
        if word in stopwords:
            continue
        input2[total_words.index(word)] += 1
    
    # Calculate cosine distance between the two vectors and return similarity
    similarity = 1 - cosine_distance(input1, input2)

    return similarity



# Function to generate a similarity matrix based on input strings and language
def gen_matrix(input_str, language):
    # Get the length of input strings
    length_of_sentences = len(input_str)
    
    # Initialize a matrix filled with zeros
    matrix = np.zeros((length_of_sentences, length_of_sentences))
    
    # Iterate over pairs of sentences to calculate similarities
    for sentence_pos1 in range(length_of_sentences):
        for sentence_pos2 in range(length_of_sentences):
            if sentence_pos1 == sentence_pos2:
                continue
            # Calculate similarity between pairs of sentences
            matrix[sentence_pos1][sentence_pos2] = similarities(input_str[sentence_pos1], input_str[sentence_pos2], language)
    
    return matrix



# Function to generate a summary based on a text file input
def gen_summary(file_name, max_lines=5):

    # Get the list of English stopwords
    language = stopwords.words('english')
    
    summarized = []
    sentences = read_file(file_name)
    
    # Generate a similarity matrix based on the sentence in text file and language
    matrix = gen_matrix(sentences, language)
    graph = nx.from_numpy_array(matrix)
    
    # Rank the sentences using networkx page rank algorithm
    ranking = nx.pagerank(graph)
    sort_ranking = sorted(((ranking[pos], str) for pos, str in enumerate(sentences)), reverse=True)
    
    # Iterate over top ranked sentences and append them to the summarized list
    for line in range(max_lines):
        # Use strip() method to remove leading and trailing whitespace, including newline characters
        summarized.append(' '.join(sort_ranking[line][1]).strip())
    
    # Print the summarized sentences
    summary_text = "Summary \n\n", " ".join(summarized)

    # Construct the output file name by removing the extension from the input file name and appending "_summarized.txt"
    output_text_file = file_name.split('.')[0] + "_summarized.txt"
    
    # Save the summarized text to the text file
    with open(output_text_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(summary_text))
    
    print("Summary saved to", output_text_file)
