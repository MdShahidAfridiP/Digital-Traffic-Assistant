from django.shortcuts import render
from .models import destination
# Create your views here.
noplate=""
personname=""
address=""
phone=""
gender=""
design=""
user=""
psswd=""
adno=""

def index(request):
    global user,psswd
    try:
        user=request.POST["username"]
        psswd=request.POST["password"]
        dest1=destination()
        dest2=destination()
        dest3=destination()

        dest1.location='Machine Learning'
        dest1.desc="Extract Text from Image"
        dest1.imgs="ml.png"

        dest2.location='Message Service'
        dest2.desc="sends Message to people"
        dest2.imgs="message.png"

        dest3.location='DataBase'
        dest3.desc="Retrive data from DataBase"
        dest3.imgs="database.jpg"
        query=f"select * from sign where username='{user}' and passwd='{psswd}'"
        str=dest1.dbmanager(query)
        if str[0]==user and str[1]==psswd:
            dests=[dest1,dest2,dest3]
            return render(request,"index.html",{'dests':dests})
        else:
            return render(request,"login.html",{'note':'Invalid username and password'})
    except Exception as e:
        return render(request,"login.html",{'note':'Invalid username and password'})

def result(request):
    global noplate,personname,address,phone,gender,noplate,adno
    try:
        dest=destination()
        vals=request.GET["urlimg"]
        res=dest.rekognition(vals)
        query1=f"select * from people where vehicle='{res}'"
        dbres1=dest.dbmanager(query1)
        #dest.message(dbres1[2])
        print(dbres1)
        personname,address,phone,gender,noplate,design,adno=dbres1[0],dbres1[1],dbres1[2],dbres1[3],dbres1[4],dbres1[5],dbres1[6]
        return render(request,"result.html",{'gennum':res,'personname':personname,'address':address,'phone':phone,'gender':gender,'vehicle':noplate,'desig':design})
    except Exception as e:
        return render(request,"result.html",{'gennum':e})

def more(request):
    global noplate
    query2=f"select * from vehicle where noplate='{noplate}'"
    print(query2)
    dest=destination()
    dbres2=dest.dbmanager(query2)
    print(dbres2)
    numplate,regdate,expdate,ownername,lastfine=dbres2[0],dbres2[1],dbres2[2],dbres2[3],dbres2[4]
    query3=f"select a.accno from people p,aadhar a where p.adno=a.adno and p.adno={adno}"
    dbres3=dest.dbmanager(query3)
    accno=dbres3[0]
    return render(request,"more.html",{'noplate':numplate,'regdate':regdate,'expdate':expdate,'owner':ownername,'lastfine':lastfine,'adno':adno,'accno':accno})

def msg(request):
    query=f"select accno from aadhar,people where aadhar.adno=people.adno and vehicle='{noplate}'"
    dest=destination()
    dbres=dest.dbmanager(query)
    if dbres[0]==None:
        return render(request,"index.html",{'note':'Transaction Failed Due to insufficient balance'})
    import datetime
    t=datetime.date.today()
    query3=f"update vehicle set lastfine='{t}' where noplate='{noplate}'"
    dest=destination()
    dest.dbmanager(query3)
    dest.message(phone)
    return render(request,"index.html",{'note':'Fine has Been Successfully charged.'})

def login(request):
    return render(request,"login.html")