import requests
from bs4 import BeautifulSoup
import json
import datetime
def saveMoney(moneys):
    with open("currency.json","w") as file:
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


if __name__=="__main__":
    while True:
    # minute = datetime.datetime.now().minute
    # hour = datetime.datetime.now().hour
    # time =str(hour) +  str(minute)
    # if time=="2123":
    #     work()
    #     print("currency file changed")
    # minute = datetime.datetime.now().minute
    # hour = datetime.datetime.now().hour
    # time =str(hour) +  str(minute)
    # if time=="2123":
    #     work()
    #     print("currency file changed")
        work()