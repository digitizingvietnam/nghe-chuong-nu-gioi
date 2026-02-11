"""
main.py

Flask API server for the Retrieval-Augmented Generation (RAG) system.

This module exposes HTTP endpoints that allow clients to:
- Submit natural language queries to the RAG pipeline
- Retrieve generated responses based on vector search
- Perform health checks for deployment monitoring
- Fetch sample historical text for frontend display or animation

The API delegates all retrieval and generation logic to the
`query_rag` utility function to ensure separation of concerns
between application logic and RAG implementation.
"""

from flask import Flask, jsonify, request, render_template, session
import pandas as pd
import os

from utils.rag import query_rag

app = Flask(__name__)
app.secret_key = '123456'


@app.route('/')
def index():
    session.clear()
    return render_template('index.html')


@app.route('/api/query', methods=['POST'])
def api_query():
    data = request.get_json(silent=True)

    if not data or "query_text" not in data:
        return jsonify({
            "error": "Missing 'query_text' in request body"
        }), 400

    query_text = data["query_text"]

    response_text = query_rag(query_text)

    return jsonify({"response": response_text})


# check server health
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Server is running fine!",
    }), 200


# read the file for animation purpose
@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    try:
        df = pd.read_csv('data/Nữ Giới Chung_Datasheet - Sheet1.csv')

        if 'Nội dung' in df.columns:
            contents = df['Nội dung'].dropna().tolist()
        else:
            contents = df.iloc[:, -1].dropna().tolist()

        contents = [
            c.replace("\\n", " ").replace("\n", " ").strip()
            for c in contents
        ]

        return jsonify(contents[:10])

    except Exception as e:
        print("Error reading CSV:", e)
        return jsonify([])


# deploy
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7070))
    app.run(host="0.0.0.0", port=port)
