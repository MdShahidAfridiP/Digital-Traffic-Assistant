from django.db import models
import boto3
import mysql.connector
import requests
# Create your models here.
class destination:
    name:str
    desc :str
    location:str
    price:int
    imgs=str
    offer=bool

    def rekognition(self,image):
        access_key_id="//your access key"
        secret_access_key="//your secret access key"

        photo=image

        client=boto3.client('rekognition',
                            aws_access_key_id = access_key_id,
                            aws_secret_access_key = secret_access_key,
                            region_name='us-west-2')

        with open(photo,'rb') as source_image:
            source_bytes=source_image.read()

        response=client.detect_text(Image={'Bytes':source_bytes})
        #print(response)
        lists=[]
        str=""
        for i in range(0,2):
            lists.append(response["TextDetections"][i]["DetectedText"])
        lists=list(dict.fromkeys(lists))
        for i in range(len(lists)):
            str+=" "+lists[i]
        return str


    def dbmanager(self,query):
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="dbmsproject")
        mycursor = mydb.cursor()
        mycursor.execute(query)
        reslist=[]
        for i in mycursor:
            reslist=list(i)
        mycursor.execute("commit")
        return reslist

    def message(self, phone):
        url = "https://www.fast2sms.com/dev/bulk"
        msg=": \n you have been charged Rs:500/-  for parking in no parking zone, please remove your vehicle"
        payload = f"sender_id=FSTSMS&message={msg}&language=english&route=p&numbers={phone}"
        headers = {
            'authorization': "//auth code",
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
