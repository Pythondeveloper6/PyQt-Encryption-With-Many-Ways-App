'''
    simple GUI to encrypt and decrypt with many algorithms
    developed by : Mahmoud Ahmed - pythondeveloper6@gmail.com

'''
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import os
from os import path
import time
import sqlite3
import math

FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"main.ui"))


Letter_to_index = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ",range(26)))
Index_to_letters = dict(zip(range(26),"ABCDEFGHIJKLMNOPQRSTUVWXYZ"))


class App_Window(QMainWindow , FORM_CLASS):
    def __init__(self):
        QMainWindow. __init__(self)
        self.setupUi(self)
        self.DB_Connect()
        self.Handel_Buttons()


    def DB_Connect(self):
        self.conection = sqlite3.connect('FDB.db')

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Add_Account_to_DB)
        self.pushButton_2.clicked.connect(self.Check_Ceaser)
        self.pushButton_5.clicked.connect(self.Check_Vigenere)
        self.pushButton_4.clicked.connect(self.Check_Row)



    def Add_Account_to_DB(self):
        username = self.lineEdit.text()
        password = self.lineEdit_3.text()
        ceaser_pass = self.Ceaser_Encrypt(password)
        vigenere_pass = self.Vigenere_Encrypt(password)
        row_pass = self.Row_Encrypt(password)

        self.conection.execute("INSERT INTO main(username,password,Ceaser_pass,Vigenere_pass,row_pass)"
                " VALUES(?,?,?,?,?)" , (username,password,ceaser_pass,vigenere_pass,row_pass))
        self.conection.commit()

    ########################################################################
    ##########################   CHECK CIPHER  #############################
    ########################################################################
    def Check_Ceaser(self):
        username = self.lineEdit_2.text()
        password = self.lineEdit_4.text()

        sql = "SELECT * From main WHERE username = ?"

        for row in self.conection.execute(sql ,[(username)]):
            real_pass = self.Ceaser_Decrypt(row[2])

            if real_pass == password.upper() :
                print('match')

            else:
                print('not match')



    def Check_Vigenere(self):
        username = self.lineEdit_10.text()
        password = self.lineEdit_9.text()

        sql = "SELECT * From main WHERE username = ?"

        for row in self.conection.execute(sql ,[(username)]):
            real_pass = self.Vigenere_Decrypt(row[3])

            if real_pass == password.upper() :
                print('match')

            else:
                print('not match')



    def Check_Row(self):
        username = self.lineEdit_8.text()
        password = self.lineEdit_7.text()

        sql = "SELECT * From main WHERE username = ?"

        for row in self.conection.execute(sql ,[(username)]):
            real_pass = self.Row_Decrypt(row[4])

            if real_pass == password :
                print('match')

            else:
                print('not match')


    ########################################################################
    ##########################  CEASER CIPHER  #############################
    ########################################################################
    def Ceaser_Encrypt(self , text):
        key = 4
        ciphertext = ""
        for c in text.upper():
            if c.isalpha():
                ciphertext += Index_to_letters[ (Letter_to_index[c] + key)%26 ]
            else:
                ciphertext += c
        print(ciphertext)
        return ciphertext




    def Ceaser_Decrypt(self , text):
        key= 4
        plaintext2 = ""
        for c in text.upper():
            if c.isalpha():
                plaintext2 += Index_to_letters[ (Letter_to_index[c] - key)%26 ]
            else:
                plaintext2 += c

        print(plaintext2)
        return plaintext2

    ########################################################################
    ############################  VIGENERE CIPHER ##########################
    ########################################################################
    def Vigenere_Encrypt(self , text):
        key = 'XPY'
        key_length = len(key)
        key_as_int = [ord(i) for i in key]
        plaintext_int = [ord(i) for i in text]
        ciphertext = ''
        for i in range(len(plaintext_int)):
            value = (plaintext_int[i] + key_as_int[i % key_length]) % 26
            ciphertext += chr(value + 65)
        print(ciphertext)
        return ciphertext


    def Vigenere_Decrypt(self , text):
        key = 'XPY'
        key_length = len(key)
        key_as_int = [ord(i) for i in key]
        ciphertext_int = [ord(i) for i in text]
        plaintext = ''
        for i in range(len(ciphertext_int)):
            value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
            plaintext += chr(value + 65)
        print(plaintext)
        return plaintext



    ########################################################################
    ##############################  ROW CIPHER  ############################
    ########################################################################
    def Row_Encrypt(self , text):
        key = 5
        ciphertext = [''] * key
        for col in range(key):
            pointer = col
            while pointer < len(text):
                ciphertext[col] += text[pointer]
                pointer += key

        print(''.join(ciphertext))
        return ''.join(ciphertext)

    def Row_Decrypt(self , text):
        key = 5
        numOfColumns = math.ceil(len(text) / key)
        numOfRows = key
        numOfShadedBoxes = (numOfColumns * numOfRows) - len(text)
        plaintext = [''] * numOfColumns
        col = 0
        row = 0
        for symbol in text:
            plaintext[col] += symbol
            col += 1
            if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
                col = 0
                row += 1
        print(''.join(plaintext))
        return ''.join(plaintext)




def main():
    app = QApplication(sys.argv)
    window = App_Window()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
