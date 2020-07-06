#this program allows the user to search IMDB by entering a title and
#optionally a year.
#It displays the movie's title, director, year, plot summary,
#language, and runtime.
#It also allows for the user to export the results
#to a text document

import csv
import urllib



#delete outdated files
#download new files
#files are gzipped, must unzip

#open files
data_file = open("data.tsv", encoding = 'utf-8')

#read files
read_tsv = csv.reader(data_file, delimiter = "\t")

#user input
title = input("Please enter a title: ")
year = input("Please enter a year: ")
resultCount = 0

for row in read_tsv:
    if (title == row[2] and
        year == row[5]):
        print("Title: " + row[2])
        resultCount += 1
print("Search complete. " + str(resultCount) + " results.")

data_file.close()
