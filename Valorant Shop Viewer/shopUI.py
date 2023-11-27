from tkinter import *
import customtkinter
import json
import urllib.request
from PIL import Image
import threading
from PIL import Image
import os
from valorantstore import ValorantStore
from time import sleep
from functools import partial
import webbrowser


with open('./config.json') as comptes:
  data = json.load(comptes)

def shopWindow(account,choice):
    # print("Choice = "+ choice)
    # print("account = " + account)

    shopFenetre = customtkinter.CTkToplevel(mainFenetre)
    shopFenetre.geometry("700x300")
    shopFenetre.minsize(width=700, height=300)
    shopFenetre.maxsize(width=700, height=300)
    shopFenetre.title(account["account"])
    valorant_store = ValorantStore(username=account["account"], password=account["password"], region="eu", sess_path=None, proxy=None)
    boutique = valorant_store.store(True)
    jsonboutique = json.loads(json.dumps(boutique))
    imageRef = []
    img_path = []
    for i in range(0,4):
        firstWP = jsonboutique["daily_offers"]["data"][i]
        skin = valorant_store.skin_info(firstWP["id"])
        image_url = firstWP["image"]
        img_path.append("./"+skin["displayName"].replace("/","")+".png")
        def download_image():
            urllib.request.urlretrieve(image_url, img_path[i])
            img = Image.open(img_path[i])
            img_width, img_height = img.size[0], img.size[1]
            img = img.resize((img_width//3, img_height//3))
            img.save(img_path[i])
        thread = threading.Thread(target=download_image)
        thread.start()
        thread.join()
        imageRef.append(PhotoImage(file=img_path[i]))
        imageLabel = customtkinter.CTkLabel(shopFenetre, image=imageRef[i], text= "")
        titre = customtkinter.CTkLabel(shopFenetre, text =skin["displayName"])
        imageLabel.grid(row=0,column=i)
        titre.grid(row=1,column=i)
        os.remove(img_path[i])
    mainloop()

def allShopWindow():
    bigShopping = customtkinter.CTkToplevel(mainFenetre)
    bigShopping.geometry("850x500")
    bigShopping.minsize(width=850, height=500)
    bigShopping.maxsize(width=850, height=500)
    bigShopping.grid_rowconfigure(0, weight=1)
    bigShopping.grid_columnconfigure(0, weight=1)
    bigShopping.title("Toutes les boutiques")
    frame = customtkinter.CTkScrollableFrame(master=bigShopping, width=500, height=700,border_color=("#ff0000"), border_width=1)
    for index,account in enumerate(data["compte"]):
        valorant_store = ValorantStore(username=account["account"], password=account["password"], region="eu", sess_path=None, proxy=None)
        boutique = valorant_store.store(True)
        jsonboutique = json.loads(json.dumps(boutique))
        imageRef = []
        img_path = []
        
        for i in range(0,4):
            firstWP = jsonboutique["daily_offers"]["data"][i]
            skin = valorant_store.skin_info(firstWP["id"])
            image_url = firstWP["image"]
            img_path.append("./"+skin["displayName"].replace("/","")+".png")
            def download_image():
                urllib.request.urlretrieve(image_url, img_path[i])
                img = Image.open(img_path[i])
                img_width, img_height = img.size[0], img.size[1]
                img = img.resize((img_width//3, img_height//3))
                img.save(img_path[i])
            thread = threading.Thread(target=download_image)
            thread.start()
            thread.join()
            imageRef.append(PhotoImage(file=img_path[i]))
            imageLabel = customtkinter.CTkLabel(frame, image=imageRef[i], text= "")
            titre = customtkinter.CTkLabel(frame, text =skin["displayName"])
            customtkinter.CTkLabel(frame, text="Shop de " + account["account"]).grid(row=index*3,columnspan=4)
            imageLabel.grid(row=(index*3)+1,column=i)
            titre.grid(row=(index*3)+2,column=i)


            os.remove(img_path[i])
    frame.grid(row=0,column=0,sticky="nsew")
    mainloop()

def exempleConfigFile(window):
    webbrowser.open('https://pastebin.com/vAs8eft2')

def selectAccount(window):
    nameCompte = []
    for widget in window.winfo_children(): 
        widget.destroy() 
    welcomePage = customtkinter.CTkLabel(window, text="Selectionne un compte").grid(row=0,column=0, columnspan=5)
    configExemple = customtkinter.CTkButton(window, text="Pas de compte?", command=partial(exempleConfigFile, window)).grid(row=1, column=1)
    for index, ligne in enumerate(data["compte"]):
        nameCompte.append(ligne["account"])
    customtkinter.CTkComboBox(window, values=nameCompte,command=partial(shopWindow, ligne)).grid(row=1, column=0)    
    customtkinter.CTkButton(window, command=allShopWindow, text="All Shop").grid(row=2, column=0)



mainFenetre = customtkinter.CTk()
customtkinter.set_appearance_mode("Dark")
mainFenetre.grid_rowconfigure(0, weight=1)
mainFenetre.grid_columnconfigure(0, weight=1)
customtkinter.CTkLabel(mainFenetre, text="Valorant Shop Viewer\n Made by SAPIFER").grid(row=0,column=0)
customtkinter.CTkButton(mainFenetre, text="Continuer", command=partial(selectAccount, mainFenetre)).grid(row=1, column=0)
mainFenetre.geometry("600x400")
mainFenetre.minsize(width=600, height=400)
mainFenetre.maxsize(width=600, height=400)
mainFenetre.title("SAPIFER's shop checker")
mainFenetre.mainloop()
