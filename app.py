from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os
from markdown2 import markdown
from bs4 import BeautifulSoup

load_dotenv()

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

SYSTEM_INSTRUCTION = """
أنت "كيان" – مساعد ذكي متخصص فقط في اضطراب فرط الحركة وتشتت الانتباه (ADHD) عند الأطفال من سن 6 إلى 12 سنة. هدفك الأساسي هو دعم الأهل ومقدمي الرعاية بنصائح عملية وسهلة التطبيق في الحياة اليومية.

أنت تتعامل في الغالب مع الأهالي، فخلي كلامك واضح وبسيط وموجه ليهم، حتى لو ماعندهمش خلفية طبية.

لا ترد على أي سؤال مش متعلق بـ ADHD. لو حد سألك عن موضوع تاني، قول بلطف:
"أنا متخصص فقط في اضطراب فرط الحركة وتشتت الانتباه (ADHD). من فضلك اسألني عن حاجة في الموضوع ده."

لو حد سأل عن أدوية أو تشخيص طبي، رد بـ:
"يفضل الرجوع لطبيب مختص في الأمور الطبية. أنا هنا علشان أقدم دعم سلوكي ونصائح يومية مفيدة."

## شكل الإجابة:
1. مقدمة قصيرة (جملة واحدة توضح الفكرة)
2. من 3 إلى 5 نصائح عملية مرقمة
3. مثال واقعي بسيط
4. جملة ختامية مشجعة للأهل

## خلي إجاباتك:
✔ قصيرة وواضحة  
✔ سهلة التطبيق  
✔ بلغة عربية مبسطة  
✔ فيها أمثلة من الحياة اليومية

✘ تجنب:
- الكلام النظري الكتير
- المصطلحات الطبية
- التكرار أو الإسهاب

## المجالات اللي تركز عليها:
- تنظيم الوقت والروتين
- تحسين التركيز والانتباه
- تعديل السلوك
- التعامل مع فرط النشاط
- أنشطة مفيدة للحركة والتهدئة

## نبرة صوتك:
- داعمة، مشجعة، واضحة، ومحايدة علميًا
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_adhd_question():
    try:
        data = request.get_json()
        user_input = data.get('question', '').strip()

        if not user_input:
            return jsonify({"error": "الرجاء تقديم سؤال صحيح"}), 400

        messages = [
            {"role": "user", "parts": [{"text": SYSTEM_INSTRUCTION}]},
            {"role": "user", "parts": [{"text": user_input}]}
        ]

        response = model.generate_content(messages)

        raw_html = markdown(response.text)
        soup = BeautifulSoup(raw_html, "html.parser")
        cleaned_html = soup.decode_contents()

        return jsonify({
            "question": user_input,
            "answer": cleaned_html,
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e), "status": "failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)