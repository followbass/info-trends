from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)
pytrends = TrendReq(hl='ar', tz=360)

@app.route('/')
def index():
    return "API شغالة. استخدم /trends?query=كلمة"

@app.route('/trends')
def trends():
    query = request.args.get('query', '').strip()

    if not query:
        return jsonify({'error': 'يرجى إدخال كلمة مفتاحية'}), 400

    try:
        # تجهيز البيانات
        pytrends.build_payload([query], cat=0, timeframe='now 7-d', geo='', gprop='')
        related = pytrends.related_queries()

        # التحقق من وجود نتائج
        if not related or query not in related:
            return jsonify({'keywords': [], 'message': 'لا توجد نتائج.'})

        result = related[query]

        # محاولة جلب "top" ثم "rising"
        df = result.get('top') or result.get('rising')

        if df is None or df.empty:
            return jsonify({'keywords': [], 'message': 'لا توجد نتائج حالياً.'})

        keywords = df['query'].tolist()
        return jsonify({'keywords': keywords})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
