from django.core.management.base import BaseCommand
from main_app.models import Conversion
import openai
import re
import pandas as pd
import time


openai.api_key = ""


def try_repeat(func):
    def wrapper(*args, **kwargs):
        count = 3

        while count:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print('!!! Error:', e)
                count -= 1
            time.sleep(20)

    return wrapper


@try_repeat
def model1(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": text}
        ]
    )
    return completion.choices[0].message.content


@try_repeat
def model2(text):
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        temperature=0,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return completion.choices[0].text


def get_first_word_with_number(x):
    for word in x.split():
        if re.search(r'\d', word):
            return word
    return None


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        # df1 = pd.DataFrame()

        df1 = pd.read_excel('convs1.xlsx', dtype='str')

        p = 0
        convs = Conversion.objects.all()

        for conv in convs:

            p += 1

            if df1[(df1['category'] == conv.category.name) & (df1['from'] == conv.from_unit.name) & (df1['to'] == conv.to_unit.name)].index.size != 0:
                print(p, '->', conv.category.name, conv.from_unit.name, conv.to_unit.name)
                continue

            # пропускаем килограммы и литры - они настраиваются с помощью sql скрипта - коэфф 0.001
            if conv.from_unit.id == 13 or conv.from_unit.id == 16:
                continue

            # if p == 5:
            #     break

            unit = ''
            if conv.to_unit.pk == 1:
                unit = 'граммы'
            elif conv.to_unit.pk == 7:
                unit = 'миллилитры'

            text = 'дай коэффициент перевода для ' + conv.category.name + ' из ' \
                   + conv.from_unit.name + ' в ' + unit + ', напиши только число без других слов'
            print(p, '->', text)

            dic1 = {'category': conv.category.name, 'from': conv.from_unit.name, 'to': conv.to_unit.name}
            dics = [dic1]
            funcs = [model1]
            
            for ind in range(1):
                print('--- Model' + str(ind + 1))
                for i in range(1, 6):
                    answer = funcs[ind](text)
                    answer = answer.replace('\n', '')

                    if answer[-1] == '.':
                        answer = answer[:-1]
                    # print("Ans" + str(i) + ':',  answer)

                    dics[ind]['ans' + str(i)] = answer

                    if not any(char.isdigit() for char in answer):
                        # print("!!! Exp" + str(i) + ": в строке нет числа")
                        continue

                    match = re.search(r'\D+$', answer)
                    if match:
                        answer = answer[:-len(match.group())]

                    res = get_first_word_with_number(answer)

                    try:
                        if '-' in res:
                            res = (float(res.split('-')[0].replace(',', '.')) + float(res.split('-')[1].replace(',', '.'))) / 2
                        else:
                            res = float(res.replace(',', '.'))
                    except:
                        continue
                    # print("Exp" + str(i) + ':', res)
                    dics[ind]['kef' + str(i)] = res
                    print(i, end=' ')
                    time.sleep(20)
                print()

            df1 = pd.concat([df1, pd.Series(dics[0]).to_frame().T]).reset_index(drop=True)
            print()

            df1.to_excel('convs1.xlsx', index=False)
