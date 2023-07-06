from flask import Flask, request, render_template
import math
from collections import Counter, defaultdict
import time
import heapq
import re

app = Flask(__name__)

def preprocess_text(text):
    # Tokenization and preprocessing steps
    tokens = re.findall(r'\b\w+\b', text.lower())  # Basic word tokenization
    # Apply additional preprocessing steps if needed, such as stop word removal, stemming, etc.
    return tokens

def compute_query_vector(query_tokens, inverted_index):
    query_tf = Counter(query_tokens)
    query_vector = {}
    query_length = 0.0
    for token, tf in query_tf.items():
        df = len(inverted_index.get(token, []))
        if df > 0:
            tf_idf = (1 + math.log(tf)) * math.log(len(inverted_index) / df)
        else:
            tf_idf = 0
        query_vector[token] = tf_idf
        query_length += tf_idf * tf_idf
    query_length = math.sqrt(query_length)
    return query_vector, query_length

# Change the inverted index data structure
# The key will be the token, the value will be a list of tuples, where each tuple contains a doc_id and the tf-idf score of that document for the token

def compute_document_scores(query_vector, query_length, inverted_index):
    document_scores = defaultdict(float)
    for token, query_tf_idf in query_vector.items():
        for doc_id, doc_tf_idf in inverted_index.get(token, []):
            document_scores[doc_id] += query_tf_idf * doc_tf_idf

    for doc_id, score in document_scores.items():
        score /= query_length
        document_scores[doc_id] = score

    return document_scores

def search(query, inverted_index):
    query_tokens = preprocess_text(query)
    query_vector, query_length = compute_query_vector(query_tokens, inverted_index)
    document_scores = compute_document_scores(query_vector, query_length, inverted_index)
    # Use a heap to keep the top results
    top_docs = heapq.nlargest(10, document_scores.items(), key=lambda x: x[1])
    return [doc_id for doc_id, _ in top_docs]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        query = request.form['query']
        #time the search
        start_time = time.time()
        results = search(query, index)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Search execution time: {execution_time} seconds")
        return render_template('results.html', results=results, query=query)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

