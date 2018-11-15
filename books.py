import numpy as np
from rec import *
import pandas as pd
import csv
import urllib
from bs4 import BeautifulSoup
import goodreads_api_client as gr


path = "C:/Users/moham/OneDrive/Documents/books_task/BX-Books.csv"
#------------------reading the CSV into a dataframe
data = pd.read_csv(path, encoding='latin-1', error_bad_lines=False , sep=";")


book_data = pd.DataFrame(data)
#----------------- initializing 2 added columns for the books data frame
book_lang = []
book_genre = []

