import urllib2
import time
import os
import json
import getPDF
import MultipartPostHandler

INTERVAL = 3
URL = 'https://api.telegram.org/bot'
TOKEN = '126922068:AAEzCd4jLc3vqrCEahi6VhdSSoO5dnc3xtc'
offset=0

def check_updates():


    proxy = urllib2.ProxyHandler({'https': 'https://nakberov:hemongoo@proxy.ksu.ru:8080'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    up_data = json.load(urllib2.urlopen(URL + TOKEN + '/getUpdates'))


    if len(up_data["result"]) != 0:
        for elem in up_data["result"]:
            offset = elem["update_id"]+1
            text = elem["message"]["text"]
            chat_id = elem["message"]["chat"]["id"]
            run_command(chat_id,text)
            urllib2.urlopen(URL + TOKEN + '/getUpdates?offset='+str(offset))
            print(chat_id,text)

def run_command(chat_id,text):
    if "/getHabr" in text:
        proxy = urllib2.ProxyHandler({'https': 'https://nakberov:hemongoo@proxy.ksu.ru:8080'})
        opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler,proxy)
        urllib2.install_opener(opener)
        if len(text.split(" ")) > 1:
            data = {"chat_id":str(chat_id),"text":"Create PDF"}
            opener.open(URL + TOKEN + '/sendMessage',data)
            
            link = getPDF.getPDF(text.split(" ")[-1])


            data = {"chat_id":str(chat_id),"text":"Upload file"}
            opener.open(URL + TOKEN + '/sendMessage',data)
            data = {"chat_id":str(chat_id),"document":open(link,"rb")}
            opener.open(URL + TOKEN + '/sendDocument',data)
            os.remove(link)
        else:
            data = {"chat_id":str(chat_id),"text":"Null link"}
            opener.open(URL + TOKEN + '/sendMessage',data)

while True:
    time.sleep(INTERVAL)
    check_updates()

