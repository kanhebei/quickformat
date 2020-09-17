from flask import Flask, render_template, jsonify, request
from bs4 import BeautifulSoup
import re


app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/format', methods=['POST'])
def quick_format():
    content = request.json.get('content').strip()
    rule = request.json.get('rule')
    soup = BeautifulSoup(content, 'html.parser')    
    
    # 过滤锚文本
    if 'clear_a' in rule:
        for a in soup.find_all('a'):
            a.unwrap()

    for img in soup.find_all('img'):
        del(img['style'])
        del(img['border'])
        del(img['class'])
        
         # 图片居中
        if 'image' in rule:
            if img.parent.name != 'center':
                img.parent.name = 'center'
        
    for center in soup.find_all('center'):
        del(center['style'])
        del(center['class'])
    for strong in soup.find_all('strong'):
        del(strong['style'])
        del(strong['class'])                
    for p in soup.find_all('p'):
        del(p['style'])
        del(p['class'])
        
    # 去除 P 开头的中文空白
    doc = re.sub('<p>(\u3000)*', '<p>', str(soup))
    # 去除strong 开头的中文空白
    doc = re.sub('<strong>(\u3000)*', '<strong>', doc)
    doc = doc.replace('<br>', '')
    doc = doc.replace('<br/>', '')
    doc = doc.replace('<br />', '')
    doc = doc.replace('&nbsp;', '')
    doc = doc.replace('<p></p>', '')
    
    # 首行空两格 中文空格
    if 'space' in rule and not p.img:
        doc = doc.replace('<p>', u'<p>\u3000\u3000')

    return jsonify({
        'content': doc
    })

