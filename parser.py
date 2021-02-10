from config import *
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import time
import pandas as pd

class CustomDataFrame:

    def __init__(self):

        self.data = []


    def addNote(self, textToSplit : str) -> None:
        textToSplit = textToSplit.lstrip('👤')
        splittedText = textToSplit.split('Должность:')
        name = splittedText[0].rstrip('\n').lstrip(' ')
        textToSplit = splittedText[1]
        print(name)
        splittedText = textToSplit.split('Профессия:')
        position = splittedText[0].rstrip('\n').lstrip(' ')
        textToSplit = splittedText[1]
        # print(position)
        splittedText = textToSplit.split('Опыт работы в текущей профессии:')
        profession = splittedText[0].rstrip('\n').lstrip(' ')
        textToSplit = splittedText[1]
        # print(profession)
        splittedText = textToSplit.split('Другой опыт:')
        profexp = splittedText[0].rstrip('\n').lstrip(' ')
        textToSplit = splittedText[1]
        # print(profexp)
        splittedText = textToSplit.split('Сильные стороны:')
        anotherexp = splittedText[0].rstrip('\n').lstrip(' ').lstrip('\n')
        textToSplit = splittedText[1]
        # print(anotherexp)
        splittedText = textToSplit.split('Как связаться:')
        strongs = splittedText[0].rstrip('\n').lstrip(' ').lstrip('\n')
        textToSplit = splittedText[1]
        # print(strongs)
        contacts = textToSplit.lstrip(' ').rstrip('\n')
        # print(contacts)
        # print()
        # print()
        self.data.append([name, position, profession, profexp, anotherexp, strongs, contacts])
        print('added')

    def getDataFrame(self):
        df = pd.DataFrame(self.data, columns=['name', 'position', 'profession', 'profexp', 'anotherexp', 'strongs', 'contacts'])
        return df

client = TelegramClient(username, api_id, api_hash)
client.start()
botEntity = client.get_entity(botTag)
client.send_message(botEntity, startCommand)




for professionIndex in range(4, 5):
    dataFrame = CustomDataFrame()
    for yearExperience in range(21):
        client.send_message(botEntity, findCommand)
        time.sleep(0.25)
        messages = client.get_messages(botEntity)
        try: messages[0].click()
        except Exception: continue
        time.sleep(0.25)
        messages = client.get_messages(botEntity)

        try: messages[0].click(professionIndex)
        except Exception: continue
        time.sleep(0.25)
        client.send_message(botEntity, str(yearExperience))
        time.sleep(0.25)
        messages = client.get_messages(botEntity)
        try: messages[0].click()
        except Exception: continue
        time.sleep(0.25)
        while True: # цикл который перебирает количество сообщений
            limit = 1
            while True: 
                messages = client.get_messages(botEntity, limit)
                # print(messages[-1].message)
                if messages[-1].message == '🎉 Я нашел для тебя следующие варианты:' or 'К сожалению, мы не нашли менторов, подходящих под твой запрос.' in messages[-1].message:
                    messages = messages[1:-1]
                    break
                limit += 1
                time.sleep(0.15)
            print(len(messages))
            for message in messages:
                try:
                    dataFrame.addNote(message.message)
                except Exception:
                    pass
            messages = client.get_messages(botEntity)
            lastMessage = messages[0]
            try:
                if lastMessage.reply_markup.rows[0].buttons[1].text == 'Покажи еще':
                    lastMessage.click(1)
                else:
                    print(lastMessage.reply_markup.rows[0].buttons[1].text)
                    break
            except Exception:
                break
            time.sleep(1)
        # print(messages)
        print(professionIndex, yearExperience)
        time.sleep(2)

    df = dataFrame.getDataFrame()
    df.drop_duplicates(keep='first', inplace=True)
    print(df)
    df.to_csv('result{}.csv'.format(professionIndex), encoding='utf-8-sig', index=False, sep = ';')
