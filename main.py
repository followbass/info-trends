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

        print("Step 1: Building payload for", query)
        pytrends.build_payload([query], cat=0, timeframe='now 7-d', geo='', gprop='')

        print("Step 2: Getting related queries")
        related = pytrends.related_queries()
        print("Step 3: Raw related data:", related)

        # تحقق من أن البيانات موجودة وسليمة
        if not related or query not in related or related[query]['top'] is None:
            return jsonify({'keywords': [], 'message': 'لا توجد نتائج حالياً.'})

        related_queries = related[query]['top']
        print("Step 4: Extracted top:", related_queries)

        # تحويل الكلمات المفتاحية إلى قائمة
        keywords = related_queries['query'].tolist()
        return jsonify({'keywords': keywords})

    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
