# Movie Organizer

import csv
import tkinter as tk
from tkinter import ttk
import imdb
from imdb import IMDb

# create Application class:
# window should have "Movie Organizer" title
# window should be 800x600
# widgets:
    # notebook - should have 2 tabs: "Add/Remove" and "Search"
    # Add tab - 3x5 grid
        # has 5 labels: "Title:" "Year:" "Result" "Format:" "Studio:"
        # Two buttons: "Search" "Add"
        # Add format and studio
        # List box for result
    # Search Tab
        # Search by Title
        # Search by Year
        # Search by Decade (should be a SpinBox)
        # Search by Director

# use IMDbPY to search would cut down search time considerably
# first, import imdb and imdb.IMDb
# Adding to List:
    # user enters in title and year
    # use title as parameter for search_movie()
    # narrow the results by comparing Year field to movie['year'] (class 'int')
        # this may throw a KeyError?
    # get ID of remaining result, get_movie(ID)
    # get 'directors', 'akas' and 'runtime' from this
    # put first result in Result fields (have it be entry so it's editable)
    # create tsv row of ['title', 'akas', 'year', 'director', 'runtime']
    # write to mylist.tsv, insert in alphabetical order by title (binary search)
# Searching for a Movie
    # take info from entry fields: title, year, director, decade
        # all should be optional, if there is no entry then print notification
    # open mylist.tsv, use binary search for title (common case)
        # check both title fields and AKAs
    # have to linearly search for all others
    # if more than one parameter, have to check each


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
        self.tabControl.pack(expand=1, fill='both')
        self.create_addTab_widgets()
        self.create_searchTab_widgets()

    def create_addTab_widgets(self):
        # widgets for Add tab
        self.addFrame = ttk.Frame(self.addTab)
        self.addFrame.pack(side=tk.TOP)
        
        self.labelTitle = ttk.Label(self.addFrame, text='Title:')
        self.labelTitle.grid(row=0, column=0, sticky=tk.E)
        self.entryTitle = ttk.Entry(self.addFrame)
        self.entryTitle.grid(row=0, column=1)
        
        self.labelYear = ttk.Label(self.addFrame, text='Year:')
        self.labelYear.grid(row=1, column=0, sticky=tk.E)
        self.entryYear = ttk.Entry(self.addFrame)
        self.entryYear.grid(row=1, column=1)

        self.searchButton = ttk.Button(self.addFrame, text='Search', 
            command=lambda: self.searchAddTab(self.entryTitle.get(),
                self.entryYear.get()))
        self.searchButton.grid(row=1, column=2)

        self.labelNote = ttk.Label(self.addFrame, text='') #filled in with input
        self.labelNote.grid(row=2, column=1)

        self.updateButton = ttk.Button(self.addFrame,
                                       text='Update', command=self.update)
        self.updateButton.grid(row=2, column=2)

        self.labelIDResult = ttk.Label(self.addFrame, text='ID#:')
        self.labelIDResult.grid(row=4, column=0, sticky=tk.E)

        self.labelID1 = ttk.Entry(self.addFrame)
        self.labelID1.grid(row=4, column=1)

        self.labelTitleResult = ttk.Label(self.addFrame, text='Title:')
        self.labelTitleResult.grid(row=5, column=0, sticky=tk.E)

        self.labelTitle1 = ttk.Entry(self.addFrame)
        self.labelTitle1.grid(row=5, column=1) 

        self.labelYearResult = ttk.Label(self.addFrame, text='Year:')
        self.labelYearResult.grid(row=6, column=0, sticky=tk.E)

        self.labelYear1 = ttk.Entry(self.addFrame)
        self.labelYear1.grid(row=6, column=1)

        self.labelDirectorResult = ttk.Label(self.addFrame, text='Director:')
        self.labelDirectorResult.grid(row=7, column=0, sticky=tk.E)

        self.labelDirector1 = ttk.Entry(self.addFrame)
        self.labelDirector1.grid(row=7, column=1)

        self.labelRuntimeResult = ttk.Label(self.addFrame, text='Runtime:')
        self.labelRuntimeResult.grid(row=8, column=0, sticky=tk.E)

        self.labelRuntime1 = ttk.Entry(self.addFrame)
        self.labelRuntime1.grid(row=8, column=1)

        self.labelFormat = ttk.Label(self.addFrame, text='Format:')
        self.labelFormat.grid(row=9, column=0, sticky=tk.E)

        v = tk.StringVar()
        optionList = ['Choose a format', 'Blu-ray', 'DVD', 'VHS', 'Other']
        v.set(optionList[0])
        self.formatMenu = ttk.OptionMenu(self.addFrame, v,'Choose a format',
                                    'Blu-ray', 'DVD', 'VHS', 'Other')
        self.formatMenu.grid(row=9, column=1, sticky=(tk.W+tk.E))

        self.labelStudio = ttk.Label(self.addFrame, text='Studio:')
        self.labelStudio.grid(row=10, column=0, sticky=tk.E)

        self.entryStudio = ttk.Entry(self.addFrame)
        self.entryStudio.grid(row=10, column=1)

        addButton = ttk.Button(self.addFrame, text='Add to List', 
                                 command=self.addToList)
        addButton.grid(row=10, column=2)

    def create_searchTab_widgets(self):
        # widgets for Search tab

        self.searchFrame = ttk.Frame(self.searchTab)
        self.searchFrame.pack(side=tk.TOP)
        
        self.searchTitle = ttk.Label(self.searchFrame, text='Title: ')
        self.searchTitle.grid(row=0, column=0, sticky=tk.E)

        self.searchTitleEntry = ttk.Entry(self.searchFrame)
        self.searchTitleEntry.grid(row=0, column=1)

        self.searchYear = ttk.Label(self.searchFrame, text='Year: ')
        self.searchYear.grid(row=1, column=0, sticky=tk.E)

        self.searchYearEntry = ttk.Entry(self.searchFrame)
        self.searchYearEntry.grid(row=1, column=1)

        self.searchDirector = ttk.Label(self.searchFrame, text='Director: ')
        self.searchDirector.grid(row=2, column=0, sticky=tk.E)

        self.searchDirectorEntry = ttk.Entry(self.searchFrame)
        self.searchDirectorEntry.grid(row=2, column=1)

        self.searchDecade = ttk.Label(self.searchFrame, text='Decade: ')
        self.searchDecade.grid(row=3, column=0, sticky=tk.E)

        v = tk.StringVar()
        v.set('Choose a Decade')
        self.formatMenu = ttk.OptionMenu(self.searchFrame, v, 'Choose a Decade',
                                         '1920s', '1930s', '1940s', '1950s',
                                         '1960s', '1970s', '1980s', '1990s',
                                         '2000s', '2010s', '2020s', '2030s')
        self.formatMenu.grid(row=3, column=1, sticky=(tk.W+tk.E))

        self.searchButton = ttk.Button(self.searchFrame, text='Search', 
            command=lambda: self.search_mylist())
        self.searchButton.grid(row=3, column=2)

        self.search_note_cell = ttk.Label(self.searchFrame, text='')
        self.search_note_cell.grid(row=4, column=1)

        self.searchResults = ttk.Treeview(self.searchTab, columns=['Title',
                                        'Year', 'Director', 'AKAs', 'Runtime',
                                        'Format', 'Studio'])
        self.searchResults.pack(side=tk.BOTTOM)
        self.searchResults.heading('Title', text='Title', anchor=tk.W)
        self.searchResults.heading('Year', text='Year', anchor=tk.W)
        self.searchResults.heading('Director', text='Director', anchor=tk.W)
        self.searchResults.heading('AKAs', text='AKAs', anchor=tk.W)
        self.searchResults.heading('Runtime', text='Runtime', anchor=tk.W)
        self.searchResults.heading('Format', text='Format', anchor=tk.W)
        self.searchResults.heading('Studio', text='Studio', anchor=tk.W)

        self.searchResults.column('Title', width=200, minwidth=200)
        self.searchResults.column('Year', width=50, minwidth=50)
        self.searchResults.column('Director', width=200, minwidth=200)
        self.searchResults.column('AKAs', width=200, minwidth=200)
        self.searchResults.column('Runtime', width=50, minwidth=50)
        self.searchResults.column('Format', width=100, minwidth=100)
        self.searchResults.column('Studio', width=200, minwidth=200)
        
        self.searchResults['show'] = 'headings'
        
    def searchAddTab(self, title, year=''):
        print('Search button clicked!')
        if (title == ''):
            self.labelNote['text'] = 'Please enter a title.'
        else:
            found = False
            directorID = ''
            self.labelNote['text'] = 'Searching...'
            with open("data/title.basics.tsv") as tb:
                rd = csv.reader(tb, delimiter='\t')
                title = self.entryTitle.get()
                if (self.entryYear.get() != 0):
                    year = self.entryYear.get()
                for row in rd:
                    if (row[2] == title and (year == '' or row[5] == year)):
                        found = True
                        self.labelID1['text'] = row[0]
                        self.labelTitle1['text'] = row[2]
                        self.labelYear1['text'] = row[5]
                        self.labelRuntime1['text'] = row[7]
                        break
            with open('data/title.crew.tsv') as tc:
                rd = csv.reader(tc, delimiter='\t')
                titleID = self.labelID1.cget('text')
                for row in rd:
                    if (row[0] == titleID):
                        directorID = row[1]
            with open('data/name.basics.tsv') as nb:
                rd = csv.reader(nb, delimiter='\t')
                for row in rd:
                    if (row[0] == directorID):
                        self.labelDirector1['text'] = row[1]
                            
            if (found):
                self.labelNote['text'] = 'Result Found!'
            else:
                self.labelNote['text'] = 'No Result Found.'

    def search_mylist(self):
        print('Searching mylist.tsv...')

    def addToList(self, ID, title, year, director, runtime, form, studio):
        print('Add button clicked!')
        # get info from result entry widgets
        # construct an entry with tabs between elements, newline at end
        # entry should include:
            # title, year, director, runtime, format, studio
        # write entry to my_list.tsv
        # send "Added to List!" to notification cell
        # organize by title (common case), use binary insert and search

    def update(self):
        print ('Update button clicked!')
        fileURLs = ['title.crew.tsv.gz', 'name.basics.tsv.gz',
                    'title.basics.tsv.gz', 'title.akas.tsv.gz']
        length = len(fileURLs)
        for i in range(length):
            filedata = urllib.request.urlopen(
                'https://datasets.imdbws.com/' + fileURLs[i])
            print('Reading file ' + str(i+1) + ' of ' + str(length))
            zippedData = filedata.read()
            print('Unzipping file ' + str(i+1) + ' of ' + str(length))
            unzipped = zlib.decompress(zippedData, 15+32)
            print('Decoding file ' + str(i+1) + ' of ' + str(length))
            listFile = unzipped.decode('utf-8').splitlines()
            print('Writing file ' + str(i+1) + ' of ' + str(length))
 
            with open(__file__[:-18] + 'data/' + fileURLs[i][:-3], 'w') as f:
                wr = csv.writer(f, delimiter='\t')
                rd = csv.reader(listFile, delimiter='\t')
                for row in rd:
                    if (i == 0 and row[1] != '\\N'):
                        wr.writerow(row)
                    elif (i == 1):
                        with open(__file__[:-18] + 'data/' +
                                  fileURLs[0][:-3], 'r') as tc:
                            rdtc = csv.reader(tc, delimiter='\t')
                            for row1 in rdtc:
                                if (row[0] in row1[1]):
                                   wr.writerow(row)
                                   break
                    elif (i == 2 and (row[1] == 'movie' or
                                    row[1] == 'short' or
                                    row[1] == 'tvMovie' or
                                    row[1] == 'video') and
                        row[5] != '\\N' and row[7] != '\\N'):
                        wr.writerow(row)
                    else:
                        wr.writerow(row)
        
        self.labelNote['text'] = 'Update successful!'
        print('Update successful!')
    
#run window
root = tk.Tk()
app = Application(master=root)
app.mainloop()
