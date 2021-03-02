#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
from tkinter import *
import threading




list = []
def save_info():
    grad_info = grad.get()
    ulica_info = ulica.get()
    broj_info = broj.get()
    #broj_info = str(broj_info)

    grad_entry.insert(INSERT, grad_info)
    ulica_entry.insert(INSERT, ulica_info)
    broj_entry.insert(INSERT, broj_info)
    adresa = grad_info, ulica_info, broj_info
    list.append(adresa)
    grad_entry.delete(0, END)
    ulica_entry.delete(0, END)
    broj_entry.delete(0, END)
    return list

def A1():
    print("Obrada u tijeku...")
    def close_window():
        screen.destroy()

    List=[]
    for item in save_info():
        #options = Options()
        #options.add_argument("--headless")
        #driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver = webdriver.Chrome(ChromeDriverManager().install())  # ,options=options)
        driver.get("https://www.a1.hr/INTERSHOP/web/WFS/A1-Shop-Site/hr_HR/a1-fixed/HRK/ViewRequisitionAvailability-View")

        #grad=driver.find_element_by_id('TechnologyAvailabilityForm_mjesto')
        #sleep(1)
        grad=WebDriverWait(driver, 20).until(
          EC.element_to_be_clickable((By.ID, 'TechnologyAvailabilityForm_mjesto')))
        try:
            for character in item[0]:
                grad.send_keys(character)
                sleep(0.3) # pause for 0.3 seconds
            grad.send_keys(Keys.RETURN)
            sleep(0.5)
        except:
            pass
        ulica = driver.find_element_by_id('TechnologyAvailabilityForm_Street')
        sleep(1)
        try:
            for character in item[1]:
                ulica.send_keys(character)
                sleep(0.1) # pause for 0.3 seconds
        except:
            pass
        try:
            ulica.send_keys(Keys.RETURN)
            sleep(0.5)
        except:
            pass
        #ulica.send_keys(item[1])
        #sleep(0.5)
        broj = driver.find_element_by_id('TechnologyAvailabilityForm_StreetNumber')
        try:
            broj.send_keys(item[2])
            sleep(0.5)
            broj.send_keys(Keys.RETURN)
            sleep(2)
        except:
            pass
        #try:
        #    sign_in = driver.find_element_by_xpath('//*[@id="AvailabilityForm"]/fieldset[2]/div[3]/button').click()
        #    sleep(3)
        #except:
        #    pass

        data = {}
        if driver.current_url == "https://www.a1.hr/dostupnost/flatbox":
            #sleep(1)
            flatbox = str(item)
            try:
                data["Flatbox"] = flatbox
            except:
                pass
        else:
            pass
        if driver.current_url == "https://www.a1.hr/dostupnost/none":
            #sleep(1)
            paketi = str(item)
            try:
                data["A1_paketi"] = paketi
            except:
                pass
        else:
            pass
        try:
            if driver.find_element_by_xpath('//*[contains(.,"Kabelske")]'):
                sleep(1)
                kablovska = str(item)
                try:
                    data['Kablovska'] = kablovska
                except:
                    pass
            else:
                pass
        except:
            pass
        try:
            if driver.find_element_by_xpath('//*[contains(.,"Optičke")]'):
                sleep(1)
                optika = str(item)
                try:
                    data['Optika'] = optika
                except:
                    pass
            else:
                pass
        except:
            pass

        List.append(data)
        print(data)
        driver.quit()
    df = pd.DataFrame(List)
    df.to_excel("A1_usluge.xlsx", index=False)
    # df.to_csv("A1_usluge.csv", index=False)
    print("Obrada završena")
    close_window()
    return List

screen = Tk()
screen.geometry("500x500")
screen.title("Python Form")
heading = Label(text="Unos podataka", bg="grey", fg="black", width="500", height="3")
heading.pack()

grad_text = Label(text="Grad * ", )
ulica_text = Label(text="Ulica * ", )
broj_text = Label(text="Broj * ", )
grad_text.place(x=15, y=70)
ulica_text.place(x=15, y=140)
broj_text.place(x=15, y=210)

grad = StringVar()
ulica = StringVar()
broj = StringVar()

grad_entry = Entry(textvariable=grad, width="30")
ulica_entry = Entry(textvariable=ulica, width="30")
broj_entry = Entry(textvariable=broj, width="30")

grad_entry.place(x=15, y=100)
ulica_entry.place(x=15, y=180)
broj_entry.place(x=15, y=240)

register1 = Button(screen, text="Unesi novu adresu", width="30", height="2", command=save_info, bg="grey")
register1.place(x=15, y=290)

register2 = Button(screen, text="Dostupnost A1-usluge", width="30", height="2", command=lambda: threading.Thread(target=A1).start(), bg="grey")
#register2 = Button(screen, text="Dostupnost A1-usluge", width="30", height="2", command=A1, bg="grey")
register2.place(x=15, y=350)

#register3 = Button(screen, text="Izlaz", width="30", height="2", command=close_window, bg="grey")
#register3.place(x=15, y=410)


screen = mainloop()




