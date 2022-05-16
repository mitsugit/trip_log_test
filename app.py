from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from create_map import create_map

# name__ を 入れ て おく こと で Flask 自身 が ディレクトリ の 場所 を 認識 する こと が でき ます。
app = Flask(__name__)

key = os.urandom(13)

# セッション 情報 を 暗号化 する ため に secret_ key の 設定
app.secret_key = key


# ログイン時に使用するIDとPW
ID_PW = {'FLASK': 'EXCEL'}

# sqliteの準備
URI = 'sqlite:///file.db'
app.config['SQLALCHEMY_DATABASE_URI'] = URI
# データベースの変更追跡
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ORMでDBを操作するためにクラスを継承
class Trip(db.Model):
    __tablename__ = 'trip_table'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True)
    content = db.Column(db.String(300))
    latitude = db.Column(db.String(100))
    longitude = db.Column(db.String(100))
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.now())


# DBの生成
'''
tableを初期化するために実行する関数。
ブラウザからではなくコマンドラインから入力して実行。
実行方法: flask initialize_DB
'''


@app.cli.command('initialize_DB')
def initialize_DB():
    db.create_all()


# トップ画面へのルーティング
@app.route('/')
def index():
    title = 'Trip log : 一覧画面'
    all_data = Trip.query.all()
    return render_template('index.html', title=title, all_data=all_data)


# 新規作成画面を展開
@app.route('/new')
def new():
    title = 'Trip Log ： 新規作成'
    return render_template('new.html', title=title)


# 新規データの保存
@app.route('/create', methods=['POST'])
def create():
    title = request.form['title']
    if title:
        content = request.form['content']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        register_data = Trip(
            title=title,
            content=content,
            latitude=latitude,
            longitude=longitude
        )
        db.session.add(register_data)
        db.session.commit()
        flash('登録できました')
        return redirect(url_for('index'))
    else:
        flash('作成できませんでした。入力内容を確認してください')
        return redirect(url_for('index'))


#詳細画面の展開
@app.route('/detail')
def detail():
    title = 'Trip Log ： 詳細画面'
    id = request.args.get('id')
    data = Trip.query.get(id)
    map = create_map(data.latitude, data.longitude)
    return render_template('detail.html', title=title, data=data, map=map)


#編集画面の展開
@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    title = 'Trip Log ： 編集画面'
    data = Trip.query.get(id)
    return render_template('edit.html', title=title, data=data)


#編集（更新）データの保存
@app.route('/update', methods=['POST'])
def update():
    id = request.form['id']
    edit_data = Trip.query.get(id)
    edit_data.title = request.form['title']
    edit_data.content = request.form['content']
    edit_data.latitude = request.form['latitude']
    edit_data.longitude = request.form['longitude']
    db.session.merge(edit_data)
    db.session.commit()
    flash('更新しました')
    return redirect(url_for('index'))


#データの削除
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    delete_data = Trip.query.get(id)
    db.session.delete(delete_data)
    db.session.commit()
    flash('削除しました')
    return redirect(url_for('index'))

# アプリケーションの起動
if __name__ == '__main__':
    app.run(debug=True)