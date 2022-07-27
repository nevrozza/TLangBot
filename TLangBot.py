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
        self.__db = sqlite3.connect('tlangbot.sqlite3', check_same_thread=False)
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

    def anti_native(self, row):
        self.del_last_msg()
        if row == 'ru':
            row = self.check_native()
            if row == 0:
                self.message('Выберите язык изучения')
            else:
                self.message('Ваш Родной язык изменён')
        elif row == 'eng':
            row = self.check_native()
            if row == 0:
                self.message('Choose language of learn')
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

    def check_lang(self):
        try:    
            self.__sql.execute(f"SELECT bot_lang FROM usercfg WHERE id = '{self.__id}'")
            return self.__sql.fetchone()[0]
        except: print('30 NONE')
    
    def check_name(self):
        try:    
            self.__sql.execute(f"SELECT name FROM usercfg WHERE id = '{self.__id}'")
            return self.__sql.fetchone()[0]
        except: print('81 NONE')

    def check_native(self):
        try:    
            self.__sql.execute(f"SELECT native_lang FROM usercfg WHERE id = '{self.__id}'")
            return self.__sql.fetchone()[0]
        except: print('41 NONE')

    def save_name(self, sent):
        self.__sql.execute(f"UPDATE usercfg SET name = '{sent.text}' WHERE id = '{self.__id}'")
        self.__db.commit() 
        self.del_last_msg(sent)
        
        row = self.check_lang()
        if row == 'ru':
            row = self.check_name()
            self.message(f"{row}, какой твой родной язык?", kb_native_language())
        elif row[0] == 'eng':
            row = self.check_name()
            self.message(f"{row}, what is your native language?", kb_native_language())    

    def callback_receiver(self, cb):
        row = self.check_lang()
        
        if cb == 'ru_bot':
            self.__sql.execute(f"UPDATE usercfg SET bot_lang = 'ru' WHERE id = '{self.__id}'")
            self.__db.commit()
            if row == 0:
                self.del_last_msg()
                sent = self.message('Как Вас зовут?')
                bot.register_next_step_handler(sent, self.save_name)
            elif row == 'eu' or row == 'eng':
                self.del_last_msg()
                self.message('Язык был успешно изменён')

        elif cb == 'eng_bot':
            self.__sql.execute(f"UPDATE usercfg SET bot_lang = 'eng' WHERE id = '{self.__id}'")
            self.__db.commit()
            if row == 0:
                self.del_last_msg()
                self.message("What's your name?")
                bot.register_next_step_handler(sent, self.save_name)
            elif row == 'ru' or row == 'eng':
                self.del_last_msg()
                self.message('Language has been changed')
        
        elif cb[0:6] == 'native':
            if row == 0:
                cb = 'eng_bot'
                self.new_user()
            else:
                
                self.anti_native(row)
                self.__sql.execute(f"UPDATE usercfg SET native_lang = '{cb[-2:]}' WHERE id = '{self.__id}'")
                self.__db.commit()
                

        elif cb[0:5] == 'first':
            if row == 0:
                cb = 'eng_bot'
                self.new_user()
            else:
                self.del_last_msg()

                self.__sql.execute(f"UPDATE usercfg SET first_lang = '{cb[-2:]}' WHERE id = '{self.__id}'")
                self.__db.commit()
                
                
        elif cb[0:6] == 'second':
            if row == 0:
                cb = 'eng_bot'
                self.new_user()
            else:
                self.del_last_msg()

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
        row = userid.check_lang()
        kb = tb.types.InlineKeyboardMarkup(row_width=1)
        if row == 0 or row == 'eng':
                btn1 = tb.types.InlineKeyboardButton('Reset bot', callback_data = 'clear_data')
                btn2 = tb.types.InlineKeyboardButton('Ne menyat nastroiki', callback_data = 'comeback')
        elif row == 'ru':
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

if __name__ == "__main__":
    TOKEN = '5175024223:AAEbmu4PvbOuwH0g9DayF4LCyatnzB0nYuU'
    bot = tb.TeleBot(TOKEN)
    lsmgs = {}


    @bot.message_handler(commands = ['start'])
    def start_command(message):
        userid = idk(message)
        row = userid.check_lang()
        if not row or row == 0:
            userid.anti_start()
            userid.new_user()
            userid.del_last_msg()
            userid.message("Hello, choose bot's language!\nПривет, выбери язык бота!", kb_bot_language())
        elif row == 'ru':
            userid.del_last_msg()
            userid.message('Мы тебя помним! Желаете перенастроить бота?', kb_clear_data(message))
        elif row == 'eng':
            userid.del_last_msg()
            userid.message('Mi teb9 pomnim! Желаете перенастроить бота?', kb_clear_data(message))
            
    @bot.callback_query_handler(func = lambda callback: callback.data)
    def check_callback_data(callback):
        userid = idk(callback.message)
        userid.callback_receiver(callback.data)
            
                 
            




    bot.polling()