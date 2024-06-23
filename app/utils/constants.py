import os


# Set up paths for entries, output, and database
INPUT_FOLDER = os.path.join('app', 'inputs', 'entries')
OUTPUT_FOLDER = os.path.join('app', 'inputs', 'processed')
DATABASE_NAME = os.path.join('app', 'storage', 'database', 'word_frequency.db')

# Define a set of common words to be ignored in word frequency analysis
COMMON_WORDS = {"a", "the", "and", "or", "but", "if", "then", "else", "when", "at", "by", "from", "of", "on", "for",
                "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below",
                "to", "from", "up", "down", "in", "out", "over", "under", "again", "further", "then", "once", "here",
                "there", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some",
                "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will",
                "just", "don", "should", "now", "th", "an", "it", "is", "that", "he", "i", "that", "this", "is", "as",
                "were", "those", "who", "were", "was", "do", "you", "your", "re", "they", "her", "rd", "st", "u", "per",
                "we", "what", "c", "am", "m", "f", "she", "nd", "q", "our"}
