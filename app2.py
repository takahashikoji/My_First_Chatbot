from flask import Flask, request, render_template, redirect ,url_for
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import Required, Length
from wtforms import Form
from unmo import Unmo
import json
import collections



passlog = []

app = Flask(__name__)

class Dialog_Form(Form):
    user = StringField('word')
    submit = SubmitField('送信')

@app.route('/study', methods=['GET', 'POST'])
def study():
    form = Dialog_Form(request.form)
    text = form.data['user']

    if not text== 'exit':
        manachan_return = chat.rulebase_func(text)
        if not 'database' in manachan_return:
            return render_template('rulebase3.html', form=form, manachan_return=manachan_return,passlog=passlog)

        if not manachan_return['database'] in passlog:
            passlog.append(manachan_return['database'])
            return render_template('rulebase2.html', form=form, manachan_return=manachan_return,passlog=passlog)
        else:
            return render_template('rulebase2.html', form=form, manachan_return=manachan_return,passlog=passlog)

    if text== 'exit':
        manachan_return = chat.main_func(text)
        return render_template('index3.html',form=form,manachan_return=manachan_return)



@app.route('/dialog', methods=['GET', 'POST'])
def index():
    form = Dialog_Form(request.form)
    if request.method == 'POST':
        text = form.data['user']
        if text == '勉強する':
            return render_template('rulebase1.html', form=form, manachan_return='',passlog=passlog)


        manachan_return = chat.main_func(text)
        return render_template('index3.html', form=form, manachan_return=manachan_return)

    return render_template('index3.html',form=form)


def build_prompt(unmo):
    """AIインスタンスを取り、AIとResponderの名前を整形して返す"""
    return '{name}:{responder}> '.format(name=unmo.name,
    responder=unmo.responder_name)


number = 0

class chat:
    def main_func(text):
        proto = Unmo('manachan')
        try:
            response = proto.dialogue(text, 1)
        except IndexError as error:
            return '{}: {}'.format(type(error).__name__, str(error)),
            '警告: 辞書が空です。(Responder: {})'.format(proto.responder_name)
        else:
            return '{response}'.format(response=response)
            # {prompt}
            # prompt=build_prompt(proto),

    def rulebase_func(word):
        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
        with open('database.txt') as db_file:
            db = decoder.decode(db_file.read())
        with open('relation.txt') as rt_file:
            rt = decoder.decode(rt_file.read())

        if word in db:
            title= 'さ〜て！べんきょう始めるよ〜！！'
            important= '重要語句'
            item= "「 人工知能, 機械学習, 深層学習 」"
            manachan_memo= 'manachanメモ !!'
            description= db[word]['description']
            database_word= '{} 関連記事'.format(word)
            URL1= db[word]['URL1']
            URL2= db[word]['URL2']
            database= db[word]['key']
            relation= rt[word]['key']
            relation_word= '{} 関連語句'.format(word)
            if database == relation:
                 conti= rt[word]["relation"]
                 dic = {'manachan_memo':manachan_memo,'title':title,'item':item,'description':description,'database_word':database_word,'URL1':URL1,'URL2':URL2,
                 'database':database,'relation':relation,'relation_word':relation_word,'conti':conti,'important':important}
                 return dic
        else:
            unknown= 'そんなのしらないよ!! ﾌﾟﾝｽｶ ٩(๑`н´๑)۶!!'
            dic2= {'unknown':unknown}
            return dic2



if __name__ == '__main__':
    app.run(debug=True)
