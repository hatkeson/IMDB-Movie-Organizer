import sqlite3 as sql
import ast
import tkinter as tk
from tkinter import ttk
import imdb
from imdb import IMDb

# TODO:
# implement edit (UPDATE) and delete (DELETE) functions
# Search shows multiple result
# Make it so that "the" "a" "an" aren't counted for alphabetizing

class Application(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        master.title("Movie Organizer")
        self.master = master
        self.pack()
        self.sql_create()
        self.create_widgets()

    def sql_create(self):
        conn = sql.connect('collection.db')
        c = conn.cursor() 
        c.execute('''CREATE TABLE IF NOT EXISTS films (
                    title text PRIMARY KEY NOT NULL,
                    year integer NOT NULL CHECK (length(year) == 4),
                    director text NOT NULL,
                    runtime integer,
                    format text,
                    studio text,
                    location text,
                    akas text)
                    WITHOUT ROWID''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        # Notebook widget for tabs
        self.tab_control = ttk.Notebook(self)
        self.add_tab = ttk.Frame(self.tab_control)
        self.search_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.add_tab, text='Add New Movie')
        self.tab_control.add(self.search_tab, text='Search My Collection')
        self.tab_control.pack(expand=1, fill=tk.BOTH)
        self.create_add_tab_widgets()
        self.create_search_tab_widgets()

    def return_add_tab_search(self, event):
        self.add_tab_search(self.title_input_entry.get(), self.year_input_entry.get())

    def return_list_add(self, event):
        self.list_add(self.title_output_entry.get(), self.year_output_entry.get(),
                       self.director_output_entry.get(), self.runtime_output_entry.get(),
                       self.akas_output_listbox.get(0, tk.END), self.v.get(),
                       self.studio_input_entry.get(), self.location_input_entry.get())

    def return_search_my_list(self, event, v):
        self.search_my_list(self.search_title_entry.get(),
                           self.search_year_entry.get(),
                           self.search_director_entry.get(),
                           v.get())

    def create_add_tab_widgets(self):
        # widgets for Add tab
        self.add_frame = ttk.Frame(self.add_tab)
        self.add_frame.pack(side=tk.TOP)
        
        self.title_input_label = ttk.Label(self.add_frame, text='Title:')
        self.title_input_label.grid(row=0, column=0, sticky=tk.E)
        self.title_input_entry = ttk.Entry(self.add_frame, width=40)
        self.title_input_entry.grid(row=0, column=1)
        self.title_input_entry.bind('<Return>', self.return_add_tab_search)
        
        self.year_input_label = ttk.Label(self.add_frame, text='Year:')
        self.year_input_label.grid(row=1, column=0, sticky=tk.E)
        self.year_input_entry = ttk.Entry(self.add_frame, width=40)
        self.year_input_entry.grid(row=1, column=1)
        self.year_input_entry.bind('<Return>', self.return_add_tab_search)

        self.add_tab_search_button = ttk.Button(self.add_frame, text='Search', 
            command=lambda: self.add_tab_search(self.title_input_entry.get(),
                self.year_input_entry.get()))
        self.add_tab_search_button.grid(row=1, column=2)
        self.add_tab_search_button.bind('<Return>', self.return_add_tab_search)

        self.add_note_cell = ttk.Label(self.add_frame, text='') 
        self.add_note_cell.grid(row=2, column=1)

        self.title_output_label = ttk.Label(self.add_frame, text='Title:')
        self.title_output_label.grid(row=4, column=0, sticky=tk.E)
        self.title_output_entry = ttk.Entry(self.add_frame, width=40)
        self.title_output_entry.grid(row=4, column=1) 

        self.year_output_label = ttk.Label(self.add_frame, text='Year:')
        self.year_output_label.grid(row=5, column=0, sticky=tk.E)
        self.year_output_entry = ttk.Entry(self.add_frame, width=40)
        self.year_output_entry.grid(row=5, column=1)

        self.director_output_label = ttk.Label(self.add_frame, text='Director:')
        self.director_output_label.grid(row=6, column=0, sticky=tk.E)
        self.director_output_entry = ttk.Entry(self.add_frame, width=40)
        self.director_output_entry.grid(row=6, column=1)

        self.runtime_output_label = ttk.Label(self.add_frame, text='Runtime:')
        self.runtime_output_label.grid(row=7, column=0, sticky=tk.E)
        self.runtime_output_entry = ttk.Entry(self.add_frame, width=40)
        self.runtime_output_entry.grid(row=7, column=1)

        self.akas_output_label = ttk.Label(self.add_frame,
                                        text='Alternate Title(s):')
        self.akas_output_label.grid(row=8, column=0, sticky=tk.E)
        self.akas_output_listbox = tk.Listbox(self.add_frame, width=40)
        self.akas_output_listbox.grid(row=8, column=1)

        self.format_input_label = ttk.Label(self.add_frame, text='Format:')
        self.format_input_label.grid(row=9, column=0, sticky=tk.E)

        self.v = tk.StringVar()
        optionList = ['Choose a format', 'Blu-ray', 'DVD', 'VHS', 'Other']
        self.v.set(optionList[0])
        self.format_input_menu = ttk.OptionMenu(self.add_frame, self.v,
                                         'Choose a format', 'Blu-ray',
                                         'DVD', 'VHS', 'Other')
        self.format_input_menu.grid(row=9, column=1, sticky=(tk.W+tk.E))

        self.studio_input_label = ttk.Label(self.add_frame, text='Studio:')
        self.studio_input_label.grid(row=10, column=0, sticky=tk.E)
        self.studio_input_entry = ttk.Entry(self.add_frame, width=40)
        self.studio_input_entry.grid(row=10, column=1)
        self.studio_input_entry.bind('<Return>', self.return_list_add)

        self.location_input_label = ttk.Label(self.add_frame, text='Location:')
        self.location_input_label.grid(row=11, column=0, sticky=tk.E)
        self.location_input_entry = ttk.Entry(self.add_frame, width=40)
        self.location_input_entry.grid(row=11, column=1)
        self.location_input_entry.bind('<Return>', self.return_list_add)

        add_button = ttk.Button(self.add_frame, text='Add to List', 
                                 command=lambda: self.list_add(
                                     self.title_output_entry.get(),
                                     self.year_output_entry.get(),
                                     self.director_output_entry.get(),
                                     self.runtime_output_entry.get(),
                                     self.akas_output_listbox.get(0, tk.END),
                                     self.v.get(),
                                     self.studio_input_entry.get(),
                                     self.location_input_entry.get()))
        add_button.grid(row=11, column=2)
        add_button.bind('<Return>', self.return_list_add)

    def create_search_tab_widgets(self):
        # widgets for Search tab

        self.search_frame = ttk.Frame(self.search_tab)
        self.search_frame.grid(row=0, column=0)
        
        self.search_title_label = ttk.Label(self.search_frame, text='Title: ')
        self.search_title_label.grid(row=0, column=0, sticky=tk.E)
        self.search_title_entry = ttk.Entry(self.search_frame, width=40)
        self.search_title_entry.grid(row=0, column=1)

        self.search_year_label = ttk.Label(self.search_frame, text='Year: ')
        self.search_year_label.grid(row=1, column=0, sticky=tk.E)
        self.search_year_entry = ttk.Entry(self.search_frame, width=40)
        self.search_year_entry.grid(row=1, column=1)

        self.search_director_label = ttk.Label(self.search_frame, text='Director: ')
        self.search_director_label.grid(row=2, column=0, sticky=tk.E)
        self.search_director_entry = ttk.Entry(self.search_frame, width=40)
        self.search_director_entry.grid(row=2, column=1)

        self.search_decade_label = ttk.Label(self.search_frame, text='Decade: ')
        self.search_decade_label.grid(row=3, column=0, sticky=tk.E)
        v = tk.StringVar()
        v.set('Choose a Decade')
        self.search_decade_menu = ttk.OptionMenu(self.search_frame, v, 'Choose a Decade',
                                         'None',
                                         '1920s', '1930s', '1940s', '1950s',
                                         '1960s', '1970s', '1980s', '1990s',
                                         '2000s', '2010s', '2020s', '2030s')
        self.search_decade_menu.grid(row=3, column=1, sticky=(tk.W+tk.E))

        self.add_tab_search_button = ttk.Button(self.search_frame, text='Search', 
            command=lambda: self.search_my_list(self.search_title_entry.get(),
                                               self.search_year_entry.get(),
                                               self.search_director_entry.get(),
                                               v.get()))
        self.add_tab_search_button.grid(row=3, column=2)

        self.search_note_cell = ttk.Label(self.search_frame, text='')
        self.search_note_cell.grid(row=4, column=1)

        self.results_tree = ttk.Treeview(self.search_tab, columns=[
                                        'Year', 'Director', 'Runtime',
                                        'Format', 'Studio', 'Location'],
                                        height=16)
        self.results_tree.grid(row=1, column=0)
        self.results_tree.heading('#0', text='Title', anchor=tk.W)
        self.results_tree.heading('Year', text='Year', anchor=tk.W)
        self.results_tree.heading('Director', text='Director', anchor=tk.W)
        self.results_tree.heading('Runtime', text='Runtime', anchor=tk.W)
        self.results_tree.heading('Format', text='Format', anchor=tk.W)
        self.results_tree.heading('Studio', text='Studio', anchor=tk.W)
        self.results_tree.heading('Location', text='Location', anchor=tk.W)

        self.results_tree.column('#0', width=200, minwidth=50)
        self.results_tree.column('Year', width=50, minwidth=50)
        self.results_tree.column('Director', width=150, minwidth=50)
        self.results_tree.column('Runtime', width=50, minwidth=50)
        self.results_tree.column('Format', width=70, minwidth=50)
        self.results_tree.column('Studio', width=150, minwidth=50)
        self.results_tree.column('Location', width=100, minwidth=50)
            
    def add_tab_search(self, title, year=''):
        self.title_output_entry.delete(0, last=tk.END)
        self.year_output_entry.delete(0, last=tk.END)
        self.director_output_entry.delete(0, last=tk.END)
        self.runtime_output_entry.delete(0, last=tk.END)
        self.akas_output_listbox.delete(0, tk.END)
        self.studio_input_entry.delete(0, tk.END)
        self.location_input_entry.delete(0, tk.END)
        if (title == ''):
            self.add_note_cell['text'] = 'Please enter a title.'
            print('Please enter a title.')
        else:
            ia = imdb.IMDb()
            movie_list = ia.search_movie(self.title_input_entry.get())
            movie_list = [mov for mov in movie_list if 'year' in mov.keys()]
            final_list = []
            if (year == ''):
                final_list = movie_list
            else:
                for mov in movie_list:
                    if (int(year) == mov['year']):
                        final_list.append(mov)
            if (len(final_list) > 0):
                self.add_note_cell['text'] = 'Result Found!'
                print('Result Found!')
                movie = ia.get_movie(final_list[0].movieID)            
                self.title_output_entry.insert(2, movie['title'])
                self.year_output_entry.insert(3, movie['year'])
                if ('runtimes' in movie.keys()):
                    for rt in movie['runtimes']:
                        self.runtime_output_entry.insert(4, rt + ' ')
                else:
                    self.runtime_output_entry.insert(4, 'Unavailable')
                if ('directors' in movie.keys()):
                    director = ia.get_person(movie['directors'][0].personID)
                    self.director_output_entry.insert(5, director['name'])
                else:
                    self.director_output_entry.insert(5, 'Unavailable')
                if ('akas' in movie.keys()):
                    for tt in movie['akas']:
                        self.akas_output_listbox.insert(tk.END, tt)
                else:
                    self.akas_output_listbox.insert(5, 'Unavailable')         
            else:
                self.add_note_cell['text'] = 'No Results Found.'
                print('No Results Found.')

    def search_my_list(self, title='', year='', director='',
                      decade='Choose a Decade'):
        for row in self.results_tree.get_children():
                self.results_tree.delete(row)
        if (title == '' and year == '' and director == ''
            and (decade == 'Choose a Decade' or decade == 'None')):
            self.search_note_cell['text'] = 'Please enter a search parameter.'
            print('Please enter a search parameter.')
        else:
            conn = sql.connect('collection.db')
            c = conn.cursor()
            param_code = 0
            query = 'SELECT * FROM films WHERE '
            switcher = {}
            start = 0
            end = 0
            if (title != ''):
                param_code += 8
                title = '%' + title + '%'
            if (year != ''):
                param_code += 4
            else:
                year = '0'
            if (director != ''):
                param_code += 2
                director = '%' + director + '%'
            if (decade != 'Choose a Decade' and decade != 'None'):
                param_code += 1
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
                start = switcher[decade][0]
                end = switcher[decade][-1]

            query_switch = {
                1: 'year >= ? AND year <= ?',
                2: 'director LIKE ?',
                3: 'director LIKE ? AND year>=? AND year<=?',
                4: 'year = ?',
                5: 'year = ? AND year >= ? AND year <= ?',
                6: 'year = ? AND director LIKE ?',
                7: 'year = ? AND director LIKE ? AND year >= ? AND year <= ?',
                8: 'title LIKE ? OR akas LIKE ?',
                9: '(title LIKE ? OR akas LIKE ?) AND year >= ? AND year <= ?',
                10: '(title LIKE ? OR akas LIKE ?) AND director LIKE ?',
                11: ('''(title LIKE ? OR akas LIKE ?) AND director LIKE ?
                                                AND year >= ? AND year <= ?'''),
                12: '(title LIKE ? OR akas LIKE ?) AND year = ?',
                13: '''(title LIKE ? OR akas LIKE ?) AND year = ? AND year >= ?
                                                AND year <= ?''',
                14: '''(title LIKE ? OR akas LIKE ?) AND year = ?
                                                AND director LIKE ?''',
                15: '''(title LIKE ? OR akas LIKE ?) AND year = ?
                                                AND director LIKE ?
                                                AND year >= ? AND year <= ?'''
                }
            query += query_switch[param_code]
            if (param_code == 1):
                query += ' ORDER BY year ASC, title ASC'
            else:
                query += ' ORDER BY title ASC, year ASC'
            
            value_switch = {
                1: (str(start), str(end)),
                2: (director,),
                3: (director, str(start), str(end)),
                4: (int(year),),
                5: (int(year), str(start),str(end)),
                6: (int(year), director),
                7: (int(year), director, str(start),str(end)),
                8: (title, title),
                9: (title, title, str(start),str(end)),
                10: (title, title, director),
                11: (title, title, director,str(start), str(end)),
                12: (title, title, int(year)),
                13: (title, title, int(year), str(start), str(end)),
                14: (title, title, int(year),director),
                15: (title, title, int(year), director, str(start), str(end))
                }
            # TODO: when both decade and year are searched for, just do year
            
            c.execute(query, value_switch[param_code])
            conn.commit()
            
            results = c.fetchall()

            if (len(results) == 0):
                self.search_note_cell['text'] = 'No Results Found.'
                print('No Results Found.')
            else:
                self.search_note_cell['text'] = 'Results Found!'
                print('Results Found!')
                for i in range(len(results)):
                    parent = self.results_tree.insert('', 'end',
                                            text=results[i][0],
                                            values=results[i][1:7])
                    alt_titles = ast.literal_eval(results[i][7])
                    for tt in alt_titles:
                        self.results_tree.insert(parent, 'end', text=tt)

    def list_add(self, title, year, director, runtime, akas, form, studio,
                  location):
        if (form != 'Choose a Format' and studio != '' and location != ''):
            conn = sql.connect('collection.db')
            c = conn.cursor()
            c.execute('''SELECT title FROM films WHERE
                        title=? AND
                        year=? AND
                        director=? AND
                        format=?''',
                      (title, int(year), director, form))
            conn.commit()

            if (len(c.fetchall()) != 0):
                self.add_note_cell['text'] = 'Movie already in list.'
                print('Movie already in list.')
            else:
                c.execute('''INSERT INTO films VALUES
                        (?, ?, ?, ?, ?, ?, ?, ?)''',
                          (title, int(year), director, runtime, form, studio,
                           location, str(akas)))
                conn.commit()
                self.add_note_cell['text'] = 'Added to List!'
                print('Added to list!')
            conn.close()
        else:
            self.add_note_cell['text'] = '''Please enter Format, Studio,
                                        and/or Location'''

root = tk.Tk()
app = Application(master=root)
app.mainloop()
