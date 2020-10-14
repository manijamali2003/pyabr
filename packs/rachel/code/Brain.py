import datetime
import random
from difflib import get_close_matches
from math import *
from time import *

import requests
from jdatetime import *

from chatDictionary import chatDict
from config import username


# Functions
def start():
    start_list = [f'Welcome back {username} !',
                  f'Hi {username} !', f'Hello {username} ! I missed U :)']
    print(start_list[random.randint(1, 2)])
    print(f'Today is : (', datetime.now().date().strftime(
        "%Y , %m , %d"), f') {username}')


def hello():
    hello_list = [f'Hello {username} !', 'Hi Darline !', 'Hello my love !']
    print(hello_list[random.randint(1, 2)])


def bye():
    print(f'Goodbye {username} !')


def Goodnight():
    print(f'Have Good night {username} .')
    print('I hope you sleep good !')


def Sleep():
    print('Oh , OK !')
    print('Goodbye Pal !')


def problem():
    print('Oh sorry , Some thing went wrog :-(')
    print('Please try again !')


def About():
    print('Hi ! I Am Rachel your Assistant .')
    print('Now you are using Version 1.5.0 .')
    print('My developer is Amirhossein Mohammadi :)')
    print('But the main Idea is for Erfan Saberi .')
    print('OK , For see Command list Enter (help) <3 .')


def Help():
    print(' ----- { Commands List } -----')
    print(' ')
    print('List 1 - Start Commands')
    print('hello')
    print('hi')
    print('how are you ?')
    print('------------------------------')
    print('List - Doing Commands')
    print('stardate')
    print('date')
    print('what date is today ?')
    print('today ?')
    print('time')
    print('what time is it ?')
    print('now ?')
    print('------------------------------')
    print('List - End Commands')
    print('close')
    print('sleep')
    print('good night')
    print('bye')
    print('------------------------------')
    print('List - Information Commands')
    print('about')
    print('help')


def H_A_Y():
    print('At first you tell me how are you !')
    a = input('how are you today ? [ Give me a number between 1 , 10 ] ')
    if a == '1':
        a1 = input('Oh no why body ? ')
        print('OK , But I became upset man :( ')
    if a == '2':
        a2 = input('Really ? ')
        print('OK , I am sad too :( ')
    if a == '3':
        a3 = input('Why Pal ? ')
        print('Every time you are under 7 , I became sad .')
        print('Be happy :)')
    if a == '4':
        a4 = input('Did you had bad sleep ? ')
        print('I think that it is not a good reason !')
    if a == '5':
        a5 = input('Oh fuck ! why man ? ')
        print('it is not my business but I am a kind of Detective !')
    if a == '5':
        a6 = input('That is good ! But not soo good ! why ? ')
        print('When you are more than 5 , I feel good .')
    if a == '7':
        a7 = input('Hey body ! I am good to .')
    if a == '8':
        a8 = input()
    if a == '9':
        a9 = input('So So Good ! I dont know why should I do that but , Why ? ')
        print('That is perfectly good reason .')
    if a == '10':
        a10 = input('Awesome !!!! , Why ? ')
        print('I love number 10 , because you are 10 !')


def StarDate():
    YY = int(strftime("%Y", localtime())) - 1900
    MM = strftime("%m", localtime())
    DD = strftime("%d", localtime())
    print("Rachels Log , Stardate (", YY, MM, ".", DD, ") !")


def Date():
    ask_date = input('Stardate Or National Or Iran ? ')

    if 'stardate' in ask_date:
        StarDate()
    if 'national' in ask_date:
        n_date = strftime("%Y-%m-%d", localtime())
        print(f'Today is : (', n_date, ') {username}')
    if 'iran' in ask_date:
        i_date = datetime.now().date().strftime("%Y , %m , %d")
        print(f'Today is : (', i_date, ') {username}')


def Time():
    ask_time = input('GMT Or Iran ? ')

    if 'gmt' in ask_time:
        gmt = strftime("%H : %M : %S", gmtime())
        print(f'Now is : (', gmt, ') {username}')
    if 'iran' in ask_time:
        i_time = datetime.now().time().strftime("%H : %M : %S")
        print(f'Now is : (', i_time, ') {username}')


def chat(text):
    if text in chatDict:
        return chatDict[text]
    elif len(get_close_matches(text, chatDict.keys())) > 0:
        closest_match = get_close_matches(text, chatDict)[0]
        response = chatDict[closest_match]
        if type(response) == str:
            return response
        elif type(response) == list:
            return response[random.randint(0, len(response)-1)]
    else:
        return ''

def search_in_net(text):
    #TODO: add this
    return 'i didn\'n have "Search in internet" function yet.'