from flask import Flask, render_template, request, redirect, url_for, session
import config_user
from models import User, Translator, Article, Result
from exts import db

app = Flask(__name__)
app.config.from_object(config_user)
db.init_app(app)


@app.route('/none/')
def index():
    return render_template("index.html")

@app.route('/translator_knows/')
def translator_knows():
    return render_template("translator_knows.html")

@app.route('/user_logout/')
def user_logout():
    session.clear()
    return redirect(url_for('user_login'))

@app.route('/translator_logout/')
def translator_logout():
    session.clear()
    return redirect(url_for('translator_login'))

@app.route('/admin_logout/')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/user_login/',methods=['GET','POST'])
def user_login():
    if request.method == 'GET':
        return render_template("user_login.html")
    else:
        emil = request.form.get('emil')
        password = request.form.get('password')
        user = User.query.filter(User.emil == emil,User.password ==password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('user'))
        else:
            tip = '用户名或密码错误'
            return render_template("user_login.html",tip = tip)

@app.route('/',methods=['GET','POST'])
def translator_login():
    if request.method == 'GET':
        return render_template("translator_login.html")
    else:
        emil = request.form.get('emil')
        password = request.form.get('password')
        translator = Translator.query.filter(Translator.emil == emil, Translator.password == password).first()
        if translator:
            session['translator_id'] = translator.id
            return redirect(url_for('translator'))
        else:
            tip = '用户名或密码错误'
            return render_template("translator_login.html", tip=tip)

@app.route('/user_regist/',methods=['GET','POST'])
def user_regist():
    if request.method == 'GET':
        return render_template("user_regist.html")
    else:
        emil = request.form.get('emil')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.emil == emil).first()
        if user:
            tip = '该用户已注册！'
            return render_template("user_regist.html",tip = tip)
        else:
            if password1 != password2:
                tip = '两次密码不一致，请重新输入！'
                return render_template("user_regist.html", tip=tip)
            else:
                user = User(emil = emil,username = username,password = password2)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('user_login'))

@app.route('/translator_regist/',methods=['GET','POST'])
def translator_regist():
    if request.method == 'GET':
        return render_template("translator_regist.html")
    else:
        emil = request.form.get('emil')
        translatorname = request.form.get('translatorname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        translator = Translator.query.filter(Translator.emil == emil).first()
        if translator:
            tip = '该用户已注册！'
            return render_template("translator_regist.html", tip=tip)
        else:
            if password1 != password2:
                tip = '两次密码不一致，请重新输入！'
                return render_template("translator_regist.html", tip=tip)
            else:
                translator = Translator(emil=emil, translatorname=translatorname, password=password2,money = 0,right = 0,right_time = 0,all_time = 0)
                db.session.add(translator)
                db.session.commit()
                return redirect(url_for('translator_login'))

@app.route('/admin/')
def admin():
    admin_name = session.get('admin_name')
    if admin_name:
        context = {
            'articles':Article.query.filter(Article.re_translated == None,Article.translated != None).all()
        }
        return render_template("admin_page.html",**context)
    else:
        return redirect(url_for('admin_login'))

@app.route('/user_article/',methods=['GET','POST'])
def admin_article():
    if request.method == 'GET':
        return render_template('admin_article.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        money = request.form.get('money')
        contents = content.splitlines()
        # price = float(money) / float(len(contents))
        i = 0
        q = 1
        while i < len(contents):
            p = int(len(contents[i]))/int(len(content))
            t_price = float(money)*p
            price = "%.2f"%t_price
            article = Article(title = title,content = contents[i],paragraph_name = q,price = price)
            db.session.add(article)
            db.session.commit()
            i = i+1
            q = q+1
        return redirect(url_for('user'))

@app.route('/admin_login/',methods=['GET','POST'])
def admin_login():
    if request.method =="GET":
        return render_template("admin_login.html")
    else:
        emil = request.form.get('emil')
        password = request.form.get('password')
        if emil =='admin' and password == '123456':
            admin_name = 'admin'
            session['admin_name'] = admin_name
            return redirect(url_for('admin'))
        else:
            tip = '用户名或密码错误'
            return render_template("admin_login.html",tip = tip)

@app.context_processor
def my_context_processor():
    translator_id = session.get('translator_id')
    user_id = session.get('user_id')
    if translator_id:
        translator = Translator.query.filter(Translator.id == translator_id).first()
        if translator:
            return {'translator':translator}
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

@app.route('/user/')
def user():
    user_id = session.get('user_id')
    if user_id:
        context = {
            'articles': Result.query.all()
        }
        return render_template("user_page.html",**context)
    else:
        return redirect(url_for('user_login'))

@app.route('/translator_center/')
def translator_center():
    translator_id = session.get('translator_id')
    massage = Translator.query.filter(Translator.id == translator_id).first()
    return render_template("translator_center.html",massage = massage)

@app.route('/center_get/',methods=['POST'])
def center_get():
    pay = request.form.get('pay')
    id = request.form.get('id')
    translator = Translator.query.filter(Translator.id == id).first()
    translator.pay = pay
    db.session.commit()
    return redirect(url_for("translator"))

@app.route('/translator/')
def translator():
    translator_id = session.get('translator_id')
    if translator_id:
        context = {
            'articles':Article.query.filter(Article.translated == None).all()
        }
        return render_template("translator_page.html",**context)
    else:
        return redirect(url_for('translator_login'))

@app.route('/translator_detil/<article_id>/')
def translator_detil(article_id):
    article = Article.query.filter(Article.id == article_id).first()
    return render_template('translator_detil.html',article = article)

@app.route('/user_detil/<article_title>/')
def user_detil(article_title):
    context = {
        'articles':Article.query.filter(Article.title == article_title).all()
    }
    title = Result.query.filter(Result.title == article_title).first()
    return render_template('user_detil.html',**context,title = title)

@app.route('/admin_detil/<article_id>/')
def admin_detil(article_id):
    article = Article.query.filter(Article.id == article_id).first()
    return render_template('admin_detil.html',article = article)

@app.route('/show_translator/')
def show_translator():
    context = {
        'persons':Translator.query.all()
    }
    return render_template("show_translator.html",**context)

@app.route('/delet_t/',methods=['POST'])
def delet():
    id = request.form.get('id')
    person = Translator.query.filter(Translator.id == id).first()
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('show_translator'))

@app.route('/clear/',methods=['POST'])
def clear():
    clear = request.form.get('clear')
    person = Translator.query.filter(Translator.id == clear).first()
    person.money = 0
    db.session.commit()
    return redirect(url_for('show_translator'))

@app.route('/get_translated',methods=['POST'])
def get_translated():
    content = request.form.get('content')
    id = request.form.get('id')
    translator = session.get('translator_id')
    man = Translator.query.filter(Translator.id == translator).first()
    translated = Article.query.filter(Article.id == id).first()
    if translated.translated:
        return u'该段落已被翻译，请重新选择段落翻译'
    else:
        man.all_time = man.all_time + 1
        translated.person = translator
        translated.translated = content
        db.session.commit()
        return redirect(url_for('translator'))

@app.route('/get_re_translated',methods=['POST'])
def get_re_translated():
    content = request.form.get('content')
    id = request.form.get('id')
    right = request.form.get('right')
    translated = Article.query.filter(Article.id == id).first()
    person = Translator.query.filter(Translator.id == translated.person).first()
    if right =='on':
        person.money = person.money + translated.price
        person.right_time = person.right_time + 1
        person.right = person.right_time/person.all_time
        translated.re_translated = content
        db.session.commit()
    else:
        translated.translated = None
        person.right = person.right_time / person.all_time
        db.session.commit()
    title = request.form.get('title')
    re_translated = Article.query.filter(Article.title == title).all()
    i = 0
    v = True
    while i < len(re_translated):
        if re_translated[i].re_translated == None:
            v = False
            break
        else:
            v = True
        i = i + 1
    if v == True:
        q = 0
        result = ''
        contents = ''
        while q < len(re_translated):
            contents = contents + re_translated[q].content
            # result = result + re_translated[q].re_translated
            q = q+1
        M = Result(title=title)
        db.session.add(M)
        db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run()