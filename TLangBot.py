
import sqlite3
import telebot as tb
import time
import schedule

from random import choices 
from threading import Thread
class idk:
    
    
    def __init__(self, message):
        self.__counts_of_words = list(range(1, 4679))
        self.__message = message
        self.__id = message.chat.id
        self.__db = sqlite3.connect(r"tlangbot.sqlite3", check_same_thread=False)
        self.__sql = self.__db.cursor()
        self.__name = self.check_db('name')
        self.__bot_lang = self.check_db('bot_lang')
        self.__native_lang = self.check_db('native_lang')
        self.__first_lang = self.check_db('first_lang')
        self.__second_lang = self.check_db('second_lang')
        

    def update(self, target):
        if target == 'name':
            self.__name = self.check_db('name')
        elif target == 'bot_lang':
            self.__bot_lang = self.check_db('bot_lang')
        elif target == 'native_lang':
            self.__native_lang = self.check_db('native_lang')
        elif target == 'first_lang':
            self.__first_lang = self.check_db('first_lang')
        elif target == 'second_lang':
            self.__second_lang = self.check_db('second_lang')
        elif target == 'all':
            self.__name = self.check_db('name')
            self.__bot_lang = self.check_db('bot_lang')
            self.__native_lang = self.check_db('native_lang')
            self.__first_lang = self.check_db('first_lang')
            self.__second_lang = self.check_db('second_lang')
        


    def new_user(self):
        
        self.__sql.execute("INSERT INTO usercfg VALUES(?, 0, 0, 0, 0, 0, 0, 0, 0, 0)", (self.__id,))
        self.__db.commit()
        
        self.update('all')

    def anti_start(self):
        try:
            self.__sql.execute(f"DELETE FROM usercfg WHERE id = '{self.__id}'")
            self.__db.commit()
        except: print('36 NONE')
        self.update('all')
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
            
            return row
        except: print('30 NONE')
    
    

    def save_name(self, sent):
       
        self.__sql.execute(f"UPDATE usercfg SET name = '{sent.text}' WHERE id = '{self.__id}'")
        self.__db.commit() 
        self.update('name')
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
            self.update('bot_lang')
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
            self.update('bot_lang')
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
                self.update('native_lang')

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
                self.update('first_lang')
                
                
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
                self.update('second_lang')
                second_lang = self.__second_lang
                self.del_last_msg()
                if bot_lang == 'ru':
                    self.message(f'Вот ваши настройки бота:\nВаше имя: {self.__name}\nРодной язык: {native_lang}\nПервый язык: {first_lang}\nВторой язык: {second_lang}', kb_clear_data(self.__message, 'newbie'))
                elif bot_lang == 'en':
                    self.message(f'This is yours bot settings:\nYour name: {self.__name}\nNative language: {native_lang}\nFirst language: {first_lang}\nSecond language: {second_lang}', kb_clear_data(self.__message, 'newbie'))
                
                
                
        
        elif cb == 'clear_data':
            self.__sql.execute(f"DELETE FROM usercfg WHERE id = '{self.__id}'")
            self.__db.commit()
            self.del_last_msg()
            self.update('all')
            start_command(self.__message)
        elif cb == 'comeback':
            self.__sql.execute(f"UPDATE usercfg SET active = 1 WHERE id = '{self.__id}'")
            self.__db.commit()
            self.del_last_msg()
            self.first_spam()
            if self.__second_lang != 0:
                self.second_spam()
        elif cb == 'yes_second':
            self.yes_second()
        elif cb == 'no_second':
            cb = 'second_00'
            self.callback_receiver(cb)

        elif cb == 'correct_answer':
            self.del_last_msg()
            self.__sql.execute(f"SELECT correct_words FROM usercfg WHERE id = '{self.__id}'")
            previous_count = self.__sql.fetchone()[0]
            self.__sql.execute(f"UPDATE usercfg SET correct_words = '{previous_count + 1}'WHERE id = '{self.__id}'")
            self.__db.commit()
            correct_words = previous_count + 1
            self.__sql.execute(f"SELECT count_of_words FROM usercfg WHERE id = '{self.__id}'")
            learned_words = self.__sql.fetchone()[0]
            if self.__bot_lang == 'ru':
                self.message(f'Вы ответили верно!\nКол-во правильных ответов: {correct_words}\nКол-во слов: {learned_words}', kb_delete_current_message(self.__message))
            elif self.__bot_lang == 'en':
                self.message(f'ENGGNGNВы ответили верно!\nКол-во правильных ответов: {correct_words}\nКол-во слов: {learned_words}', kb_delete_current_message(self.__message))

        elif cb[:19] == 'wrong_answer_first_':
            self.del_last_msg()
            self.__sql.execute(f"SELECT count_of_words FROM usercfg WHERE id = '{self.__id}'")
            learned_words = self.__sql.fetchone()[0]
            self.__sql.execute(f"SELECT correct_words FROM usercfg WHERE id = '{self.__id}'")
            correct_words = self.__sql.fetchone()[0]
            self.__sql.execute(f"SELECT {self.__native_lang} FROM words WHERE en = '{cb[19:]}'")
            native_correct_word = self.__sql.fetchone()[0]
            self.__sql.execute(f"SELECT {self.__first_lang} FROM words WHERE en = '{cb[19:]}'")
            first_correct_word = self.__sql.fetchone()[0]
            if self.__bot_lang == 'ru':
                self.message(f'Вы ответили неверно!\nПравильный ответ:\n{first_correct_word} - {native_correct_word}\nКол-во правильных ответов: {correct_words}\nКол-во слов: {learned_words}', kb_delete_current_message(self.__message))
            elif self.__bot_lang == 'en':
                self.message(f'ENGGNGNВы ответили неверно!\nПравильный ответ:\n{first_correct_word} - {native_correct_word}\nКол-во правильных ответов: {correct_words}\nКол-во слов: {learned_words}', kb_delete_current_message(self.__message))
        elif cb[:20] == 'wrong_answer_second_':
            self.del_last_msg()
            self.__sql.execute(f"SELECT count_of_words FROM usercfg WHERE id = '{self.__id}'")
            learned_words = self.__sql.fetchone()[0]
            self.__sql.execute(f"SELECT correct_words FROM usercfg WHERE id = '{self.__id}'")
            correct_words = self.__sql.fetchone()[0]
            self.__sql.execute(f"SELECT {self.__native_lang} FROM words WHERE en = '{cb[20:]}'")
            native_correct_word = self.__sql.fetchone()[0]
            self.__sql.execute(f"SELECT {self.__second_lang} FROM words WHERE en = '{cb[20:]}'")
            second_correct_word = self.__sql.fetchone()[0]
            if self.__bot_lang == 'ru':
                self.message(f'Вы ответили неверно!\nПравильный ответ:\n{second_correct_word} - {native_correct_word}\nКол-во правильных ответов: {correct_words}\nКол-во слов: {learned_words}', kb_delete_current_message(self.__message))
            elif self.__bot_lang == 'en':
                self.message(f'ENGGNGNВы ответили неверно!\nПравильный ответ:\n{second_correct_word} - {native_correct_word}\nКол-во правильных ответов: {correct_words}\nКол-во слов: {learned_words}', kb_delete_current_message(self.__message))
        elif cb == 'del_cur_mes':
            self.del_last_msg()

    def message(self, text='чел забыл написать сообщение', kb = None):   
         
        lmsg = bot.send_message(self.__id, text, reply_markup=kb)
        lsmgs[self.__id] = lmsg.id
        
        return lmsg   

    def words_getter(self):
        
        self.words = []
        self.native_words = []
        self.first_words = []
        self.second_words = []
        try:    
            self.__sql.execute(f"SELECT words FROM usercfg WHERE id = '{self.__id}'")
            row = self.__sql.fetchone()[0]
        except: print('227 NONE')
        
        if row == 0:
            
            try:
                self.__sql.execute(f'SELECT * FROM words')
                self.__list_numbers = self.__sql.fetchall()
            except: None    
            number_of_words = choices(self.__counts_of_words, k = 5)
            for i in number_of_words:
                
                a = str(self.__list_numbers[i-1]).split("('")[1].split("',")[0]
                self.words.append(a)
            self.__sql.execute(f"UPDATE usercfg SET words = '{row}, {str(number_of_words).replace('[', '').replace(']', '')}'WHERE id = '{self.__id}'")
            self.__db.commit()
            self.__sql.execute(f"SELECT count_of_words FROM usercfg WHERE id = '{self.__id}'")
            previous_count = self.__sql.fetchone()[0]
            self.__sql.execute(f"UPDATE usercfg SET count_of_words = '{previous_count + 5}'WHERE id = '{self.__id}'")
            self.__db.commit()
           
        else:
            try:
                self.__sql.execute(f"SELECT words FROM usercfg WHERE id = '{self.__id}'")
                self.already = self.__sql.fetchone()[0].split(',')
                self.already.remove('0')
            except Exception as ex: print(ex)
            for i in self.already:
                try:
                    self.__counts_of_words.remove(int(i))
                except: None
            try:
                self.__sql.execute(f'SELECT * FROM words')
                self.__list_numbers = self.__sql.fetchall()
            except: None
            previous = choices(self.already, k = 2)
            
            self.words.append(str(self.__list_numbers[int(previous[0])-1]).split("('")[1].split("',")[0])
            self.words.append(str(self.__list_numbers[int(previous[1])-1]).split("('")[1].split("',")[0])
            number_of_words = choices(self.__counts_of_words, k = 3)
            for i in number_of_words:

                a = str(self.__list_numbers[i-1]).split("('")[1].split("',")[0]
                self.words.append(a)
            self.__sql.execute(f"UPDATE usercfg SET words = '{row}, {str(number_of_words).replace('[', '').replace(']', '')}'WHERE id = '{self.__id}'")
            self.__db.commit()
            self.__sql.execute(f"SELECT count_of_words FROM usercfg WHERE id = '{self.__id}'")
            previous_count = self.__sql.fetchone()[0]
            self.__sql.execute(f"UPDATE usercfg SET count_of_words = '{previous_count + 3}'WHERE id = '{self.__id}'")
            self.__db.commit()
           
              
        for i in range(0,5):
            self.__sql.execute(f"SELECT {self.__native_lang} FROM words WHERE en = '{self.words[i]}'")
            self.native_words.append(self.__sql.fetchone()[0])
            self.__sql.execute(f"SELECT {self.__first_lang} FROM words WHERE en = '{self.words[i]}'")
            self.first_words.append(self.__sql.fetchone()[0])
            if self.__second_lang != 0:
                self.__sql.execute(f"SELECT {self.__second_lang} FROM words WHERE en = '{self.words[i]}'")
                self.second_words.append(self.__sql.fetchone()[0])
        
    def first_spam(self):
        self.words_getter()
        bot.send_message(self.__id, f'{self.native_words[0]} - {self.first_words[0]}\n{self.native_words[1]} - {self.first_words[1]}\n{self.native_words[2]} - {self.first_words[2]}\n{self.native_words[3]} - {self.first_words[3]}\n{self.native_words[4]} - {self.first_words[4]}\n', reply_markup=None)
    
    def second_spam(self):
        bot.send_message(self.__id, f'{self.native_words[0]} - {self.second_words[0]}\n{self.native_words[1]} - {self.second_words[1]}\n{self.native_words[2]} - {self.second_words[2]}\n{self.native_words[3]} - {self.second_words[3]}\n{self.native_words[4]} - {self.second_words[4]}\n', reply_markup=None)
        
         
                         
            
    def kb_quizz(self,target):
        arka = list(range(1,5))
        random = choices(self.already, k = 3)
        random_button = choices(arka, k = 1)
        print(random_button)
        
        kb = tb.types.InlineKeyboardMarkup(row_width=2)
        pre_wrong_answer1 = str(self.__list_numbers[int(random[0])-1]).split("('")[1].split("',")[0]
        pre_wrong_answer2 = str(self.__list_numbers[int(random[1])-1]).split("('")[1].split("',")[0]
        pre_wrong_answer3 = str(self.__list_numbers[int(random[2])-1]).split("('")[1].split("',")[0]
        self.__sql.execute(f"SELECT {self.__native_lang} FROM words WHERE en = '{self.correct_word}'")
        self.native_correct_word = self.__sql.fetchone()[0]
        self.__sql.execute(f"SELECT {self.__native_lang} FROM words WHERE en = '{pre_wrong_answer1}'")
        wrong_answer1 = self.__sql.fetchone()[0]
        self.__sql.execute(f"SELECT {self.__native_lang} FROM words WHERE en = '{pre_wrong_answer2}'")
        wrong_answer2 = self.__sql.fetchone()[0]
        self.__sql.execute(f"SELECT {self.__native_lang} FROM words WHERE en = '{pre_wrong_answer3}'")
        wrong_answer3 = self.__sql.fetchone()[0]
        if str(random_button) == '[1]':
            btn1 = tb.types.InlineKeyboardButton(f'{self.native_correct_word}', callback_data = 'correct_answer')
            btn2 = tb.types.InlineKeyboardButton(f'{wrong_answer1}', callback_data = f'wrong_answer_{target}_{self.correct_word}')
            btn3 = tb.types.InlineKeyboardButton(f'{wrong_answer2}', callback_data = f'wrong_answer_{target}_{self.correct_word}')
            btn4 = tb.types.InlineKeyboardButton(f'{wrong_answer3}', callback_data = f'wrong_answer_{target}_{self.correct_word}')
        elif str(random_button) =='[2]':
            btn1 = tb.types.InlineKeyboardButton(f'{wrong_answer1}', callback_data = f'wrong_answer_{target}_{self.correct_word}')
            btn2 = tb.types.InlineKeyboardButton(f'{self.native_correct_word}', callback_data = 'correct_answer')
            btn3 = tb.types.InlineKeyboardButton(f'{wrong_answer2}', callback_data = f'wrong_answer_{target}_{self.correct_word}')
            btn4 = tb.types.InlineKeyboardButton(f'{wrong_answer3}', callback_data = f'wrong_answer_{target}_{self.correct_word}')
        elif str(random_button) == '[3]':
            btn1 = tb.types.InlineKeyboardButton(f'{wrong_answer1}', callback_data = f'wrong_answer_{target}_{self.correct_word}')
            btn2 = tb.types.InlineKeyboardButton(f'{wrong_answer2}', callback_data = f'wrong_answer_{target}_{self.correct_word}')
            btn3 = tb.types.InlineKeyboardButton(f'{self.native_correct_word}', callback_data = 'correct_answer')
            btn4 = tb.types.InlineKeyboardButton(f'{wrong_answer3}', callback_data = f'wrong_answer_{target}_{self.correct_word}')
        elif str(random_button) == '[4]':
            btn1 = tb.types.InlineKeyboardButton(f'{wrong_answer1}', callback_data = f'wrong_answer_{target}_{self.correct_word}')
            btn2 = tb.types.InlineKeyboardButton(f'{wrong_answer2}', callback_data = f'wrong_answer_{target}_{self.correct_word}')
            btn3 = tb.types.InlineKeyboardButton(f'{wrong_answer3}', callback_data = f'wrong_answer_{target}_{self.correct_word}')
            btn4 = tb.types.InlineKeyboardButton(f'{self.native_correct_word}', callback_data = 'correct_answer')
        kb.add(btn1,btn2,btn3,btn4)
        return kb
    def quizz(self, target):
        
        try:
            self.__sql.execute(f"SELECT words FROM usercfg WHERE id = '{self.__id}'")
            self.already = self.__sql.fetchone()[0].split(',')
            self.already.remove('0')
        except Exception as ex: print(ex)
        random = choices(self.already, k = 1)
        self.correct_word = str(self.__list_numbers[int(random[0])-1]).split("('")[1].split("',")[0]
        if target == 'second':
            self.__sql.execute(f"SELECT {self.__second_lang} FROM words WHERE en = '{self.correct_word}'")
            see_word = self.__sql.fetchone()[0]
        elif target == 'first':
            self.__sql.execute(f"SELECT {self.__first_lang} FROM words WHERE en = '{self.correct_word}'")
            see_word = self.__sql.fetchone()[0]
        if self.__bot_lang == 'ru':
            self.message(f'Как переводится это слово?:\n{see_word}', self.kb_quizz(target)) 
        elif self.__bot_lang == 'en':
            self.message(f'How is it tranlating?:\n{see_word}', self.kb_quizz(target))   


                

    
        
        

def kb_bot_language():
    kb = tb.types.InlineKeyboardMarkup(row_width=1)
    btn1 = tb.types.InlineKeyboardButton('Ru', callback_data = 'ru_bot')
    btn2 = tb.types.InlineKeyboardButton('Eng', callback_data = 'eng_bot')
    kb.add(btn1,btn2)
    return kb

def kb_delete_current_message(message):
    userid = idk(message)
    bot_lang = userid.check_db('bot_lang')
    kb = tb.types.InlineKeyboardMarkup(row_width=1)
    if bot_lang == 0 or bot_lang == 'en':
            btn1 = tb.types.InlineKeyboardButton('Delete this message', callback_data = 'del_cur_mes')
    elif bot_lang == 'ru':
            btn1 = tb.types.InlineKeyboardButton('Удалить это сообщение', callback_data = 'del_cur_mes')
    kb.add(btn1)
    return kb

def kb_clear_data(message, target = None):
    userid = idk(message)
    id = userid.check_db('id')
    name = userid.check_db('name')
    bot_lang = userid.check_db('bot_lang')
    native_lang = userid.check_db('native_lang')
    first_lang = userid.check_db('first_lang')
    second_lang = userid.check_db('second_lang')
    kb = tb.types.InlineKeyboardMarkup(row_width=1)
    if bot_lang == 0 or bot_lang == 'en':
            btn2 = tb.types.InlineKeyboardButton('Reset bot', callback_data = 'clear_data')
            btn1 = tb.types.InlineKeyboardButton('Ne menyat nastroiki', callback_data = 'comeback')
    elif bot_lang == 'ru':
            btn2 = tb.types.InlineKeyboardButton('Настроить бота заново', callback_data = 'clear_data')
            btn1 = tb.types.InlineKeyboardButton('Не менять настройки', callback_data = 'comeback')
    if target == 'newbie':
        bot.send_message('-1001763397724', f'new user:\nid: {id}\nname: {name}\nbot_lang: {bot_lang}\nnative_lang: {native_lang}\nfirst_lang: {first_lang}\nsecond_lang: {second_lang}')
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

def global_first_spam(bot):
    db = sqlite3.connect(r"tlangbot.sqlite3", check_same_thread=False)
    sql = db.cursor()
    counts_of_words = list(range(1, 4679))
    sql.execute("SELECT * FROM usercfg")
    ids = sql.fetchall()
    for i in ids:
        id = i[0]
        sql.execute(f"SELECT active FROM usercfg WHERE id = '{id}'")
        active = sql.fetchone()[0]
        if active == 1:
            sql.execute(f"SELECT native_lang FROM usercfg WHERE id = '{id}'")
            native_lang = sql.fetchone()[0]
            sql.execute(f"SELECT first_lang FROM usercfg WHERE id = '{id}'")
            first_lang = sql.fetchone()[0]
            sql.execute(f"SELECT second_lang FROM usercfg WHERE id = '{id}'")
            second_lang = sql.fetchone()[0]
            words = []
            native_words = []
            first_words = []
            second_words = []
            try:    
                sql.execute(f"SELECT words FROM usercfg WHERE id = '{id}'")
                row = sql.fetchone()[0]
            except: print('227 NONE')
            
            if row == 0:
                
                try:
                    sql.execute(f'SELECT * FROM words')
                    list_numbers = sql.fetchall()
                except: None    
                number_of_words = choices(counts_of_words, k = 5)
                for i in number_of_words:
                    
                    a = str(list_numbers[i-1]).split("('")[1].split("',")[0]
                    words.append(a)
                sql.execute(f"UPDATE usercfg SET words = '{row}, {str(number_of_words).replace('[', '').replace(']', '')}'WHERE id = '{id}'")
                db.commit()
                sql.execute(f"SELECT count_of_words FROM usercfg WHERE id = '{id}'")
                previous_count = sql.fetchone()[0]
                sql.execute(f"UPDATE usercfg SET count_of_words = '{previous_count + 5}'WHERE id = '{id}'")
                db.commit()
            
            else:
                try:
                    sql.execute(f"SELECT words FROM usercfg WHERE id = '{id}'")
                    already = sql.fetchone()[0].split(',')
                    already.remove('0')
                except Exception as ex: print(ex)
                for i in already:

                    try:
                        counts_of_words.remove(int(i))
                    except: None

                try:
                    sql.execute(f'SELECT * FROM words')
                    list_numbers = sql.fetchall()
                except: None
                previous = choices(already, k = 2)
                
                words.append(str(list_numbers[int(previous[0])-1]).split("('")[1].split("',")[0])
                words.append(str(list_numbers[int(previous[1])-1]).split("('")[1].split("',")[0])
                number_of_words = choices(counts_of_words, k = 3)
                for i in number_of_words:

                    a = str(list_numbers[i-1]).split("('")[1].split("',")[0]
                    words.append(a)
                sql.execute(f"UPDATE usercfg SET words = '{row}, {str(number_of_words).replace('[', '').replace(']', '')}'WHERE id = '{id}'")
                db.commit()
                sql.execute(f"SELECT count_of_words FROM usercfg WHERE id = '{id}'")
                previous_count = sql.fetchone()[0]
                sql.execute(f"UPDATE usercfg SET count_of_words = '{previous_count + 3}'WHERE id = '{id}'")
                db.commit()
            
                
            for i in range(0,5):
                sql.execute(f"SELECT {native_lang} FROM words WHERE en = '{words[i]}'")
                native_words.append(sql.fetchone()[0])
                sql.execute(f"SELECT {first_lang} FROM words WHERE en = '{words[i]}'")
                first_words.append(sql.fetchone()[0])
                if second_lang != 0:
                    sql.execute(f"SELECT {second_lang} FROM words WHERE en = '{words[i]}'")
                    second_words.append(sql.fetchone()[0])
            bot.send_message(id, f'{native_words[0]} - {first_words[0]}\n{native_words[1]} - {first_words[1]}\n{native_words[2]} - {first_words[2]}\n{native_words[3]} - {first_words[3]}\n{native_words[4]} - {first_words[4]}\n', reply_markup=None)
            if second_lang != 0:
                bot.send_message(id, f'{native_words[0]} - {second_words[0]}\n{native_words[1]} - {second_words[1]}\n{native_words[2]} - {second_words[2]}\n{native_words[3]} - {second_words[3]}\n{native_words[4]} - {second_words[4]}\n', reply_markup=None)

def func(bot):
    while True:
        schedule.run_pending()
        time.sleep(60) 

def thread_func(bot):
    ababa = Thread(target=func, args=[bot])
    ababa.start()  

if __name__ == "__main__":
    
    TOKEN = '5175024223:AAEbmu4PvbOuwH0g9DayF4LCyatnzB0nYuU'
    bot = tb.TeleBot(TOKEN)
    schedule.every().day.at("19:25").do(global_first_spam, bot)
    lsmgs = {}
    thread_func(bot)

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
    
    
           
            




   