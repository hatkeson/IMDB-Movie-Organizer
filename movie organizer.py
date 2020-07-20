import csv
import ast
import os
from os import path
import tkinter as tk
from tkinter import ttk
import imdb
from imdb import IMDb

class Application(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        master.title("Movie Organizer")
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Notebook widget for tabs
        self.tabControl = ttk.Notebook(self)
        self.addTab = ttk.Frame(self.tabControl)
        self.searchTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.addTab, text='Add New Movie')
        self.tabControl.add(self.searchTab, text='Search My Collection')
        self.tabControl.pack(expand=1, fill=tk.BOTH)
        self.create_addTab_widgets()
        self.create_searchTab_widgets()

    def handleReturn_searchAddTab(self, event):
        self.searchAddTab(self.entryTitle.get(), self.entryYear.get())

    def handleReturn_addToList(self, event):
        self.addToList(self.labelTitle1.get(), self.labelYear1.get(),
                       self.labelDirector1.get(), self.labelRuntime1.get(),
                       self.listAKA1.get(0, tk.END), self.v.get(),
                       self.entryStudio.get(), self.entryLocation.get())

    def handleReturn_search_mylist(self, event, v):
        self.search_mylist(self.searchTitleEntry.get(),
                           self.searchYearEntry.get(),
                           self.searchDirectorEntry.get(),
                           v.get())

    def create_addTab_widgets(self):
        # widgets for Add tab
        self.addFrame = ttk.Frame(self.addTab)
        self.addFrame.pack(side=tk.TOP)
        
        self.labelTitle = ttk.Label(self.addFrame, text='Title:')
        self.labelTitle.grid(row=0, column=0, sticky=tk.E)
        self.entryTitle = ttk.Entry(self.addFrame, width=40)
        self.entryTitle.grid(row=0, column=1)
        self.entryTitle.bind('<Return>', self.handleReturn_searchAddTab)
        
        self.labelYear = ttk.Label(self.addFrame, text='Year:')
        self.labelYear.grid(row=1, column=0, sticky=tk.E)
        self.entryYear = ttk.Entry(self.addFrame, width=40)
        self.entryYear.grid(row=1, column=1)
        self.entryYear.bind('<Return>', self.handleReturn_searchAddTab)

        self.searchButton = ttk.Button(self.addFrame, text='Search', 
            command=lambda: self.searchAddTab(self.entryTitle.get(),
                self.entryYear.get()))
        self.searchButton.grid(row=1, column=2)
        self.searchButton.bind('<Return>', self.handleReturn_searchAddTab)

        self.labelNote = ttk.Label(self.addFrame, text='') 
        self.labelNote.grid(row=2, column=1)

        self.labelTitleResult = ttk.Label(self.addFrame, text='Title:')
        self.labelTitleResult.grid(row=4, column=0, sticky=tk.E)
        self.labelTitle1 = ttk.Entry(self.addFrame, width=40)
        self.labelTitle1.grid(row=4, column=1) 

        self.labelYearResult = ttk.Label(self.addFrame, text='Year:')
        self.labelYearResult.grid(row=5, column=0, sticky=tk.E)
        self.labelYear1 = ttk.Entry(self.addFrame, width=40)
        self.labelYear1.grid(row=5, column=1)

        self.labelDirectorResult = ttk.Label(self.addFrame, text='Director:')
        self.labelDirectorResult.grid(row=6, column=0, sticky=tk.E)
        self.labelDirector1 = ttk.Entry(self.addFrame, width=40)
        self.labelDirector1.grid(row=6, column=1)

        self.labelRuntimeResult = ttk.Label(self.addFrame, text='Runtime:')
        self.labelRuntimeResult.grid(row=7, column=0, sticky=tk.E)
        self.labelRuntime1 = ttk.Entry(self.addFrame, width=40)
        self.labelRuntime1.grid(row=7, column=1)

        self.labelAKAResult = ttk.Label(self.addFrame,
                                        text='Alternate Title(s):')
        self.labelAKAResult.grid(row=8, column=0, sticky=tk.E)
        self.listAKA1 = tk.Listbox(self.addFrame, width=40)
        self.listAKA1.grid(row=8, column=1)

        self.labelFormat = ttk.Label(self.addFrame, text='Format:')
        self.labelFormat.grid(row=9, column=0, sticky=tk.E)

        self.v = tk.StringVar()
        optionList = ['Choose a format', 'Blu-ray', 'DVD', 'VHS', 'Other']
        self.v.set(optionList[0])
        self.formatMenu = ttk.OptionMenu(self.addFrame, self.v,
                                         'Choose a format', 'Blu-ray',
                                         'DVD', 'VHS', 'Other')
        self.formatMenu.grid(row=9, column=1, sticky=(tk.W+tk.E))

        self.labelStudio = ttk.Label(self.addFrame, text='Studio:')
        self.labelStudio.grid(row=10, column=0, sticky=tk.E)
        self.entryStudio = ttk.Entry(self.addFrame, width=40)
        self.entryStudio.grid(row=10, column=1)
        self.entryStudio.bind('<Return>', self.handleReturn_addToList)

        self.labelLocation = ttk.Label(self.addFrame, text='Location:')
        self.labelLocation.grid(row=11, column=0, sticky=tk.E)
        self.entryLocation = ttk.Entry(self.addFrame, width=40)
        self.entryLocation.grid(row=11, column=1)
        self.entryLocation.bind('<Return>', self.handleReturn_addToList)

        addButton = ttk.Button(self.addFrame, text='Add to List', 
                                 command=lambda: self.addToList(
                                     self.labelTitle1.get(),
                                     self.labelYear1.get(),
                                     self.labelDirector1.get(),
                                     self.labelRuntime1.get(),
                                     self.listAKA1.get(0, tk.END),
                                     self.v.get(),
                                     self.entryStudio.get(),
                                     self.entryLocation.get()))
        addButton.grid(row=11, column=2)
        addButton.bind('<Return>', self.handleReturn_addToList)

    def create_searchTab_widgets(self):
        # widgets for Search tab

        self.searchFrame = ttk.Frame(self.searchTab)
        self.searchFrame.grid(row=0, column=0)
        
        self.searchTitle = ttk.Label(self.searchFrame, text='Title: ')
        self.searchTitle.grid(row=0, column=0, sticky=tk.E)
        self.searchTitleEntry = ttk.Entry(self.searchFrame, width=40)
        self.searchTitleEntry.grid(row=0, column=1)

        self.searchYear = ttk.Label(self.searchFrame, text='Year: ')
        self.searchYear.grid(row=1, column=0, sticky=tk.E)
        self.searchYearEntry = ttk.Entry(self.searchFrame, width=40)
        self.searchYearEntry.grid(row=1, column=1)

        self.searchDirector = ttk.Label(self.searchFrame, text='Director: ')
        self.searchDirector.grid(row=2, column=0, sticky=tk.E)
        self.searchDirectorEntry = ttk.Entry(self.searchFrame, width=40)
        self.searchDirectorEntry.grid(row=2, column=1)

        self.searchDecade = ttk.Label(self.searchFrame, text='Decade: ')
        self.searchDecade.grid(row=3, column=0, sticky=tk.E)
        v = tk.StringVar()
        v.set('Choose a Decade')
        self.decadeMenu = ttk.OptionMenu(self.searchFrame, v, 'Choose a Decade',
                                         'None',
                                         '1920s', '1930s', '1940s', '1950s',
                                         '1960s', '1970s', '1980s', '1990s',
                                         '2000s', '2010s', '2020s', '2030s')
        self.decadeMenu.grid(row=3, column=1, sticky=(tk.W+tk.E))

        self.searchButton = ttk.Button(self.searchFrame, text='Search', 
            command=lambda: self.search_mylist(self.searchTitleEntry.get(),
                                               self.searchYearEntry.get(),
                                               self.searchDirectorEntry.get(),
                                               v.get()))
        self.searchButton.grid(row=3, column=2)

        self.search_note_cell = ttk.Label(self.searchFrame, text='')
        self.search_note_cell.grid(row=4, column=1)

        self.searchResults = ttk.Treeview(self.searchTab, columns=[
                                        'Year', 'Director', 'Runtime',
                                        'Format', 'Studio', 'Location'],
                                        height=16)
        self.searchResults.grid(row=1, column=0)
        self.searchResults.heading('#0', text='Title', anchor=tk.W)
        self.searchResults.heading('Year', text='Year', anchor=tk.W)
        self.searchResults.heading('Director', text='Director', anchor=tk.W)
        self.searchResults.heading('Runtime', text='Runtime', anchor=tk.W)
        self.searchResults.heading('Format', text='Format', anchor=tk.W)
        self.searchResults.heading('Studio', text='Studio', anchor=tk.W)
        self.searchResults.heading('Location', text='Location', anchor=tk.W)

        self.searchResults.column('#0', width=200, minwidth=50)
        self.searchResults.column('Year', width=50, minwidth=50)
        self.searchResults.column('Director', width=150, minwidth=50)
        self.searchResults.column('Runtime', width=50, minwidth=50)
        self.searchResults.column('Format', width=70, minwidth=50)
        self.searchResults.column('Studio', width=150, minwidth=50)
        self.searchResults.column('Location', width=100, minwidth=50)
            
    def searchAddTab(self, title, year=''):
        print('Search button clicked!')
        if (title == ''):
            self.labelNote['text'] = 'Please enter a title.'
        else:
            self.labelNote['text'] = 'Searching...'

            ia = imdb.IMDb()
            movieList = ia.search_movie(self.entryTitle.get())
            movieList = [mov for mov in movieList if 'year' in mov.keys()]
            finalList = []
            if (year == ''):
                finalList = movieList
            else:
                for mov in movieList:
                    if (int(year) == mov['year']):
                        finalList.append(mov)
            self.labelTitle1.delete(0, last=tk.END)
            self.labelYear1.delete(0, last=tk.END)
            self.labelDirector1.delete(0, last=tk.END)
            self.labelRuntime1.delete(0, last=tk.END)
            self.listAKA1.delete(0, tk.END)
            self.entryStudio.delete(0, tk.END)
            self.entryLocation.delete(0, tk.END)
            if (len(finalList) > 0):
                self.labelNote['text'] = 'Result Found!'
                movie = ia.get_movie(finalList[0].movieID)            
                self.labelTitle1.insert(2, movie['title'])
                self.labelYear1.insert(3, movie['year'])
                if ('runtimes' in movie.keys()):
                    for rt in movie['runtimes']:
                        self.labelRuntime1.insert(4, rt + ' ')
                else:
                    self.labelRuntime1.insert(4, 'Unavailable')
                if ('directors' in movie.keys()):
                    director = ia.get_person(movie['directors'][0].personID)
                    self.labelDirector1.insert(5, director['name'])
                else:
                    self.labelDirector1.insert(5, 'Unavailable')
                if ('akas' in movie.keys()):
                    for tt in movie['akas']:
                        self.listAKA1.insert(tk.END, tt)
                else:
                    self.listAKA1.insert(5, 'Unavailable')         
            else:
                self.labelNote['text'] = 'No Result Found.'

    def search_mylist(self, title='', year='', director='',
                      decade='Choose a Decade'):
        # go through each parameter until you find one that isn't empty
        # on the filled parameter, get all entries that match that parameter
        # on the next filled parameter, delete non-matches from that list
        # continue until out of parameters, then print results to list
        for row in self.searchResults.get_children():
                self.searchResults.delete(row)
        if (title == '' and year == '' and director == ''
            and (decade == 'Choose a Decade' or decade == 'None')):
            self.search_note_cell['text'] = 'Please enter a search parameter.'
        else:
            results = []
            with open('./data/my_collection.tsv', 'r') as mc:
                rd = csv.reader(mc, delimiter='\t')
                if (title != ''):
                    for row in rd:
                        if (title.casefold() in row[0].casefold() or
                            title.casefold() in row[4].casefold()):
                            results.append(row)
                if (year != ''):
                    if (len(results) > 0):
                        results = [ent for ent in results
                                   if ent[1] == year]
                    else:
                        for row in rd:
                            if (row[1] == year):
                                results.append(row)
                if (director != ''):
                    if (len(results) > 0):
                        results = [ent for ent in results
                                   if ent[2] == director]
                    else:
                        for row in rd:
                            if (director.casefold() in row[2].casefold()):
                                results.append(row)
                if (decade != 'Choose a Decade' and decade != 'None'):
                    switcher = {
                            '1920s': range(1920, 1930),
                            '1930s': range(1930, 1940),
                            '1940s': range(1940, 1950),
                            '1950s': range(1950, 1960),
                            '1960s': range(1960, 1970),
                            '1970s': range(1970, 1980),
                            '1980s': range(1980, 1990),
                            '1990s': range(1990, 2000),
                            '2000s': range(2000, 2010),
                            '2010s': range(2010, 2020),
                            '2020s': range(2020, 2030),
                            '2030s': range(2030, 2040)
                            }
                    if (len(results) > 0):
                        results = [ent for ent in results if int(ent[1])
                                   in switcher[decade]]
                    else:
                        for row in rd:
                            if (int(row[1]) in switcher[decade]):
                                    results.append(row)
            if (len(results) == 0):
                self.search_note_cell['text'] = 'No Result Found.'
            else:
                self.search_note_cell['text'] = 'Results Found!'
                for i in range(len(results)):
                    parent = self.searchResults.insert('', 'end',
                                            text=results[i][0],
                                            values=results[i][1:7])
                    alt_titles = ast.literal_eval(results[i][7])
                    for tt in alt_titles:
                        self.searchResults.insert(parent, 'end', text=tt)
                    
                        
    def create_tsv(self):
        with open('./data/my_collection.tsv', 'wt') as mc:
            print('File created!')

    def addToList(self, title, year, director, runtime, akas, form, studio,
                  location):
        print('Add button clicked!')
        
        if (form != 'Choose a Format' and studio != '' and location != ''):
            if (not os.path.isfile('./data/my_collection.tsv')):
                self.create_tsv()
            l = [title, year, director, runtime, form, studio, location, akas]
            with open('./data/my_collection.tsv', 'r+') as mc:
                wr = csv.writer(mc, delimiter='\t')
                already_present = False
                rd = csv.reader(mc, delimiter='\t')
                for row in rd:
                    if (row[:3] == l[:3]):
                        already_present = True
                if (already_present):
                    self.labelNote['text'] = 'Movie already in list.'
                else:
                    wr.writerow(l)
                    self.labelNote['text'] = 'Added to List!'
        else:
            self.labelNote['text'] = 'Please enter Format, Studio, and/or Location'

    
#run window
root = tk.Tk()
app = Application(master=root)
app.mainloop()
