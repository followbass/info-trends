from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)
pytrends = TrendReq(hl='en-US', tz=360)

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
    app.run()
