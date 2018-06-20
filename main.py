from Tkinter import *
from PIL import ImageGrab
from googleapiclient.discovery import build
import pytesseract
import webbrowser

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
api_key = # insert api key
search_engine_id = # insert search engine id
bot_lang = 'eng'
service = build("customsearch", "v1", developerKey = api_key)

def capture_qa():
    img = ImageGrab.grab(bbox=(35,170,388,280))
    query = pytesseract.image_to_string(img, lang = bot_lang).lower()
    query = query.replace("\n", " ").replace("?", "").replace('"', "").replace("'", "").replace(",", "")

    # if not questions
    if query.find('not') >= 0:
        query = query.replace('not', '').replace('  ', ' ')

    print query

    img = ImageGrab.grab(bbox=(60,327,315,383))
    img2 = ImageGrab.grab(bbox=(60,404,315,459))
    img3 = ImageGrab.grab(bbox=(60,480,315,537))
    
    answer1 = pytesseract.image_to_string(img, lang = bot_lang).lower()
    answer2 = pytesseract.image_to_string(img2, lang = bot_lang).lower()
    answer3 = pytesseract.image_to_string(img3, lang = bot_lang).lower()
    
    # split for search method
    split1 =  answer1.split(' ')
    split2 =  answer2.split(' ')
    split3 =  answer3.split(' ')
    
    print answer1
    print answer2
    print answer3

    ans1Counter = 0
    ans2Counter = 0
    ans3Counter = 0
    
    webbrowser.open("http://google.com/?#q=" + query)

    res = service.cse().list(q=query,cx=search_engine_id,).execute()

    for item in res['items']:
        for word in split1:
            if word in item['snippet'].lower():
                ans1Counter += 1
            if word in item['title'].lower():
                ans1Counter += 1
                
    for item in res['items']:
        for word in split2:
            if word in item['snippet'].lower():
                ans2Counter += 1
            if word in item['title'].lower():
                ans2Counter += 1

    for item in res['items']:
        for word in split3:
            if word in item['snippet'].lower():
                ans3Counter += 1
            if word in item['title'].lower():
                ans3Counter += 1

    print str(ans1Counter) + ' | ' + str(ans2Counter) + ' | ' + str(ans3Counter)

    answer = max(ans1Counter, ans2Counter, ans3Counter)

    if answer == ans1Counter:
        print 'The most probable answer is: ' + answer1
    elif answer == ans2Counter:
        print 'The most probable answer is: ' + answer2
    elif answer == ans3Counter:
        print 'The most probable answer is: ' + answer3
        
class MainApp:
    def __init__(self, master):
        self.read_button = Button(master, text="Read Question", command= lambda: capture_qa())
        self.read_button.pack(side=LEFT)
        
if __name__ == '__main__':
    root = Tk()
    a = MainApp(root)
    root.mainloop()
