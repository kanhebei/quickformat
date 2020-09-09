from flask import Flask, render_template, jsonify, request
from bs4 import BeautifulSoup


app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/format', methods=['POST'])
def quick_format():
    doc = request.json.get('content')
    rule = request.json.get('rule')
    
    # 清洗数据
    doc = doc.replace('&nbsp;', '').replace('<p></p>', '').strip().replace(u'<p>\u3000\u3000', '<p>')

    soup = BeautifulSoup(doc, 'html.parser')
    
    # 过滤锚文本
    if 'clear_a' in rule:
        for a in soup.find_all('a'):
            a.unwrap()

    for p in soup.find_all('p'):
        # 图片居中
        if 'image' in rule and p.img:
            p['style'] = "text-align:center"

        # 首行空两格 中文空格
        if 'space' in rule and not p.img:
            p.insert(0, u'\u3000\u3000')
            
    return jsonify({
        'content': str(soup)
    })

