from flask import Flask
import requests
from bs4 import BeautifulSoup
from flask.ext.sqlalchemy import SQLAlchemy
import models

app = Flask(__name__)
db = SQLAlchemy(app)

@app.route("/")
def hello():
    member = models.Member
    return "Hello World!"

if __name__ == "__main__":
    app.run()

url = "http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results"
queries = ["?q=&sen=1&par=-1&gen=0&ps=0", "?q=&mem=1&par=-1&gen=0&ps=0"]
member_links = []

def getFederalMembers(query):
    page = requests.get(url + query).content
    soup = BeautifulSoup(page)
    for x in soup.find_all('p', "title"):
        link = x.find_all('a')
        if len(link) > 0 :
            member_links.append(link[0]['href'])

    next_page = soup.find_all('a', attrs={'title' : 'Next page'})
    if len(next_page) > 0:
        getFederalMembers(next_page[0]['href'])

# for query in queries:
#     getFederalMembers(query)
#
# print member_links
