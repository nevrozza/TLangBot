import sqlite3
import telebot as tb
import time
import schedule

from threading import Thread
# from random import sample

class idk:
    
    
    def __init__(self, message):
        self.__message = message
        self.__id = message.chat.id
        self.__db = sqlite3.connect(r"tlangbot.sqlite3", check_same_thread=False)
        self.__sql = self.__db.cursor()
        self.__name = self.check_db('name')
        self.__bot_lang = self.check_db('bot_lang')
        self.__native_lang = self.check_db('native_lang')
        self.__first_lang = self.check_db('first_lang')
        self.__second_lang = self.check_db('second_lang')
        

    def update(self):
        self.__name = self.check_db('name')
        self.__bot_lang = self.check_db('bot_lang')
        self.__native_lang = self.check_db('native_lang')
        self.__first_lang = self.check_db('first_lang')
        self.__second_lang = self.check_db('second_lang')
        


    def new_user(self):
        
        self.__sql.execute("INSERT INTO usercfg VALUES(?, 0, 0, 0, 0, 0, 0)", (self.__id,))
        self.__db.commit()
        bot.send_message('-1001763397724', f'new user: {self.__id}')
        print(f'new user: {self.__id}')
        self.update()

    def anti_start(self):
        
        try:
            self.__sql.execute(f"DELETE FROM usercfg WHERE id = '{self.__id}'")
            self.__db.commit()
        except: print('36 NONE')
        self.update()
    def anti_native(self):
        
        self.del_last_msg()
        
        
        if self.__bot_lang == 'ru':
            if self.__native_lang == 0:
                self.message('Выберите язык изучения', kb_languages('first'))
            else:
                self.message('Ваш Родной язык изменён')
        elif self.__bot_lang == 'en':
            if self.__native_lang == 0:
                self.message('Choose language of learn', kb_languages('first'))
            else:
                self.message('Your native language has been changed')
        
    def yes_second(self):
        
        self.del_last_msg()
        if self.__bot_lang == 'ru':
            self.message('Выберите второй язык изучения', kb_languages('second'))
        elif self.__bot_lang == 'en':
            self.message('Choose second language of learn', kb_languages('second'))
            

    def del_last_msg(self, sent = None):
        try:
            bot.delete_message(self.__id, lsmgs[self.__id])
            del lsmgs[self.__id]
        except: print('59 NONE')
             
        try:
            bot.delete_message(self.__id, self.__message.id)
        except: print('63 NONE')
        if sent != None:
            try:
                bot.delete_message(self.__id, sent.id)
            except: print('63 NONE')

    

    def check_db(self, target):
        
        try:    
            self.__sql.execute(f"SELECT {target} FROM usercfg WHERE id = '{self.__id}'")
            row = self.__sql.fetchone()[0]
            print(target, row)
            return row
        except: print('30 NONE')
    
    

    def save_name(self, sent):
       
        self.__sql.execute(f"UPDATE usercfg SET name = '{sent.text}' WHERE id = '{self.__id}'")
        self.__db.commit() 
        self.update()
        self.del_last_msg(sent)
        kb = kb_languages('native')
        
        if self.__bot_lang == 'ru':
            self.message(f"{self.__name}, какой твой родной язык?", kb)
        elif self.__bot_lang == 'en':
            self.message(f"{self.__name}, what is your native language?", kb)    

    def callback_receiver(self, cb):
        
        bot_lang = self.__bot_lang
        native_lang = self.__native_lang
        first_lang = self.__first_lang
        second_lang = self.__second_lang
        if cb == 'ru_bot':
            self.__sql.execute(f"UPDATE usercfg SET bot_lang = 'ru' WHERE id = '{self.__id}'")
            self.__db.commit()
            if bot_lang == 0:
                self.del_last_msg()
                sent = self.message('Как Вас зовут?')
                bot.register_next_step_handler(sent, self.save_name)
            elif bot_lang == 'ru' or bot_lang == 'en':
                self.del_last_msg()
                self.message('Язык был успешно изменён')

        elif cb == 'eng_bot':
            self.__sql.execute(f"UPDATE usercfg SET bot_lang = 'en' WHERE id = '{self.__id}'")
            self.__db.commit()
            if bot_lang == 0:
                self.del_last_msg()
                sent = self.message("What's your name?")
                bot.register_next_step_handler(sent, self.save_name)
            elif bot_lang == 'ru' or bot_lang == 'en':
                self.del_last_msg()
                self.message('Language has been changed')
        
        elif cb[0:6] == 'native':
            if bot_lang == 0:
                cb = 'eng_bot'
                self.new_user()
            else:
                
                self.anti_native()
                self.__sql.execute(f"UPDATE usercfg SET native_lang = '{cb[-2:]}' WHERE id = '{self.__id}'")
                self.__db.commit()
                

        elif cb[0:5] == 'first':
            if bot_lang == 0:
                cb = 'eng_bot'
                self.new_user()
            elif cb[-2:] == native_lang:
                if bot_lang == 'ru':
                    self.message('Вы не можете выбрать одинаковые языки')
                elif bot_lang == 'en':
                    self.message('рпарпаВы не можете выбрать одинаковые языки')

            elif cb[-2:] == second_lang:
                if bot_lang == 'ru':
                    self.message('Вы не можете изучать 2 одинаковых языка')
                elif bot_lang == 'en':
                    self.message('You cannot choice 2 odinakovix yazika')
            else:
                self.del_last_msg()
                if bot_lang == 'ru':
                    self.message('Хотите ли Вы выбрать ещё один язык?', kb_second_choose(self.__message))
                elif bot_lang == 'en':
                    self.message('Do you want to choose second language?', kb_second_choose(self.__message))
                self.__sql.execute(f"UPDATE usercfg SET first_lang = '{cb[-2:]}' WHERE id = '{self.__id}'")
                self.__db.commit()
                
                
        elif cb[0:6] == 'second':
            if bot_lang == 0:
                cb = 'eng_bot'
                self.new_user()
            elif cb[-2:] == native_lang:
                if bot_lang == 'ru':
                    self.message('Вы не можете выбрать одинаковые языки')
                elif bot_lang == 'en':
                    self.message('рпарпаВы не можете выбрать одинаковые языки')
            elif cb[-2:] == first_lang:
                if bot_lang == 'ru':
                    self.message('Вы не можете изучать 2 одинаковых языка')
                elif bot_lang == 'en':
                    self.message('You cannot choice 2 odinakovix yazika')
            else:
                self.__sql.execute(f"UPDATE usercfg SET second_lang = '{cb[-2:]}' WHERE id = '{self.__id}'")
                self.__db.commit()
                self.update()
                second_lang = self.__second_lang
                self.del_last_msg()
                if bot_lang == 'ru':
                    self.message(f'Вот ваши настройки бота:\nВаше имя: {self.__name}\nРодной язык: {native_lang}\nПервый язык: {first_lang}\nВторой язык: {second_lang}', kb_clear_data(self.__message))
                elif bot_lang == 'en':
                    self.message(f'This is yours bot settings:\nYour name: {self.__name}\nNative language: {native_lang}\nFirst language: {first_lang}\nSecond language: {second_lang}', kb_clear_data(self.__message))
                
                
                
        
        elif cb == 'clear_data':
            self.__sql.execute(f"DELETE FROM usercfg WHERE id = '{self.__id}'")
            self.__db.commit()
            self.del_last_msg()
            start_command(self.__message)
        elif cb == 'comeback':
            pass
        elif cb == 'yes_second':
            self.yes_second()
        elif cb == 'no_second':
            cb = 'second_00'
            self.callback_receiver(cb)
        self.update()
    def message(self, text='чел забыл написать сообщение', kb = None):   
         
        lmsg = bot.send_message(self.__id, text, reply_markup=kb)
        lsmgs[self.__id] = lmsg.id
        
        return lmsg   

    def sam_bot(self, __id):
        
        
        return

def kb_bot_language():
    kb = tb.types.InlineKeyboardMarkup(row_width=1)
    btn1 = tb.types.InlineKeyboardButton('Ru', callback_data = 'ru_bot')
    btn2 = tb.types.InlineKeyboardButton('Eng', callback_data = 'eng_bot')
    kb.add(btn1,btn2)
    return kb

def kb_clear_data(message):
    userid = idk(message)
    bot_lang = userid.check_db('bot_lang')
    kb = tb.types.InlineKeyboardMarkup(row_width=1)
    if bot_lang == 0 or bot_lang == 'en':
            btn2 = tb.types.InlineKeyboardButton('Reset bot', callback_data = 'clear_data')
            btn1 = tb.types.InlineKeyboardButton('Ne menyat nastroiki', callback_data = 'comeback')
    elif bot_lang == 'ru':
            btn2 = tb.types.InlineKeyboardButton('Настроить бота заново', callback_data = 'clear_data')
            btn1 = tb.types.InlineKeyboardButton('Не менять настройки', callback_data = 'comeback')

    kb.add(btn1,btn2)
    return kb

def kb_second_choose(message):
    userid = idk(message)
    bot_lang = userid.check_db('bot_lang')
    kb = tb.types.InlineKeyboardMarkup(row_width=1)
    if bot_lang == 0 or bot_lang == 'en':
        btn1 = tb.types.InlineKeyboardButton('Yes', callback_data = 'yes_second')
        btn2 = tb.types.InlineKeyboardButton('No', callback_data = 'no_second')
    elif bot_lang == 'ru':
        btn1 = tb.types.InlineKeyboardButton('Да', callback_data = 'yes_second')
        btn2 = tb.types.InlineKeyboardButton('Нет', callback_data = 'no_second')
    kb.add(btn1,btn2)
    return kb

def kb_languages(choice):
    
    kb = tb.types.InlineKeyboardMarkup(row_width=3)
    
    btn1 = tb.types.InlineKeyboardButton('Ru', callback_data = f'{choice}_ru')
    btn2 = tb.types.InlineKeyboardButton('Eng', callback_data = f'{choice}_en')
    btn3 = tb.types.InlineKeyboardButton('Kor', callback_data = f'{choice}_ko')
    btn4 = tb.types.InlineKeyboardButton('Pl', callback_data = f'{choice}_pl')
    btn5 = tb.types.InlineKeyboardButton('Ar', callback_data = f'{choice}_ar')
    btn6 = tb.types.InlineKeyboardButton('Po', callback_data = f'{choice}_po')
    btn7 = tb.types.InlineKeyboardButton('Go', callback_data = f'{choice}_go')
    btn8 = tb.types.InlineKeyboardButton('Rum', callback_data = f'{choice}_rm')
    btn9 = tb.types.InlineKeyboardButton('Ivr', callback_data = f'{choice}_iv')
    btn10 = tb.types.InlineKeyboardButton('Sp', callback_data = f'{choice}_sp')
    btn11 = tb.types.InlineKeyboardButton('Tu', callback_data = f'{choice}_tu')
    btn12 = tb.types.InlineKeyboardButton('It', callback_data = f'{choice}_it')
    btn13 = tb.types.InlineKeyboardButton('Ua', callback_data = f'{choice}_ua')
    btn14 = tb.types.InlineKeyboardButton('Zh', callback_data = f'{choice}_zh')
    btn15 = tb.types.InlineKeyboardButton('Fr', callback_data = f'{choice}_fr')
    btn16 = tb.types.InlineKeyboardButton('Sw', callback_data = f'{choice}_sw')
    btn17 = tb.types.InlineKeyboardButton('De', callback_data = f'{choice}_de')
    btn18 = tb.types.InlineKeyboardButton('Ja', callback_data = f'{choice}_ja')
    
    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn15, btn16, btn17, btn18)
    return kb     


if __name__ == "__main__":
    TOKEN = '5175024223:AAEbmu4PvbOuwH0g9DayF4LCyatnzB0nYuU'
    bot = tb.TeleBot(TOKEN)
    lsmgs = {}


    @bot.message_handler(commands = ['start'])
    def start_command(message):
        userid = idk(message)
        bot_lang = userid.check_db('bot_lang')
        if not bot_lang or bot_lang == 0:
            userid.anti_start()
            userid.new_user()
            userid.del_last_msg()
            userid.message("Hello, choose bot's language!\nПривет, выбери язык бота!", kb_bot_language())
        elif bot_lang == 'ru':
            userid.del_last_msg()
            userid.message('Мы тебя помним! Желаете перенастроить бота?', kb_clear_data(message))
        elif bot_lang == 'en':
            userid.del_last_msg()
            userid.message('Mi teb9 pomnim! Желаете перенастроить бота?', kb_clear_data(message))
            
    @bot.callback_query_handler(func = lambda callback: callback.data)
    def check_callback_data(callback):
        userid = idk(callback.message)
        userid.callback_receiver(callback.data)
            
                 
            




    bot.polling()