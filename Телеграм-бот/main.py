import time
import requests
from bs4 import BeautifulSoup

import telebot
from telebot import types

TOKEN = secrets

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts


def get_teacher_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    teacher_name = soup.find('h1').text

    emails = soup.find_all('a', class_='mailto')
    email_list = [email.get('href').replace('mailto:', '') for email in emails]
    return teacher_name, email_list

def get_kaf_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Извлечение названия кафедры
    department_name_tag = soup.find('div', class_='title-h2')
    department_name = department_name_tag.h2.text if department_name_tag else 'Название не найдено'
    # Извлечение сайта кафедры
    department_site_tag = soup.find(
        lambda tag: tag.name == 'a' and 'href' in tag.attrs and 'ict.herzen.spb.ru' in tag['href'])
    department_site = department_site_tag['href'] if department_site_tag else 'Сайт не найден'
    # Извлечение email кафедры
    department_email_tag = soup.find(
        lambda tag: tag.name == 'a' and 'href' in tag.attrs and 'mailto:' in tag['href'])
    department_email = department_email_tag['href'].replace('mailto:',
                                                            '') \
        if department_email_tag else 'Email не найден'
    # Извлечение адреса кафедры
    department_address_tag = soup.find(
        lambda tag: tag.name == 'a' and 'href' in tag.attrs and 'maps' in tag['href'])
    department_address = department_address_tag.text if department_address_tag else 'Адрес не найден'

    return department_name, department_site, department_email, department_address


commands = {  # command description used in the "help" command
    'start'       : 'Начать использовать бот заново',
    'help'        : 'Посмотреть все команды',
    'ivt'       : 'Посмотри информацию по нашему курсу'
}

info = {
    'dean'             :  'Посмотри информацию о работе деканата',
    'disciplines'      :  'Список предметов, которые есть в этом семестре (+преподаватели ;))',
    'tutor'            :  'Информация о кураторе курса',
    'kaf'              :  'Информация о нашей кафедре ИТТЭО',
    'periods'          :  'Информация о сроках обучения, сессии и каникул'
}

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


hbjnmcd_bot = telebot.TeleBot('7152726739:AAH7vH7pTfn8sL9vmvJ1Czl6IqGmgkRRbUI')
hbjnmcd_bot.set_update_listener(listener)  # register listener


# handle the "/start" command
@hbjnmcd_bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:
        hbjnmcd_bot.send_message(cid, "Привет, это бот, который что-то умеет :)")
        hbjnmcd_bot.send_message(cid, "Вот что я могу:")
        command_help(m)  # show the new user the help page
    else:
        hbjnmcd_bot.send_message(cid, "Снова привет!")


# help page
@hbjnmcd_bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Вот что ты можешь посмотреть: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    hbjnmcd_bot.send_message(cid, help_text)  # send the generated help page


@hbjnmcd_bot.message_handler(commands=['ivt'])
def command_ivt(m):
    cid = m.chat.id
    info_text = "Ты можешь посмотреть следующую информацию:\n"
    for key in info:  # generate help text out of the commands dictionary defined at the top
        info_text += "/" + key + ": "
        info_text += info[key] + "\n"
    hbjnmcd_bot.send_message(cid, info_text)


@hbjnmcd_bot.message_handler(commands=['dean'])
def command_dean(m):
    cid = m.chat.id
    hbjnmcd_bot.send_message(cid, "Деканат обычно работает с 10 до 17 часов.")


@hbjnmcd_bot.message_handler(commands=['disciplines'])
def command_disciplines(m):
    cid = m.chat.id
    hbjnmcd_bot.send_message(cid, "Остался один экзамен по Сервервым и веб-технологиям")


@hbjnmcd_bot.message_handler(commands=['tutor'])
def command_tutor(m):
    cid = m.chat.id
    hbjnmcd_bot.send_message(cid,"Сейчас куратор нашего курса:\n")
    teacher_url = 'https://ict.herzen.spb.ru/department/employees/person/zhukov-n-n'
    teacher_name, email_list = get_teacher_info(teacher_url)
    emails = ', '.join(email_list)
    hbjnmcd_bot.send_message(cid,
                             f"ФИО преподавателя: {teacher_name}\n"
                             f"Электронная почта: {emails}\n"
                             f"Телеграм: @nzhukov")

@hbjnmcd_bot.message_handler(commands=['kaf'])
def command_kaf(m):
    cid = m.chat.id
    hbjnmcd_bot.send_message(cid,"Информация о кафедре:\n")
    kaf_url = 'https://www.herzen.spb.ru/about/struct-uni/inst/i-it/kafedry/kafedra-informatsionnykh-tekhnologiy-i-elektronnogo-obucheniya/'
    department_name, department_site, department_email, department_address = get_kaf_info(kaf_url)
    hbjnmcd_bot.send_message(cid,
                             f"Название: {department_name}\n"
                             f"Сайт: {department_site}\n"
                             f"Электронная почта: {department_email}\n"
                             f"Адрес: {department_address}")
    hbjnmcd_bot.send_message(cid, "Заведующая кафедрой:\n")
    teacher_url = 'https://ict.herzen.spb.ru/department/employees/person/vlasova-e-z'
    teacher_name, email_list = get_teacher_info(teacher_url)
    emails = ', '.join(email_list)
    hbjnmcd_bot.send_message(cid,
                             f"ФИО преподавателя: {teacher_name}\n"
                             f"Электронная почта: {emails}\n"
                             f"Телеграм: ищи в беседе https://t.me/ivt2022_2026")

@hbjnmcd_bot.message_handler(commands=['periods'])
def command_periods(m):
    cid = m.chat.id
    hbjnmcd_bot.send_message(cid, "Сейчас уже каникулы, ура-ура!")


# filter on a specific message
@hbjnmcd_bot.message_handler(func=lambda message: message.text == "Привет")
def command_text_hi(m):
    hbjnmcd_bot.send_message(m.chat.id, "Привет!")


# default handler for every other text
@hbjnmcd_bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    hbjnmcd_bot.send_message(m.chat.id, "Я не понимаю, что ты хочешь. \"" + m.text + "\"\nМожет тебе поможет это? /help")


hbjnmcd_bot.infinity_polling()
