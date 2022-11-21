from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from flask import Flask, render_template, request
from newsapi import NewsApiClient
import os 

serviceUsername = "apikey-v2-i4aqnyc5du58vsvbebuib0pzt343xdamcoe6giwojve"
servicePassword = "945f1f315020063c3ff2210bb1392366"
serviceURL = "https://apikey-v2-i4aqnyc5du58vsvbebuib0pzt343xdamcoe6giwojve:945f1f315020063c3ff2210bb1392366@a10227b9-f22d-49cb-abac-f177c15a9bf1-bluemix.cloudantnosqldb.appdomain.cloud"

client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
client.connect()

app = Flask(__name__)

@app.route("/news")
def news():
    api_key = '8c23ecafe68242e5888dc613abebba6e'
    
    newsapi = NewsApiClient(api_key=api_key)

    top_headlines = newsapi.get_top_headlines(sources = "the-verge")
    all_articles = newsapi.get_everything(sources = "the-verge")

    t_articles = top_headlines['articles']
    a_articles = all_articles['articles']

    news = []
    desc = []
    img = []
    p_date = []
    url = []

    for i in range (len(t_articles)):
        main_article = t_articles[i]

        news.append(main_article['title'])
        desc.append(main_article['description'])
        img.append(main_article['urlToImage'])
        p_date.append(main_article['publishedAt'])
        url.append(main_article['url'])

        contents = zip( news,desc,img,p_date,url)

    news_all = []
    desc_all = []
    img_all = []
    p_date_all = []   
    url_all = []

    for j in range(len(a_articles)): 
        main_all_articles = a_articles[j]   

        news_all.append(main_all_articles['title'])
        desc_all.append(main_all_articles['description'])
        img_all.append(main_all_articles['urlToImage'])
        p_date_all.append(main_all_articles['publishedAt'])
        url_all.append(main_article['url'])
        
        all = zip( news_all,desc_all,img_all,p_date_all,url_all)

    return render_template('home.html',all = all)

@app.route("/search",methods = ['POST', 'GET'])
def searchFunct():
    inputText = request.form['sear']
    api_key = '4f625485702d4929a546bcf4eb9d5c79'
    
    newsapi = NewsApiClient(api_key=api_key)

    top_headlines = newsapi.get_top_headlines(sources="bbc-news")
    all_articles = newsapi.get_everything(q=inputText)

    t_articles = top_headlines['articles']
    a_articles = all_articles['articles']

    news = []
    desc = []
    img = []
    p_date = []
    url = []

    for i in range (len(t_articles)):
        main_article = t_articles[i]

        news.append(main_article['title'])
        desc.append(main_article['description'])
        img.append(main_article['urlToImage'])
        p_date.append(main_article['publishedAt'])
        url.append(main_article['url'])

        contents = zip( news,desc,img,p_date,url)

    news_all = []
    desc_all = []
    img_all = []
    p_date_all = []   
    url_all = []

    for j in range(len(a_articles)): 
        main_all_articles = a_articles[j]   

        news_all.append(main_all_articles['title'])
        desc_all.append(main_all_articles['description'])
        img_all.append(main_all_articles['urlToImage'])
        p_date_all.append(main_all_articles['publishedAt'])
        url_all.append(main_article['url'])
        
        all = zip( news_all,desc_all,img_all,p_date_all,url_all)

    return render_template('home.html', all = all)

def addNewUser(userName,userEmail,userPassword):
    jsondata = {}
    jsondata["userName"] = str(userName)
    jsondata["userEmail"] = str(userEmail)
    jsondata["userPassword"] = str(userPassword)

    myDataBase = client['database_db']
    newDocument = myDataBase.create_document(jsondata)


def authenticate(userName,userEmail):
    myDataBase = client['database_db']
    result_collection = Result(myDataBase.all_docs, include_docs=True)
    for data in result_collection:

        if data['doc']['userName'] == str(userName):
            return True
        if data['doc']['userEmail'] == str(userEmail):
            return True
    return False

def authenticateLogin(userEmail,userPassword):
    myDataBase = client['database_db']
    result_collection = Result(myDataBase.all_docs, include_docs=True)
   
    for data in result_collection:
        if data['doc']['userPassword'] == str(userPassword) and data['doc']['userEmail'] == str(userEmail):    
            return True
    return False

@app.route("/login",methods = ['POST', 'GET'])
def loginUser():    
    userEmail = request.form.get("email")
    userPassword = request.form.get("pass")
    print(userEmail)
    if(authenticateLogin(userEmail,userPassword)):
        return news()
    else:
        return render_template("fail.html")

@app.route("/register",methods = ['POST', 'GET'])
def registerUserData():
    userName = request.form.get("uname")
    userEmail = request.form.get("uemail")
    userPassword = request.form.get("upass")
    
    print(userEmail,userName,userPassword)
    if(authenticate(userName=userName,userEmail=userEmail)):
        return render_template("register.html")
    addNewUser(userName,userEmail,userPassword)
    return news()

@app.route("/")
def home():
    return render_template("index.html")



if __name__ == '__main__':
    port = os.environ.get('PORT',5000)
    app.run(port=port,host="0.0.0.0",debug=True)
