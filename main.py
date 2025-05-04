from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import pandas as pd
import os

app = Flask(__name__)
pytrends = TrendReq(hl='en-US', tz=360)

@app.route('/')
def home():
    return jsonify({
        "message": "أهلاً بك في خدمة Google Trends API المصغرة!",
        "طريقة الاستخدام": "/trends?query=كلمة_البحث"
    })

@app.route('/trends')
def get_trends():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'يرجى تحديد الكلمة باستخدام ?query=keyword'}), 400

    try:
        pytrends.build_payload([query], cat=0, timeframe='now 7-d', geo='', gprop='')
        related_queries = pytrends.related_queries()[query]['top']

        if related_queries is None:
            return jsonify({'message': 'لا توجد بيانات كافية لهذه الكلمة الآن.'})

        keywords = related_queries['query'].tolist()
        return jsonify({'keywords': keywords})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
