import json
import collections

decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
with open('database.txt') as db_file:
    db = decoder.decode(db_file.read())
with open('relation.txt') as rt_file:
    rt = decoder.decode(rt_file.read())

class Rulebase:

    # def __init__(self, db,rt):
    #     self.db = db
    #     self.rt = rt

    def rule_response(self):
        count= 0
        while True:
            print(' ')
            if count== 0:
                print('よ〜し！べんきょう始めるよ〜！！')
                print('')
                print('「人工知能　','機械学習　','深層学習　」')
            else:
                print('上記から調べたい言葉を入力してね。')

            word= input('Keyward ')

            if word == 'exit':

                print('')
                break

            if word in db:
                count+= 1
                print(' ')
                print(db[word]['description'])
                print(db[word]['URL1'])
                print(db[word]['URL2'])
                database= db[word]['key']
                relation= rt[word]['key']
                print(' ')
                print('{} 関連の語句'.format(word))
                if database == relation:
                    print(rt[word]["relation"])
            else:
                print('それはわからんばい。')
