import urllib.request
import requests
from bs4 import BeautifulSoup
import goodreads_api_client as gr
import time



start_time = time.time()
#gets the url of the book on goodreads by its isbn

def get_url(isbn):
    response = requests.get("http://www.goodreads.com/book/isbn/"+isbn)
    if response.history:
        return  response.url

#scrap the page for the language and genre of the book
def scrap_language(url):
    thepage = urllib.request.urlopen(url)
    soup = BeautifulSoup(thepage, "html.parser")
    lang_soup = soup.findAll("div",{"class":"infoBoxRowItem"})
    language = lang_soup[2].text

    return language
def scrap_genre(url):
    genre_list = []
    thepage = urllib.request.urlopen(url)
    soup = BeautifulSoup(thepage, "html.parser")
    genre_soup = soup.findAll("div", {"class": "elementList"})
    for i in range(len(genre_soup)):
        genre_list.append(genre_soup[i].div.find("a").text)
    return set(genre_list)

#-----------testing the functions by a given url----------------
print(scrap_language(get_url('0002005018')))
print(scrap_genre(get_url('0002005018')))
print("--- %s seconds ---" % (time.time() - start_time))