import requests
#pip install requests
import time
import shutil
import pytesseract
import argparse
import cv2
import random
import mysql.connector
import os
import qrcode
import datetime
import pytz

pytesseract.pytesseract.tesseract_cmd = r"full path to the exe file"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

chars = 'CDHKPQRVXY'
nums =  '123456789'
total = 10
rndstr = [1,2,3,4,5,6,7]
rndint = [1,2,3,4,5,6,7]
random.choice(rndstr)
random.choice(rndint)

for i in range(total):
    selects = random.sample(chars, random.choice(rndstr)) + random.sample(nums, random.choice(rndint))
    random.shuffle(selects)
    unique_code = ''.join(selects)
    fixbarcode = (unique_code)
    fixrandom = f'{unique_code}.png'

print(type(round(time.time()*1000)))


url='http://192.168.100.63'
milli = round(time.time()*1000)
print (milli)

r = requests.get(f'{url}/capture?_cb={int(round(time.time() * 1000))}', stream=True)
print (r.status_code)

r = requests.get(f'{url}/capture?_cb={int(round(time.time() * 1000))}', stream=True)
dir_name = 'gambar/'
suffix = '.png'
fixgambar = os.path.join(dir_name, unique_code + suffix)
with open (fixgambar,'wb') as out_file:
    shutil.copyfileobj(r.raw, out_file)
  
image = cv2.imread(fixgambar)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# use Tesseract to OCR the image
text = pytesseract.image_to_string(image, config='--psm 11')
print(text)

img = qrcode.make(fixbarcode)

folder_name = 'barcode/'
ext = '.png'
fixqr = os.path.join(folder_name, unique_code + ext)
now_utc = pytz.utc.localize(datetime.datetime.now())
now_asia = now_utc.astimezone(pytz.timezone('Asia/Jakarta'))
img.save(fixqr)


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="read_text"
)

mycursor = mydb.cursor()

sql = "INSERT INTO tnkb (nomor_tnkb, barcode, fototnkb, fotoqr,jam_keluar) VALUES (%s,%s,%s,%s,%s)"
val = (text,fixbarcode,fixrandom,fixrandom,now_asia.strftime('%Y-%m-%d %H:%M:%S'))
mycursor.execute(sql, val)

mydb.commit()