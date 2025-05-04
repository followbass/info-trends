from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)

# إعداد pytrends لدعم العربية
pytrends = TrendReq(hl='ar-EG', tz=360)

@app.route('/')
def home():
    return 'API جاهز. استخدم /trends?query=كلمتك'

@app.route('/trends')
def get_trends():
    try:
        query = request.args.get('query', '').encode('utf-8').decode('utf-8').strip()
        print("Query Received:", query)

        if not query:
            return jsonify({'error': 'يرجى إدخال كلمة مفتاحية'}), 400

        pytrends.build_payload([query], cat=0, timeframe='now 7-d', geo='', gprop='')
        related_queries = pytrends.related_queries()[query]['top']

        if related_queries is None or related_queries.empty:
            return jsonify({'keywords': [], 'message': 'لا توجد نتائج لهذه الكلمة حالياً.'})

        keywords = related_queries['query'].tolist()
        return jsonify({'keywords': keywords})

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
