import requests, string, urllib3
import concurrent.futures
urllib3.disable_warnings()

from flask import *

app=Flask(__name__)
app.secret="hlwvai00008"


ends=string.ascii_lowercase+string.digits





def searchAmazon(q):
    try:
        h={
    "Host": "completion.amazon.com",
    "Connection": "keep-alive",
    "sec-ch-ua": "\"Not?A_Brand\";v\u003d\"8\", \"Chromium\";v\u003d\"108\", \"Google Chrome\";v\u003d\"108\"",
    "DNT": "1",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": "\"Linux\"",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Dest": "script",
    "Referer": "https://vaibhav.wtf/",
    "Accept-Language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7"
        }
        req=requests.get(f"https://completion.amazon.com/search/complete?mkt\u003d1\u0026search-alias\u003daps\u0026q\u003d{q}", headers=h, verify=False).text
        data=eval(req)
        #print(data)
        return data[1]
    except:
        return []

def searchGoogle(q):
    try:
        h={
    "Host": "suggestqueries.google.com",
    "sec-ch-ua": "\"Not?A_Brand\";v\u003d\"8\", \"Chromium\";v\u003d\"108\", \"Google Chrome\";v\u003d\"108\"",
    "dnt": "1",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": "\"Linux\"",
    "accept": "*/*",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-dest": "script",
    "referer": "https://vaibhav.wtf/",
    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7"
        }
        req=requests.get(f"https://suggestqueries.google.com/complete/search?client\u003dchrome\u0026q\u003d{q}", headers=h, verify=False).text
        data=eval(req.replace("false", "False",).replace("true", "True"))
        return data[1]
    except:
        return []


def searchYouTube(q):
    try:
        h={
    "Host": "clients1.google.com",
    "sec-ch-ua": "\"Not?A_Brand\";v\u003d\"8\", \"Chromium\";v\u003d\"108\", \"Google Chrome\";v\u003d\"108\"",
    "dnt": "1",
    "sec-ch-ua-mobile": "?0",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": "\"Linux\"",
    "accept": "*/*",
    "sec-fetch-site": "cross-site",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-dest": "script",
    "referer": "https://vaibhav.wtf/",
    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7"
        }
        req=requests.get(f"https://clients1.google.com/complete/search?client\u003dyoutube\u0026q\u003d{q}", headers=h, verify=False).text
    
        j=["(",")","window.google.ac.h"]
        for ho in j:
            req=req.replace(ho, "")
       # print(req)
        data=eval(req)[1]
        kw=[]
        for i in range(0, len(data)-2):
            kw.append(data[i][0])
        return kw
    except:
        return []
 


def m(t):
    kw=[]
    h=searchYouTube(t)
    h1=searchGoogle(t)
    h2=searchAmazon(t)
    for ok in h:
        kw.append(ok.strip())

    for ok in h1:
        if ok.strip() not in kw:
            kw.append(ok.strip())

    for ok in h2:
        if ok.strip() not in kw:
            kw.append(ok.strip())
    for i in ends:
        q1=t+" "+i
        h=searchYouTube(q1)
        h1=searchAmazon(q1)
        h2=searchGoogle(q1)
        for ok in h:
            if ok.strip() not in kw:
                kw.append(ok.strip())
        for ok in h1:
            if ok.strip() not in kw:
                kw.append(ok.strip())
        for ok in h2:
            if ok.strip() not in kw:
                kw.append(ok.strip())
        
    return kw

@app.route("/api/keyword")
@app.route("/api/keyword")
def keywordapi():
    if request.args.get("q"):
        kw=[]
        q=request.args.get("q")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(m, q)
            kw = future.result()
        return jsonify(status=True, data=kw)
    else:
        return jsonify(status=False, data=None)

@app.route("/")
def home():
    return "hey"
if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")
