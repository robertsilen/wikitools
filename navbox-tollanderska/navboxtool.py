import pyperclip
import mwclient
import re
import time
from datetime import datetime
import webbrowser

#a = "Linus Torvalds"
path = "/Users/robertsilen/Python/Roberts-Wikiverktyg/tollander/"
input1 = "tollander.txt"
input2 = "tollander2.txt"
input3 = "mauritz.txt"
input4 = "mauritz2.txt"
output = "tollander-output.txt"
input = input3

lang = "sv"
username = "Robertsilen" # sätt användarnament för botten här
password = open(path+"password.txt", "r").read() # Mitt lösenord är i denna fil och därför finns inte filen på Github
site = mwclient.Site(lang + ".wikipedia.org")
site.login(username, password) 
# summar defined in function
edit_summary = ""


def readfile(fullpath):
    file = open(fullpath, "r")
    data = file.read()
    rows = data.split("\n")
    datalist = []
    for row in rows:
        datalist.append(row.split("\t"))
    file.close()
    return datalist

def createnav(datalist):
    r = ""
    s = ""
    s +="{{Navbox\n"
    s +="| innhållsklass = \n"
    #s +="|title = [[Tollanderska priset]]\n"
    #s +="| name = Tollanderska priset\n"
    s +="|title = [[Statsrådet Mauritz Hallbergs pris]] av [[Svenska litteratursällskapet i Finland]]\n"
    s +="| name = Statsrådet Mauritz Hallbergs pris\n"
    s +="| state = {{{state<includeonly>|collapsed</includeonly>}}}\n"
    s +="| evenodd = on"
    categorylist = []
    i = 0
    for x in range(1920,2030,20) : 
        i += 1
        start = x
        end = x+20-1
        s += f"\n|group{i}  = {start}-{end}\n|list{i} = "
        for c, data in enumerate(datalist) : 
            if int(data[0])>=start and int(data[0])<=end : 
                s += f"{data[0]}:"
                data[1] = data[1].replace(" och",",")
                items = data[1].split(", ")
                for index, item in enumerate(items) : 
                    s += f" [[{item}]]"
                    r += f"{item}\n"
                    if index < len(items)-1 : 
                        s += f","
                s +="{{·}} "

    s += "\n}}<noinclude>"
    s += "\n[[Kategori:Vetenskapspriser]]"
    s += "\n</noinclude>"
    s = s.replace("{{·}} \n","\n")
    return s,r

def insert_text(string, index, key):
    return string[:index] + key + string[index:]

def addnavruta(datalist) : 
    #edit_summary = "Lägger till navruta för Tollanderska priset"
    edit_summary = "Lägger till navruta för Statsrådet Mauritz Hallbergs pris"
    add = "{{Statsrådet Mauritz Hallbergs pris}}"
    counter = 0
    found = 0
    edited = 0

    for index, cur in enumerate(datalist) : 
        #print(cur)
        counter += 1
        keys = ["{{[A,a]uktoritetsdata}}","{{STANDARDSORTERING","{{DEFAULT"]
        page = site.pages[cur]
        if page.exists :
            found += 1
            article_text = page.text()
            match1 = re.search(add,article_text)
            if match1 :
                start = match1.span(0)[0]
                print(f"{cur}, {start}: mall found")
            if not match1 :
                print(f"{cur}, mall not found, adding")
                start = 10000000
                for key in keys : 
                    match = re.search(key,article_text)
                    if match :
                        if match.span(0)[0]<start : 
                            start = match.span(0)[0]
                            #print(f"found {key} at {start}")
                article_text = insert_text(article_text,start,"\n"+add+"\n")
                print(article_text)
                page.edit(article_text, edit_summary)
                print(f"{cur}, mall added")
                webbrowser.open("https://sv.wikipedia.org/wiki/"+cur[0])
                time.sleep(9)

def addcat(datalist) : 
    edit_summary = "Lägger till kategori Mottagare av Statsrådet Mauritz Hallbergs pris"
    add = "[[Kategori:Mottagare av Statsrådet Mauritz Hallbergs pris]]"
    keys = "\[\[Kategori.*\]\]"
    counter = 0
    found = 0
    edited = 0

    for index, cur in enumerate(datalist) : 
        #print(cur)
        counter += 1
        page = site.pages[cur]
        if page.exists :
            found += 1
            article_text = page.text()
            match1 = re.search(add.replace("[","\["),article_text)
            if match1 :
                start = match1.span(0)[0]
                print(f"{cur}, {start}, {add} found")
            if not match1 :
                print(f"{cur}, {add} not found, adding")
                index = 0
                value = ""
                for match in re.finditer(keys,article_text) :
                    index = match.end()
                    value = match.group()
                article_text = insert_text(article_text,index,"\n"+add+"\n")
                #print(article_text)
                page.edit(article_text, edit_summary)
                print(f"{cur}, added {add}")
                webbrowser.open("https://sv.wikipedia.org/wiki/"+cur[0])
                time.sleep(9)

def addinfobox(datalist) : 
    edit_summary = "Lägger till infobox Faktamall biografi WD"
    add = "{{Faktamall biografi WD}}"
    skip = "\{\{[F|f]aktamall biografi WD|\{\{[F|f]örfattare|\{\{[Ö|ö]versättare"
    flag = "\[\[File:"
    keys = ""
    counter = 0
    found = 0
    edited = 0

    for index, cur in enumerate(datalist) : 
        #print(cur)
        counter += 1
        page = site.pages[cur]
        if page.exists :
            found += 1
            article_text = page.text()
            match1 = re.search(skip,article_text)
            if match1 :
                start = match1.span(0)[0]
                print(f"{cur}, {start}, found: {skip}")
            if not match1 :
                print(f"{cur}, {add} not found, adding")
                index = 0
                article_text = insert_text(article_text,index,add+"\n")
                print(article_text)
                page.edit(article_text, edit_summary)
                print(f"{cur}, added {add}")
                webbrowser.open("https://sv.wikipedia.org/wiki/"+cur[0])
                time.sleep(15)


## Read list of articles to work on
#datalist = readfile(path+input2)
datalist = readfile(path+input)

## Create navruta to articles before auktoritetsdata and standardordning
navruta,list = createnav(datalist)
print(navruta)
#pyperclip.copy(navruta)
#print(list)

## Add navruta 
#addnavruta(datalist)

## Add category to articles as last category
#addcat(datalist)
## Add Wikidata infobox to beginning
#addinfobox(datalist)

## handy to copy to clipboard
#pyperclip.copy(r)
