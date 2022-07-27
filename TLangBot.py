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
        self.__db = sqlite3.connect(r"D:\github\TLangBot\tlangbot.sqlite3", check_same_thread=False)
        self.__sql = self.__db.cursor()

    def new_user(self):
        self.__sql.execute("INSERT INTO usercfg VALUES(?, 0, 0, 0, 0, 0, 0, 0, 0)", (self.__id,))
        self.__db.commit()
        bot.send_message('-1001763397724', f'new user: {self.__id}')
        print(f'new user: {self.__id}')
        

    def anti_start(self):
        try:
            self.__sql.execute(f"DELETE FROM usercfg WHERE id = '{self.__id}'")
            self.__db.commit()
        except: print('36 NONE')

    def anti_native(self, bot_lang):
        self.del_last_msg()
        native_lang = self.check_db('native_lang')
        
        if bot_lang == 'ru':
            if native_lang == 0:
                self.message('Выберите язык изучения', kb_first_language())
            else:
                self.message('Ваш Родной язык изменён')
        elif bot_lang == 'eng':
            if native_lang == 0:
                self.message('Choose language of learn', kb_first_language())
            else:
                self.message('Your native language has been changed')

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
            return self.__sql.fetchone()[0]
        except: print('30 NONE')
    

    def save_name(self, sent):
        self.__sql.execute(f"UPDATE usercfg SET name = '{sent.text}' WHERE id = '{self.__id}'")
        self.__db.commit() 
        self.del_last_msg(sent)
        name = self.check_db('name')
        lang = self.check_db('bot_lang')
        kb = kb_native_language()
        if lang == 'ru':
            self.message(f"{name}, какой твой родной язык?", kb)
        elif lang == 'eng':
            self.message(f"{name}, what is your native language?", kb)    

    def callback_receiver(self, cb):
        bot_lang = self.check_db('bot_lang')
        
        if cb == 'ru_bot':
            self.__sql.execute(f"UPDATE usercfg SET bot_lang = 'ru' WHERE id = '{self.__id}'")
            self.__db.commit()
            if bot_lang == 0:
                self.del_last_msg()
                sent = self.message('Как Вас зовут?')
                bot.register_next_step_handler(sent, self.save_name)
            elif bot_lang == 'ru' or bot_lang == 'eng':
                self.del_last_msg()
                self.message('Язык был успешно изменён')

        elif cb == 'eng_bot':
            self.__sql.execute(f"UPDATE usercfg SET bot_lang = 'eng' WHERE id = '{self.__id}'")
            self.__db.commit()
            if bot_lang == 0:
                self.del_last_msg()
                self.message("What's your name?")
                bot.register_next_step_handler(sent, self.save_name)
            elif bot_lang == 'ru' or bot_lang == 'eng':
                self.del_last_msg()
                self.message('Language has been changed')
        
        elif cb[0:6] == 'native':
            if bot_lang == 0:
                cb = 'eng_bot'
                self.new_user()
            else:
                
                self.anti_native(bot_lang)
                self.__sql.execute(f"UPDATE usercfg SET native_lang = '{cb[-2:]}' WHERE id = '{self.__id}'")
                self.__db.commit()
                

        elif cb[0:5] == 'first':
            second_lang = self.check_db('second_lang')
            bot_lang = self.check_db('bot_lang')
            if bot_lang == 0:
                cb = 'eng_bot'
                self.new_user()
            elif cb[-2:] == second_lang:
                if bot_lang == 'ru':
                    self.message('Вы не можете изучать 2 одинаковых языка')
                elif bot_lang == 'eng':
                    self.message('You cannot choice 2 odinakovix yazika')
            else:
                self.del_last_msg()
                if bot_lang == 'ru':
                    self.message('Хотите ли Вы выбрать ещё один язык?')
                elif bot_lang == 'eng':
                    self.message('Do you want to choose second language?')
                self.__sql.execute(f"UPDATE usercfg SET first_lang = '{cb[-2:]}' WHERE id = '{self.__id}'")
                self.__db.commit()
                
                
        elif cb[0:6] == 'second':
            first_lang = self.check_db('first_lang')
            if bot_lang == 0:
                cb = 'eng_bot'
                self.new_user()
            elif cb[-2:] == first_lang:
                if bot_lang == 'ru':
                    self.message('Вы не можете изучать 2 одинаковых языка')
                elif bot_lang == 'eng':
                    self.message('You cannot choice 2 odinakovix yazika')
            else:
                self.del_last_msg()
                if bot_lang == 'ru':
                    self.message('Во сколько Вы хотите получать по мск')
                elif bot_lang == 'eng':
                    self.message('ENG Во сколько Вы хотите получать по мск ')
                self.__sql.execute(f"UPDATE usercfg SET second_lang = '{cb[-2:]}' WHERE id = '{self.__id}'")
                self.__db.commit()
                
                
        
        elif cb == 'clear_data':
            self.__sql.execute(f"DELETE FROM usercfg WHERE id = '{self.__id}'")
            self.__db.commit()
            self.del_last_msg()
            start_command(self.__message)
        elif cb == 'comeback':
            pass

    def message(self, text='чел забыл написать сообщение', kb = None):   
         
        lmsg = bot.send_message(self.__id, text, reply_markup=kb)
        lsmgs[self.__id] = lmsg.id
        
        return lmsg            

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
        if bot_lang == 0 or bot_lang == 'eng':
                btn1 = tb.types.InlineKeyboardButton('Reset bot', callback_data = 'clear_data')
                btn2 = tb.types.InlineKeyboardButton('Ne menyat nastroiki', callback_data = 'comeback')
        elif bot_lang == 'ru':
                btn1 = tb.types.InlineKeyboardButton('Настроить бота заново', callback_data = 'clear_data')
                btn2 = tb.types.InlineKeyboardButton('Не менять настройки', callback_data = 'comeback')

        kb.add(btn1,btn2)
        return kb

def kb_native_language():
    
    kb = tb.types.InlineKeyboardMarkup(row_width=3)
    btn1 = tb.types.InlineKeyboardButton('Ru', callback_data = 'native_ru')
    btn2 = tb.types.InlineKeyboardButton('Eng', callback_data = 'native_en')
    btn3 = tb.types.InlineKeyboardButton('Kor', callback_data = 'native_ko')
    btn4 = tb.types.InlineKeyboardButton('Pl', callback_data = 'native_pl')
    btn5 = tb.types.InlineKeyboardButton('Ar', callback_data = 'native_ar')
    btn6 = tb.types.InlineKeyboardButton('Po', callback_data = 'native_po')
    btn7 = tb.types.InlineKeyboardButton('Go', callback_data = 'native_go')
    btn8 = tb.types.InlineKeyboardButton('Rum', callback_data = 'native_rm')
    btn9 = tb.types.InlineKeyboardButton('Ivr', callback_data = 'native_iv')
    btn10 = tb.types.InlineKeyboardButton('Sp', callback_data = 'native_sp')
    btn11 = tb.types.InlineKeyboardButton('Tu', callback_data = 'native_tu')
    btn12 = tb.types.InlineKeyboardButton('It', callback_data = 'native_it')
    btn13 = tb.types.InlineKeyboardButton('Ua', callback_data = 'native_ua')
    btn14 = tb.types.InlineKeyboardButton('Zh', callback_data = 'native_zh')
    btn15 = tb.types.InlineKeyboardButton('Fr', callback_data = 'native_fr')
    btn16 = tb.types.InlineKeyboardButton('Sw', callback_data = 'native_sw')
    btn17 = tb.types.InlineKeyboardButton('De', callback_data = 'native_de')
    btn18 = tb.types.InlineKeyboardButton('Ja', callback_data = 'native_ja')
    
    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn15, btn16, btn17, btn18)
    return kb     

def kb_first_language():
    kb = tb.types.InlineKeyboardMarkup(row_width=3)
    btn1 = tb.types.InlineKeyboardButton('Ru', callback_data = 'first_ru')
    btn2 = tb.types.InlineKeyboardButton('Eng', callback_data = 'first_en')
    btn3 = tb.types.InlineKeyboardButton('Kor', callback_data = 'first_ko')
    btn4 = tb.types.InlineKeyboardButton('Pl', callback_data = 'first_pl')
    btn5 = tb.types.InlineKeyboardButton('Ar', callback_data = 'first_ar')
    btn6 = tb.types.InlineKeyboardButton('Po', callback_data = 'first_po')
    btn7 = tb.types.InlineKeyboardButton('Go', callback_data = 'first_go')
    btn8 = tb.types.InlineKeyboardButton('Rum', callback_data = 'first_rm')
    btn9 = tb.types.InlineKeyboardButton('Ivr', callback_data = 'first_iv')
    btn10 = tb.types.InlineKeyboardButton('Sp', callback_data = 'first_sp')
    btn11 = tb.types.InlineKeyboardButton('Tu', callback_data = 'first_tu')
    btn12 = tb.types.InlineKeyboardButton('It', callback_data = 'first_it')
    btn13 = tb.types.InlineKeyboardButton('Ua', callback_data = 'first_ua')
    btn14 = tb.types.InlineKeyboardButton('Zh', callback_data = 'first_zh')
    btn15 = tb.types.InlineKeyboardButton('Fr', callback_data = 'first_fr')
    btn16 = tb.types.InlineKeyboardButton('Sw', callback_data = 'first_sw')
    btn17 = tb.types.InlineKeyboardButton('De', callback_data = 'first_de')
    btn18 = tb.types.InlineKeyboardButton('Ja', callback_data = 'first_ja')
    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn15, btn16, btn17, btn18)
    return kb

def kb_second_language():
    kb = tb.types.InlineKeyboardMarkup(row_width=3)
    btn1 = tb.types.InlineKeyboardButton('Ru', callback_data = 'second_ru')
    btn2 = tb.types.InlineKeyboardButton('Eng', callback_data = 'second_en')
    btn3 = tb.types.InlineKeyboardButton('Kor', callback_data = 'second_ko')
    btn4 = tb.types.InlineKeyboardButton('Pl', callback_data = 'second_pl')
    btn5 = tb.types.InlineKeyboardButton('Ar', callback_data = 'second_ar')
    btn6 = tb.types.InlineKeyboardButton('Po', callback_data = 'second_po')
    btn7 = tb.types.InlineKeyboardButton('Go', callback_data = 'second_go')
    btn8 = tb.types.InlineKeyboardButton('Rum', callback_data = 'second_rm')
    btn9 = tb.types.InlineKeyboardButton('Ivr', callback_data = 'second_iv')
    btn10 = tb.types.InlineKeyboardButton('Sp', callback_data = 'second_sp')
    btn11 = tb.types.InlineKeyboardButton('Tu', callback_data = 'second_tu')
    btn12 = tb.types.InlineKeyboardButton('It', callback_data = 'second_it')
    btn13 = tb.types.InlineKeyboardButton('Ua', callback_data = 'second_ua')
    btn14 = tb.types.InlineKeyboardButton('Zh', callback_data = 'second_zh')
    btn15 = tb.types.InlineKeyboardButton('Fr', callback_data = 'second_fr')
    btn16 = tb.types.InlineKeyboardButton('Sw', callback_data = 'second_sw')
    btn17 = tb.types.InlineKeyboardButton('De', callback_data = 'second_de')
    btn18 = tb.types.InlineKeyboardButton('Ja', callback_data = 'second_ja')
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
        elif bot_lang == 'eng':
            userid.del_last_msg()
            userid.message('Mi teb9 pomnim! Желаете перенастроить бота?', kb_clear_data(message))
            
    @bot.callback_query_handler(func = lambda callback: callback.data)
    def check_callback_data(callback):
        userid = idk(callback.message)
        userid.callback_receiver(callback.data)
            
                 
            




    bot.polling()