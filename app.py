from flask import Flask,render_template,url_for,jsonify,request,redirect,make_response
import json
import requests
from bs4 import BeautifulSoup
import random
from datetime import date
from flask_babel import Babel,_
import os
app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE']='az'
babel=Babel(app)
@babel.localeselector
def get_local():
    lang=request.cookies.get('language')
    if lang=="en":
        return 'en'
    elif lang=='ru':
        return 'ru'
    elif lang=='tr':
        return 'tr'
    elif lang=='az':
        return "az"
    else:
        return request.accept_languages.best_match(["en","ru","tr","az"])

def getObject():
     with open("cars.json","r") as file:
            data=file.read()
            file.close()
            obyekt=json.loads(data)
            return obyekt
def saveMoney(moneys):
    with open("static/currency/currency.json","w") as file:
        json.dump(moneys,file)
def work():
    soup = BeautifulSoup(requests.get("http://www.mezenne.az/").content, "html.parser")
    trler = soup.findAll('tr', style="white-space: nowrap;")
    moneyList = []
    for i in trler:
        children = i.findChildren("td", recursive=False)
        pulVahidininAdi = str(children[2]).replace("<td>", "").replace("</td>", "")
        deyer = str(children[3])
        deyerFrom = deyer.find('placeholder="')
        deyer = deyer[deyerFrom + 13:]
        last = deyer.find('"')
        deyer = deyer[:last]
        moneyList.append([pulVahidininAdi, deyer])
    saveMoney(moneyList)
def getCurrency():
    try:
         with open("static/currency/currency.json","r") as file:
            data=file.read()
            file.close()
            obyekt=json.loads(data)
            return obyekt   
    except Exception as ex:
        print(ex)
        result=getCurrency()
        return result
@app.errorhandler(404)
def error404(error):
    return render_template("404.html")
@app.errorhandler(500)
def error500(error):
    return render_template("404.html")
@app.errorhandler(403)
def error500(error):
    return render_template("404.html")
@app.route("/cars")
def cars():
    pullar=getCurrency()
    with open("cars.json","r") as file:
        data=file.read()
    obyekt=json.loads(data)
    return render_template("cars.html",cars=obyekt,moneys=pullar)
@app.route("/about")
def about():
    pullar=getCurrency()
    return render_template("about.html",moneys=pullar)    
@app.route("/changemoney/<string:currency>")
def changemoney(currency):
    work()
    return redirect(url_for("index"))
@app.route("/car/<int:id>")
def car(id):
    pullar=getCurrency()
    with open("cars.json","r") as file:
        data=file.read()
        file.close()
    obyekt=json.loads(data)
    return render_template("car.html",id=id,cars=obyekt,moneys=pullar) 
    
def dataNowDays(picked):
    pick=str(picked).split("-")
    pickk=[]
    try:
        for i in pick:    
            i=i.replace(" ","")
            pickk.append(int(i))
        pick=date(pickk[0],pickk[1],pickk[2])
        today=date.today()
        today=str(today).split("-")
        todayy=[]
        for i in today:
            i=i.replace(" ","")
            
            todayy.append(int(i))
        print(todayy,"seseseseasease")
        fromToday=pick-date(todayy[0],todayy[1],todayy[2])
        print(fromToday,"seseseseasease")

        try:
            fromToday=int(str(fromToday).split(",")[0].strip("days"))
        except Exception as ex:
            print(ex,"""
               try:
            fromToday=int(str(fromToday).split(",")[0].strip("days"))
        except Exception as ex:
            """)
            fromToday=1
        if fromToday<0:
            return True
        
    except Exception as ex:
        print(ex)
        return True
    return False
    
def totalDays(droped,picked):
    drop=str(droped).split("-")
    pick=str(picked).split("-")
    dropp=[]
    for i in drop:
        dropp.append(int(i))
    pickk=[]
    for i in pick:
        pickk.append(int(i))
    drop=date(dropp[0],dropp[1],dropp[2])
    pick=date(pickk[0],pickk[1],pickk[2])
    days=drop-pick
    days=str(days).split(",")
    days=days[0]
    days=days.strip("days")
    numberDays=int(days)
    return numberDays
def cheking(pick,drop):
    total=str(pick)+str(drop)
    print(total)
    if dataNowDays(pick):
        return "Informasiya yanlis daxil edilib",False
    elif str(pick)==str(drop):
        return "Goturulme tarixi ve buraxilma tarixi eyni ola bilmez",False
    elif len(total)<19:
        return "Goturulme tarixi ve ya buraxilma tarixi daxil edilmeyib",False
    elif totalDays(drop,pick)<0:
        return "Buraxilma tarixi Goturulme tarixinden tezdir",False
    return "",True

def calPrice(pick,drop,baby,id,carss):
    totalPrice=0
    numberDays=totalDays(drop,pick)
    
    for car in carss:
        if car['id']==id:
            if numberDays<4:
                totalPrice+=numberDays*car['days']['2_3']
            elif numberDays<8:
                totalPrice+=numberDays*car['days']['4_7']
            elif numberDays<16:
                totalPrice+=numberDays*car['days']['8_15']
            elif numberDays<30:
                totalPrice+=numberDays*car['days']['16_30']
            elif numberDays>=30:
                totalPrice+=numberDays*car['days']['30_']
    if "0"!=str(baby):
        totalPrice+=30
        return totalPrice,numberDays,True
    return totalPrice,numberDays,False
    
@app.route("/calc/<int:id>",methods=["POST"])
def calc(id):
    pullar=getCurrency()
    if request.method=="POST":
        pick=request.form.get('pick')
        drop=request.form.get('drop')
        baby=request.form.get('baby')
        obyekt=getObject()
        res = cheking(pick,drop)
        if res[1] is False:
            error=res[0]
            return render_template("car.html",id=id,cars=obyekt,moneys=pullar,error=error)
        else:
            totalPrice,totalDays,totalBaby=calPrice(pick,drop,baby,id,obyekt) 
            return render_template("car.html",id=id,cars=obyekt,moneys=pullar,totalPrice=totalPrice,totalDays=totalDays,totalBaby=totalBaby) 
        return render_template("car.html",id=id,cars=obyekt) 
        
    return render_template("404.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/wewillcallyou/<int:carid>/<int:totalprice>/",methods=["POST"])
def wewillcallyou(carid,totalPrice):
    pullar=getCurrency()
    if request.method=="POST":
        name=request.form.get('name')
        mail=request.form.get('mail')
        phone=request.form.get('phone')
        obyekt=getObject()
        # return  render_template("cars.html",cars=obyekt,moneys=pullar,callyou=True)
        return "{}{}{}{}{}".format(name,mail,phone,carid,totalPrice)
    return render_template("404.html")
@app.route("/")
def index():
    pullar=getCurrency()
    obyekt=getObject()
    aCar=random.randint(1,len(obyekt))
    print("random a car",aCar)
    return render_template("index.html",cars=obyekt,moneys=pullar,aCar=aCar)

@app.route("/currency")
def getcur():
    result=getCurrency()
    return jsonify(result)
if __name__=="__main__":
    app.run(port=5050,debug=True,host='127.0.0.2')