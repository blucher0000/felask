from flask import Flask, render_template
from markupsafe import escape
from faker import Faker
from datetime import datetime
from pprint import pprint
from paddlenlp import Taskflow
import json
from flask import request, url_for, redirect, flash
#明光桥位于洪湖市小港管理区，中心桩号为k1+044，是一座空腹圬工拱，桥梁全长为16m，桥跨组合为1*6m，桥梁全宽为5.5m，桥宽组合为1m（护栏）+3.5m（行车道）+1m（护栏）。上部结构为空腹圬工拱，支座状态为未设置支座。下部结构为砖砌混凝土重力式桥台。桥面铺装采用乐高积木铺装，两侧设有砖砌混凝土护栏，未设置伸缩缝。该桥始建于1981，设计荷载为挂车-100级。桥梁正面照、立面照见图1.1-1、图1.1-2。
f=Faker(locale='zh_CN')
currentDateAndTime = datetime.now()
name = '喵喵喵' + f.ssn()
time = currentDateAndTime
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies,time=time) 

@app.route('/hi')
@app.route('/home')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/user', defaults={'name': 'defaults'})
@app.route('/user/<name>')
def user_page(name):
    print('User:'+ name)
    return f'User: {escape(name)}'


@app.route('/ie')
def myie():
    text_str = request.args.get('s')
    schema = ["桥梁名称",'位置市','位置镇', '中心桩号','全长', '桥跨组合', '桥梁全宽',"上部结构","下部结构","桥面铺装采用","桥宽组合","始建时间","设计荷载"] # Define the schema for entity extraction
    ie = Taskflow('information_extraction', schema=schema,batch_size=16, model='uie-base',position_prob=0.5)
    pprint(ie(text_str))
    #j = json.dumps(ie(text_str))
    return ie(text_str)

@app.route('/bie', methods=['GET', 'POST'])
def mybie():
    if request.method == 'POST':
        mystring = request.form.get('mystring')  # 传入表单对应输入字段的 name 值
        myschema = request.form.get('myschema')
        myschema = myschema.split()
        ie = Taskflow('information_extraction', schema=myschema,batch_size=16, model='uie-base',position_prob=0.5)
        j = json.dumps(ie(mystring)[0],ensure_ascii=False)
        return render_template('bie.html',result =j)
    return render_template('bie.html', result=" ")

@app.route('/biet')
def mybiet():
    return render_template('biet.html')

@app.route('/bietd', methods=['POST'])
def mybietd():
    json_v = request.json
    print(type(json_v))
    print('recv:', json_v)
    mystring = json_v['binfo']
    myschema = json_v['schema']
    myschema = myschema.split()
    ie = Taskflow('information_extraction', schema=myschema,batch_size=16, model='uie-base',position_prob=0.5)
    result = json.dumps(ie(mystring)[0],ensure_ascii=False)
    print('return:', result)
    return result

@app.route('/biee')
def biee():
    return render_template('biee.html')

@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请访问 http://127.0.0.1:5000/test 后在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 生成 hello 视图函数对应的 URL，将会输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'

