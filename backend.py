from flask import Flask, request
import logging
from flask_cors import CORS
import re
from hmm_pos_tagger import HMMPosTagger
import pickle

app = Flask(__name__)
CORS(app)

with open('hmm_tagger.pkl', 'rb') as file:
    hmm_tagger = pickle.load(file)

with open('naive_tagger.pkl', 'rb') as file:
    naive_tagger = pickle.load(file)

# Configure logging
logging.basicConfig(level=logging.INFO)

def split_into_sentences(text):
    # Split the text into sentences using punctuation symbols as delimiters
    sentences = re.split(r'[.!?]', text)
    
    # Remove empty sentences
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    result = []
    
    for sentence in sentences:
        # Split each sentence into words and special symbols
        words_and_symbols = re.findall(r'\b\w+\b|[^\w\s]', sentence)
        
        # Filter out empty items
        words_and_symbols = [item for item in words_and_symbols if item.strip()]
        
        result.append(words_and_symbols)
    
    return result

@app.route('/tag', methods=['POST'])
def tag_endpoint():
    try:
        data = request.get_json()
        message = data.get('message', '')

        # naive or hmm
        tagger = data.get("tagger", "naive")

        # Log the received message
        logging.info(f"Received message: {message}, tagging with {tagger}")

        sentences = split_into_sentences(message)

        if tagger == "naive":
            tagged = naive_tagger.tag(sentences)
        elif tagger == "hmm":
            tagged = hmm_tagger.tag(sentences)
        else:
            raise Exception("tagger not found")

        return {'tagged': tagged, "tagged_with": tagger}, 200

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    app.run(debug=True)
