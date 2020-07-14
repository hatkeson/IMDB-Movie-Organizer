# Movie Organizer
# all IMDB interface files are sorted 

import csv, zlib, urllib.request
import tkinter as tk
from tkinter import ttk

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
        # Search by title
        # Search by Year
        # Search by decade should be a SpinBox
        # Search by director

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
        self.tabControl.add(self.searchTab, text='Search Movie List')
        self.tabControl.pack(expand=1, fill='both')

        # widgets for Add tab
        self.labelTitle = ttk.Label(self.addTab, text='Title:')
        self.labelTitle.grid(row=0, column=0, sticky=tk.E)
        self.entryTitle = ttk.Entry(self.addTab)
        self.entryTitle.grid(row=0, column=1)
        
        self.labelYear = ttk.Label(self.addTab, text='Year:')
        self.labelYear.grid(row=1, column=0, sticky=tk.E)
        self.entryYear = ttk.Entry(self.addTab)
        self.entryYear.grid(row=1, column=1)

        self.searchButton = ttk.Button(self.addTab, text='Search', 
            command=lambda: self.searchAddTab(self.entryTitle.get(),
                self.entryYear.get()))
        self.searchButton.grid(row=1, column=2)

        self.labelNote = ttk.Label(self.addTab, text='') #filled in with input
        self.labelNote.grid(row=2, column=1)

        self.updateButton = ttk.Button(self.addTab,
                                       text='Update', command=self.update)
        self.updateButton.grid(row=2, column=2)

        self.labelIDResult = ttk.Label(self.addTab, text='ID#:')
        self.labelIDResult.grid(row=4, column=0, sticky=tk.E)

        self.labelID1 = ttk.Label(self.addTab, text='')
        self.labelID1.grid(row=4, column=1, sticky=tk.W)

        self.labelTitleResult = ttk.Label(self.addTab, text='Title:')
        self.labelTitleResult.grid(row=5, column=0, sticky=tk.E)

        self.labelTitle1 = ttk.Label(self.addTab, text='')
        self.labelTitle1.grid(row=5, column=1, sticky=tk.W) 

        self.labelYearResult = ttk.Label(self.addTab, text='Year:')
        self.labelYearResult.grid(row=6, column=0, sticky=tk.E)

        self.labelYear1 = ttk.Label(self.addTab, text='')
        self.labelYear1.grid(row=6, column=1, sticky=tk.W)

        self.labelDirectorResult = ttk.Label(self.addTab, text='Director:')
        self.labelDirectorResult.grid(row=7, column=0, sticky=tk.E)

        self.labelDirector1 = ttk.Label(self.addTab, text='')
        self.labelDirector1.grid(row=7, column=1, sticky=tk.W)

        self.labelRuntimeResult = ttk.Label(self.addTab, text='Runtime:')
        self.labelRuntimeResult.grid(row=8, column=0, sticky=tk.E)

        self.labelRuntime1 = ttk.Label(self.addTab, text='')
        self.labelRuntime1.grid(row=8, column=1, sticky=tk.W)

        self.labelFormat = ttk.Label(self.addTab, text='Format:')
        self.labelFormat.grid(row=9, column=0, sticky=tk.E)

        v = tk.StringVar()
        optionList = ['Choose a format', 'Blu-ray', 'DVD', 'VHS', 'Other']
        v.set(optionList[0])
        self.formatMenu = ttk.OptionMenu(self.addTab, v,'Choose a format',
                                    'Blu-ray', 'DVD', 'VHS', 'Other')
        self.formatMenu.grid(row=9, column=1, sticky=(tk.W+tk.E))

        self.labelStudio = ttk.Label(self.addTab, text='Studio:')
        self.labelStudio.grid(row=10, column=0, sticky=tk.E)

        self.entryStudio = ttk.Entry(self.addTab)
        self.entryStudio.grid(row=10, column=1)

        addButton = ttk.Button(self.addTab, text='Add to List', 
                                 command=self.addToList)
        addButton.grid(row=10, column=2)

        # widgets for Search tab
        self.label2 = ttk.Label(self.searchTab, text='This is the search tab')
        self.label2.grid(row=0, column=0)
        
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
                    
        # search primaryTitle (third element in entry, entry[2])
        # if match found
            # send 'Result Found' to notification cell
            # fill in result fields: Title, Year, Director, Runtime
                # for Director field:
                # must use title ID (tt) to search title.crew and
                # find director ID (nm) entry[1]
                # use director ID to search name.basics to find name string
        # if match not found
            # send 'Result Not Found' to notification cell

    def addToList(self, ID, title, year, director, runtime, form, studio):
        print('Add button clicked!')
        # get info from label widgets
        # construct an entry with tabs between elements, newline at end
        # entry should include:
            # title, year, director, runtime, format, studio
        # write entry to my_list.tsv
        # send "Added to List!" to notification cell
        # organize by title (common case), use binary insert and search

    def update(self):
        print ('Update button clicked!')
        fileURLs = ['name.basics.tsv.gz', 'title.basics.tsv.gz',
                'title.crew.tsv.gz']
        length = len(fileURLs)
        for i in range(length):
            filedata = urllib.request.urlopen(
                'https://datasets.imdbws.com/' + fileURLs[i])
            print('Reading file ' + str(i+1) + ' of ' + str(length))
            self.labelNote['text'] = 'Reading file ' + str(i+1) \
                + ' of ' + str(length)
            zippedData = filedata.read()
            print('Unzipping file ' + str(i+1) + ' of ' + str(length))
            self.labelNote['text'] = 'Unzipping file ' + str(i+1) \
                + ' of ' + str(length)
            unzipped = zlib.decompress(zippedData, 15+32)
            print('Decoding file ' + str(i+1) + ' of ' + str(length))
            self.labelNote['text'] = 'Decoding file ' + str(i+1) \
                + ' of ' + str(length)
            listFile = unzipped.decode('utf-8').splitlines()
            print('Writing file ' + str(i+1) + ' of ' + str(length))
            self.labelNote['text'] ='Writing file ' + str(i+1) \
                + ' of ' + str(length)
 
            with open(__file__[:-18] + 'data/' + fileURLs[i][:-3], 'w') as f:
                wr = csv.writer(f, delimiter='\t')
                rd = csv.reader(listFile, delimiter='\t')
                for row in rd:
                    if (i == 0):
                        wr.writerow(row)
                    elif (i == 1 and (row[1] == 'movie' or
                                    row[1] == 'short' or
                                    row[1] == 'tvMovie' or
                                    row[1] == 'video') and
                        row[5] != '\\N' and row[7] != '\\N'):
                        wr.writerow(row)
                    elif (i == 2 and row[1] != '\\N'):
                        wr.writerow(row)
        
        self.labelNote['text'] = 'Update successful!'
        print('Update successful!')
    
#run window
root = tk.Tk()
app = Application(master=root)
app.mainloop()
