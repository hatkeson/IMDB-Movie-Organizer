import sqlite3 as sql
import ast
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import imdb
from imdb import IMDb

class Application(tk.Frame):
    """GUI for a database of films"""
    
    def __init__(self, master=None):
        super().__init__(master)
        master.title("Movie Organizer")
        self.master = master
        self.pack()
        self.sql_create()
        self.create_widgets()

    def sql_create(self):
        """Creates a database and table if they don't already exist."""
        
        conn = sql.connect('collection.db')
        c = conn.cursor() 
        c.execute('''CREATE TABLE IF NOT EXISTS films (
                    title text NOT NULL,
                    year integer NOT NULL CHECK (year >= 1894),
                    director text NOT NULL,
                    rating text,
                    genre text,
                    runtime integer,
                    format text,
                    studio text,
                    location text,
                    cast text,
                    akas text,
                    akas_country text,
                    PRIMARY KEY(title, year, director, format))''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        """Creates two tabs and the widgets for those tabs"""
        
        self.tab_control = ttk.Notebook(self)
        self.add_tab = ttk.Frame(self.tab_control)
        self.search_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.add_tab, text='Add New Movie')
        self.tab_control.add(self.search_tab, text='Search My Collection')
        self.tab_control.pack(expand=1, fill=tk.BOTH)
        self.create_add_tab_widgets()
        self.create_search_tab_widgets()

    def return_add_tab_search(self, event):
        """Allows the user to search on the add tab with the return key"""
        
        self.add_tab_search()

    def return_list_add(self, event):
        """Allows the user to search on the add tab with the return key"""
        
        self.list_add()
        
    def return_search_my_list(self, event):
        """Allows the user to add an entry to the list with the return key"""
        
        self.search_my_list()

    def create_add_tab_widgets(self):
        """Creates the add tab widgets"""
        
        # widgets for Add tab
        self.add_frame = ttk.Frame(self.add_tab)
        self.add_frame.pack(side=tk.TOP)

        # user input frame
        self.user_input_frame = ttk.Frame(self.add_frame)
        self.user_input_frame.grid(row=0, column=0)
        self.add_tab_results_frame = ttk.Frame(self.add_frame)
        self.add_tab_results_frame.grid(row=1, column=0)
        self.add_to_list_frame = ttk.Frame(self.add_frame)
        self.add_to_list_frame.grid(row=2, column=0)
        
        self.title_input_label = ttk.Label(self.user_input_frame, text='Title:')
        self.title_input_label.grid(row=0, column=0, sticky=tk.E)
        self.title_input_entry = ttk.Entry(self.user_input_frame, width=40)
        self.title_input_entry.grid(row=0, column=1)
        self.title_input_entry.bind('<Return>', self.return_add_tab_search)
        
        self.year_input_label = ttk.Label(self.user_input_frame, text='Year:')
        self.year_input_label.grid(row=1, column=0, sticky=tk.E)
        self.year_input_entry = ttk.Entry(self.user_input_frame, width=40)
        self.year_input_entry.grid(row=1, column=1)
        self.year_input_entry.bind('<Return>', self.return_add_tab_search)

        self.add_tab_search_button = ttk.Button(self.user_input_frame,
                                                text='Search', 
            command=self.add_tab_search)
        self.add_tab_search_button.grid(row=1, column=2)
        self.add_tab_search_button.bind('<Return>', self.return_add_tab_search)

        # results table
        self.add_note_cell = ttk.Label(self.add_tab_results_frame, text='') 
        self.add_note_cell.pack()
        
        self.add_results_tree = ttk.Treeview(self.add_tab_results_frame,
                                             columns=[
                                                 'Year', 'Director',
                                                 'Rating', 'Genre', 'Runtime']
                                             )
        self.add_results_tree.pack()
        self.add_results_tree.heading('#0', text='Title', anchor=tk.W)
        self.add_results_tree.heading('Year', text='Year', anchor=tk.W)
        self.add_results_tree.heading('Director', text='Director', anchor=tk.W)
        self.add_results_tree.heading('Rating', text='Rating', anchor=tk.W)
        self.add_results_tree.heading('Genre', text='Genre', anchor=tk.W)
        self.add_results_tree.heading('Runtime', text='Runtime', anchor=tk.W)

        self.add_results_tree.column('#0', width=200, minwidth=50)
        self.add_results_tree.column('Year', width=50, minwidth=50)
        self.add_results_tree.column('Director', width=200, minwidth=50)
        self.add_results_tree.column('Rating', width=50, minwidth=50)
        self.add_results_tree.column('Genre', width=100, minwidth=50)
        self.add_results_tree.column('Runtime', width=50, minwidth=50)

        self.add_select_button = ttk.Button(self.add_tab_results_frame,
                                            text='Select',
                                            command=self.add_select)
        self.add_select_button.pack()

        # Add to List frame
        self.title_output_label = ttk.Label(self.add_to_list_frame,
                                            text='Title:')
        self.title_output_label.grid(row=0, column=0, sticky=tk.E)
        self.title_output_entry = ttk.Entry(self.add_to_list_frame, width=40)
        self.title_output_entry.grid(row=0, column=1) 

        self.year_output_label = ttk.Label(self.add_to_list_frame, text='Year:')
        self.year_output_label.grid(row=1, column=0, sticky=tk.E)
        self.year_output_entry = ttk.Entry(self.add_to_list_frame, width=40)
        self.year_output_entry.grid(row=1, column=1)

        self.director_output_label = ttk.Label(self.add_to_list_frame,
                                               text='Director:')
        self.director_output_label.grid(row=2, column=0, sticky=tk.E)
        self.director_output_entry = ttk.Entry(self.add_to_list_frame, width=40)
        self.director_output_entry.grid(row=2, column=1)

        self.cast_output_label = ttk.Label(self.add_to_list_frame,
                                               text='Cast:')
        self.cast_output_label.grid(row=3, column=2, sticky=tk.E)
        self.cast_output_text = tk.Text(self.add_to_list_frame, width=50,
                                          height=5, wrap=tk.NONE)
        self.cast_output_text.grid(row=3, column=3)

        self.rating_output_label = ttk.Label(self.add_to_list_frame,
                                               text='Rating:')
        self.rating_output_label.grid(row=0, column=2, sticky=tk.E)
        self.rating_output_entry = ttk.Entry(self.add_to_list_frame, width=40)
        self.rating_output_entry.grid(row=0, column=3)

        self.genre_output_label = ttk.Label(self.add_to_list_frame,
                                               text='Genre:')
        self.genre_output_label.grid(row=1, column=2, sticky=tk.E)
        self.genre_output_entry = ttk.Entry(self.add_to_list_frame, width=40)
        self.genre_output_entry.grid(row=1, column=3)

        self.runtime_output_label = ttk.Label(self.add_to_list_frame,
                                              text='Runtime:')
        self.runtime_output_label.grid(row=2, column=2, sticky=tk.E)
        self.runtime_output_entry = ttk.Entry(self.add_to_list_frame, width=40)
        self.runtime_output_entry.grid(row=2, column=3)

        self.akas_output_label = ttk.Label(self.add_to_list_frame,
                                        text='Alternate Title(s):')
        self.akas_output_label.grid(row=3, column=0, sticky=tk.E)
        self.akas_output_text = tk.Text(self.add_to_list_frame, width=50,
                                              height=5, wrap=tk.NONE)
        self.akas_output_text.grid(row=3, column=1)

        self.format_input_label = ttk.Label(self.add_to_list_frame,
                                            text='Format:')
        self.format_input_label.grid(row=4, column=0, sticky=tk.E)

        self.v = tk.StringVar()
        optionList = ['Choose a format', 'Blu-ray', 'DVD', 'VHS', 'Other']
        self.v.set(optionList[0])
        self.format_input_menu = ttk.OptionMenu(self.add_to_list_frame, self.v,
                                         'Choose a format', 'Blu-ray',
                                         'DVD', 'VHS', 'Other')
        self.format_input_menu.grid(row=4, column=1, sticky=(tk.W+tk.E))

        self.studio_input_label = ttk.Label(self.add_to_list_frame,
                                            text='Studio:')
        self.studio_input_label.grid(row=5, column=0, sticky=tk.E)
        self.studio_input_entry = ttk.Entry(self.add_to_list_frame, width=40)
        self.studio_input_entry.grid(row=5, column=1)
        self.studio_input_entry.bind('<Return>', self.return_list_add)

        self.location_input_label = ttk.Label(self.add_to_list_frame,
                                              text='Location:')
        self.location_input_label.grid(row=6, column=0, sticky=tk.E)
        self.location_input_entry = ttk.Entry(self.add_to_list_frame, width=40)
        self.location_input_entry.grid(row=6, column=1)
        self.location_input_entry.bind('<Return>', self.return_list_add)

        add_button = ttk.Button(self.add_to_list_frame, text='Add to List', 
                                 command=self.list_add)
        add_button.grid(row=6, column=2)
        add_button.bind('<Return>', self.return_list_add)

    def create_search_tab_widgets(self):
        """Creates the search tab widgets"""
        
        self.search_frame = ttk.Frame(self.search_tab)
        self.search_results_frame = ttk.Frame(self.search_tab)
        self.search_edit_frame = ttk.Frame(self.search_tab)
        
        self.search_frame.pack()
        self.search_results_frame.pack()
        self.search_edit_frame.pack(side=tk.RIGHT)
        
        self.search_title_label = ttk.Label(self.search_frame, text='Title: ')
        self.search_title_label.grid(row=0, column=0, sticky=tk.E)
        self.search_title_entry = ttk.Entry(self.search_frame, width=40)
        self.search_title_entry.grid(row=0, column=1)
        self.search_title_entry.bind('<Return>', self.return_search_my_list)

        self.search_year_label = ttk.Label(self.search_frame, text='Year: ')
        self.search_year_label.grid(row=1, column=0, sticky=tk.E)
        self.search_year_entry = ttk.Entry(self.search_frame, width=40)
        self.search_year_entry.grid(row=1, column=1)
        self.search_year_entry.bind('<Return>', self.return_search_my_list)

        self.search_director_label = ttk.Label(self.search_frame,
                                               text='Director: ')
        self.search_director_label.grid(row=2, column=0, sticky=tk.E)
        self.search_director_entry = ttk.Entry(self.search_frame, width=40)
        self.search_director_entry.grid(row=2, column=1)
        self.search_director_entry.bind('<Return>', self.return_search_my_list)

        self.search_cast_label = ttk.Label(self.search_frame, text='Cast: ')
        self.search_cast_label.grid(row=3, column=0, sticky=tk.E)
        self.search_cast_entry = ttk.Entry(self.search_frame, width=40)
        self.search_cast_entry.grid(row=3, column=1)
        self.search_cast_entry.bind('<Return>', self.return_search_my_list)

        self.search_rating_label = ttk.Label(self.search_frame, text='Rating: ')
        self.search_rating_label.grid(row=4, column=0, sticky=tk.E)
        self.search_rating_entry = ttk.Entry(self.search_frame, width=40)
        self.search_rating_entry.grid(row=4, column=1)
        self.search_rating_entry.bind('<Return>', self.return_search_my_list)

        self.search_genre_label = ttk.Label(self.search_frame, text='Genre: ')
        self.search_genre_label.grid(row=5, column=0, sticky=tk.E)
        self.search_genre_entry = ttk.Entry(self.search_frame, width=40)
        self.search_genre_entry.grid(row=5, column=1)
        self.search_genre_entry.bind('<Return>', self.return_search_my_list)

        self.search_decade_label = ttk.Label(self.search_frame, text='Decade: ')
        self.search_decade_label.grid(row=6, column=0, sticky=tk.E)
        self.dec_val = tk.StringVar()
        self.dec_val.set('Choose a Decade')
        self.search_decade_menu = ttk.OptionMenu(self.search_frame,
                                                 self.dec_val,
                                                 'Choose a Decade','None',
                                                 '1920s', '1930s', '1940s',
                                                 '1950s', '1960s', '1970s',
                                                 '1980s', '1990s', '2000s',
                                                 '2010s', '2020s', '2030s')
        self.search_decade_menu.grid(row=6, column=1, sticky=(tk.W+tk.E))
        self.search_decade_menu.bind('<Return>', self.return_search_my_list)

        self.add_tab_search_button = ttk.Button(self.search_frame, text='Search',
                                                command=self.search_my_list)
        self.add_tab_search_button.grid(row=6, column=2)
        self.add_tab_search_button.bind('<Return>', self.return_search_my_list)

        self.search_note_cell = ttk.Label(self.search_frame, text='')
        self.search_note_cell.grid(row=7, column=1)

        self.results_tree = ttk.Treeview(self.search_results_frame, columns=[
                                        'Year', 'Director',
                                        'Rating', 'Genre', 'Runtime',
                                        'Format', 'Studio', 'Location'],
                                        height=16)
        self.results_tree.grid(row=0, column=0)
        self.results_tree.heading('#0', text='Title', anchor=tk.W)
        self.results_tree.heading('Year', text='Year', anchor=tk.W)
        self.results_tree.heading('Director', text='Director', anchor=tk.W)
        self.results_tree.heading('Rating', text='Rating', anchor=tk.W)
        self.results_tree.heading('Genre', text='Genre', anchor=tk.W)
        self.results_tree.heading('Runtime', text='Runtime', anchor=tk.W)
        self.results_tree.heading('Format', text='Format', anchor=tk.W)
        self.results_tree.heading('Studio', text='Studio', anchor=tk.W)
        self.results_tree.heading('Location', text='Location', anchor=tk.W)

        self.results_tree.column('#0', width=200, minwidth=50)
        self.results_tree.column('Year', width=50, minwidth=50)
        self.results_tree.column('Director', width=150, minwidth=50)
        self.results_tree.column('Rating', width=50, minwidth=50)
        self.results_tree.column('Genre', width=200, minwidth=50)
        self.results_tree.column('Runtime', width=50, minwidth=50)
        self.results_tree.column('Format', width=70, minwidth=50)
        self.results_tree.column('Studio', width=150, minwidth=50)
        self.results_tree.column('Location', width=100, minwidth=50)

        self.search_edit_button = ttk.Button(self.search_edit_frame,
                                             text='Edit',
                                             command=self.edit_entry)
        self.search_edit_button.grid(row=0, column=0)

        self.search_delete_button = ttk.Button(self.search_edit_frame,
                                               text='Delete',
                                               command=self.delete_entry)
        self.search_delete_button.grid(row=0, column=1)
            
    def add_tab_search(self):
        """Searches IMDB for the input title (required)
        and the year(optional)"""
        
        title = self.title_input_entry.get(),
        year = self.year_input_entry.get()
       
        self.title_output_entry.delete(0, last=tk.END)
        self.year_output_entry.delete(0, last=tk.END)
        self.director_output_entry.delete(0, last=tk.END)
        self.cast_output_text.delete(1.0, tk.END)
        self.rating_output_entry.delete(0, last=tk.END)
        self.genre_output_entry.delete(0, last=tk.END)
        self.runtime_output_entry.delete(0, last=tk.END)
        self.akas_output_text.delete(1.0, tk.END)
        self.add_results_tree.delete(*self.add_results_tree.get_children())
        self.studio_input_entry.delete(0, tk.END)
        self.location_input_entry.delete(0, tk.END)
        if (title == ''):
            self.add_note_cell['text'] = 'Please enter a title.'
            print('Please enter a title.')
        else:
            ia = imdb.IMDb()
            movie_list = ia.search_movie(self.title_input_entry.get(),
                                         results=10)
            movie_list = [mov for mov in movie_list if 'year' in mov.keys()]
            final_list = []
            if (year == ''):
                final_list = movie_list
            else:
                for mov in movie_list:
                    if (int(year) == mov['year']):
                        final_list.append(mov)
            if (len(final_list) > 0):
                self.add_note_cell['text'] = 'Results Found!'
                print('Result Found!')
                for mov in final_list:
                    movie = ia.get_movie(mov.movieID)
                    m = [movie['title'], movie['year']]
                    if ('directors' in movie.keys()):
                        dir_nm = []
                        for i in movie['directors']:
                            dir_nm.append(i.get('name'))
                        dir_str = ''
                        dir_str = ', '.join(dir_nm)
                        m.append(dir_str)
                    else:
                        m.append('Unavailable')
                    if ('certificates' in movie.keys()):
                        rat = ''
                        for crt in movie['certificates'][::-1]:
                            if (crt[0:14] == 'United States:'):
                                rat = crt[14:]
                                break
                        if (rat != ''):
                            m.append(rat)
                        else:
                            m.append('Unavailable')
                    else:
                        m.append('Unavailable')
                    if ('genres' in movie.keys()):
                        m.append(', '.join(movie['genres']))
                    else:
                        m.append('Unavailable')
                    if ('runtimes' in movie.keys()):
                        m.append(movie['runtimes'])
                    else:
                        m.append('Unavailable')
                    par = self.add_results_tree.insert('', 'end',
                                            text=m[0],
                                            values=m[1:7])
                    if ('akas' in movie.keys()):
                        akas_row = self.add_results_tree.insert(par, 'end',
                                                                text='Alternate Titles')
                        for tt in movie['akas']:
                            self.add_results_tree.insert(akas_row, 'end', text=tt)
                    if ('cast' in movie.keys()):
                        cast_row = self.add_results_tree.insert(par, 'end',
                                                                    text='Cast')
                        c = 0
                        if (len(movie['cast']) >= 5):
                            c = 5
                        else:
                            c = len(movie['cast'])
                        for i in range(c):
                            self.add_results_tree.insert(cast_row, 'end',
                                                         text=movie['cast'][i].get('name'))
            else:
                self.add_note_cell['text'] = 'No Results Found.'
                print('No Results Found.')

    def add_select(self):
        """Shows details about a selected title"""
        
        self.title_output_entry.delete(0, last=tk.END)
        self.year_output_entry.delete(0, last=tk.END)
        self.director_output_entry.delete(0, last=tk.END)
        self.cast_output_text.delete(1.0, tk.END)
        self.rating_output_entry.delete(0, last=tk.END)
        self.genre_output_entry.delete(0, last=tk.END)
        self.runtime_output_entry.delete(0, last=tk.END)
        self.akas_output_text.delete(1.0, tk.END)
        self.studio_input_entry.delete(0, tk.END)
        self.location_input_entry.delete(0, tk.END)
        
        cur_item = self.add_results_tree.focus()
        if (cur_item != ''):
            item_dict = self.add_results_tree.item(cur_item)
            print(item_dict)
            self.title_output_entry.insert(0, item_dict['text'])
            self.year_output_entry.insert(0, item_dict['values'][0])
            self.director_output_entry.insert(0, item_dict['values'][1])
            self.rating_output_entry.insert(0, item_dict['values'][2])
            self.genre_output_entry.insert(0, item_dict['values'][3])
            self.runtime_output_entry.insert(0, item_dict['values'][4])

            for child in self.add_results_tree.get_children(cur_item):
                child_dict = self.add_results_tree.item(child)
                gchild_names = []
                for gchild in self.add_results_tree.get_children(child):
                    gchild_dict = self.add_results_tree.item(gchild)
                    gchild_names.append(gchild_dict['text'])
                gchild_names_str = '\n'.join(gchild_names)
                if (child_dict['text'] == 'Alternate Titles'):
                    self.akas_output_text.insert(tk.END,
                                                 gchild_names_str)
                else:
                    self.cast_output_text.insert(tk.END,
                                                 gchild_names_str)              
        else:
            self.add_note_cell['text'] = 'Please highlight a result.'

    def search_my_list(self):
        """Searches the list of owned films"""
        
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)
        
        title = self.search_title_entry.get()
        year = self.search_year_entry.get()
        director = self.search_director_entry.get()
        cast = self.search_cast_entry.get()
        rating = self.search_rating_entry.get()
        genre = self.search_genre_entry.get()
        decade = self.dec_val.get()
        
        if (title == '' and year == '' and director == '' and
            cast == '' and rating == '' and genre == '' and
            (decade == 'Choose a Decade' or decade == 'None')):
            self.search_note_cell['text'] = 'Please enter a search parameter.'
            print('Please enter a search parameter.')
        else:
            conn = sql.connect('collection.db')
            c = conn.cursor()

            query = '''SELECT * FROM films WHERE '''
            sub_query = []
            vals = []
            start = 0
            end = 0
            if (title != ''):
                sub_query.append('(title LIKE ? OR akas LIKE ?)')
                vals.append('%' + title + '%')
                vals.append('%' + title + '%')
            if (year != ''):
                sub_query.append('year = ?')
                vals.append(year)
            else:
                year = '0'
            if (director != ''):
                sub_query.append('director LIKE ?')
                vals.append('%' + director + '%')
            if (cast != ''):
                sub_query.append('"cast" LIKE ?')
                vals.append('%' + cast + '%')
            if (rating != ''):
                sub_query.append('rating = ?')
                vals.append(rating)
            if (genre != ''):
                sub_query.append('genre LIKE ?')
                vals.append('%' + genre + '%')
            if (decade != 'Choose a Decade' and decade != 'None'):
                sub_query.append('year >= ? AND year <= ?')
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
                vals.append(start)
                vals.append(end)

            sub_query_str = ' AND '.join(sub_query)
            query += sub_query_str
            
            if (len(vals) == 1 and vals[0] == decade):
                query += ''' ORDER BY year ASC, (CASE
                            WHEN title LIKE 'the %' THEN substr(title, 5)
                            WHEN title LIKE 'a %' THEN substr(title, 3)
                            WHEN title LIKE 'an %' THEN substr(title, 4)
                            ELSE title
                            END) ASC'''
            else:
                query += ''' ORDER BY (CASE
                            WHEN title LIKE 'the %' THEN substr(title, 5)
                            WHEN title LIKE 'a %' THEN substr(title, 3)
                            WHEN title LIKE 'an %' THEN substr(title, 4)
                            ELSE title
                            END) ASC, year ASC'''
            c.execute(query, vals)
            conn.commit()
            
            results = c.fetchall()

            c.execute('SELECT COUNT(*) FROM films')
            conn.commit()

            total_count = c.fetchone()
            conn.close()

            res_count = len(results)
            self.search_note_cell['text'] = ('Showing ' + str(res_count) +
                                             ' out of ' + str(total_count[0])
                                             + ' entries.')
            for i in range(res_count):
                parent = self.results_tree.insert('', 'end',
                                        text=results[i][0],
                                        values=(results[i][1:9]))
                alt_row = self.results_tree.insert(parent, 'end',
                                                   text='Alternate Titles',
                                                   open=True)
                cast_row = self.results_tree.insert(parent, 'end',
                                                   text='Cast',
                                                    open=True)
                cst = results[i][9].split('\n')
                cst.pop()
                alt = ast.literal_eval(results[i][10])
                alt_country = ast.literal_eval(results[i][11])
                alt_combined = []
                for i in range(len(alt)):
                    alt_combined.append(alt[i] + ' ' + alt_country[i])
                for tt in alt_combined:
                    self.results_tree.insert(alt_row, 'end', text=tt)
                for n in cst:
                    self.results_tree.insert(cast_row, 'end', text=n)

    def list_add(self):
        """Adds a film to the list"""
        
        title = self.title_output_entry.get()
        year = self.year_output_entry.get()
        director = self.director_output_entry.get()
        cast = self.cast_output_text.get(1.0, tk.END)
        rating = self.rating_output_entry.get()
        genre = self.genre_output_entry.get()
        runtime = self.runtime_output_entry.get()
        akas = self.akas_output_text.get(1.0, tk.END)
        form = self.v.get()
        studio = self.studio_input_entry.get()
        location = self.location_input_entry.get()
        
        if (form != 'Choose a Format' and studio != '' and location != ''):
            conn = sql.connect('collection.db')
            c = conn.cursor()
            c.execute('''SELECT title FROM films WHERE
                        title=? AND
                        year=? AND
                        director=? AND
                        format=?''',
                      (title, year, director, form))
            conn.commit()

            if (len(c.fetchall()) != 0):
                self.add_note_cell['text'] = 'Movie already in list.'
                print('Movie already in list.')
            else:
                akas_list = []
                akas_country_list = []
                if (len(akas) > 0):
                    akas_raw = akas.split('\n')
                    akas_raw.pop()
                    paren_idx = 0
                    for n in akas_raw:
                        paren_idx = n.index('(')
                        akas_list.append(n[:paren_idx - 1])
                        akas_country_list.append(n[paren_idx:])
                c.execute('''INSERT INTO films VALUES
                        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (title, year, director, rating, genre, runtime,
                           form, studio, location, cast, str(akas_list),
                           str(akas_country_list)))
                conn.commit()
                self.add_note_cell['text'] = 'Added to List!'
                print('Added to list!')
            conn.close()
        else:
            self.add_note_cell['text'] = ('Please enter Format, Studio, '
                                          'and/or Location')

    def delete_entry(self):
        """Deletes an entry from the list"""
        
        if (self.results_tree.focus() != ''):
            if tk.messagebox.askyesno(title='Delete Entry',
                                      message='Are you sure '
                                      'you want to delete this entry?',
                                      parent=self.master):
                cur_item = self.results_tree.focus()
                item_dict = self.results_tree.item(cur_item)
                title = item_dict['text']
                year = item_dict['values'][0]
                director = item_dict['values'][1]
                form = item_dict['values'][5]
                
                conn = sql.connect('collection.db')
                c = conn.cursor()
                q = '''DELETE FROM films WHERE title = ?
                        AND year = ? 
                        AND director = ?
                        AND format = ?'''
                v = [title, year, director, form]
                c.execute(q, v)
                conn.commit()
                conn.close()
                
                self.results_tree.delete(cur_item)
                self.search_note_cell['text'] = 'Entry Deleted!'
        else:
            self.search_note_cell['text'] = ('Please select a result from '
                                             'the table.')

    def edit_entry(self):
        """Pulls up a new window where the user can alter an entry"""
        
        if (self.results_tree.focus() != ''):
            # place widgets
            self.edit_window = tk.Toplevel(self.master)
            self.edit_window.title('Edit Entry')
            self.edit_frame = ttk.Frame(self.edit_window)
            self.edit_confirm_cancel = ttk.Frame(self.edit_frame)
            self.edit_frame.pack()
            self.edit_confirm_cancel.grid(row=6, column=3)

            self.edit_title_output_label = ttk.Label(self.edit_frame,
                                                text='Title:')
            self.edit_title_output_label.grid(row=0, column=0, sticky=tk.E)
            self.edit_title_output_entry = ttk.Entry(self.edit_frame, width=40)
            self.edit_title_output_entry.grid(row=0, column=1) 

            self.edit_year_output_label = ttk.Label(self.edit_frame,
                                                    text='Year:')
            self.edit_year_output_label.grid(row=1, column=0, sticky=tk.E)
            self.edit_year_output_entry = ttk.Entry(self.edit_frame, width=40)
            self.edit_year_output_entry.grid(row=1, column=1)

            self.edit_director_output_label = ttk.Label(self.edit_frame,
                                                   text='Director:')
            self.edit_director_output_label.grid(row=2, column=0, sticky=tk.E)
            self.edit_director_output_entry = ttk.Entry(self.edit_frame,
                                                        width=40)
            self.edit_director_output_entry.grid(row=2, column=1)

            self.edit_cast_output_label = ttk.Label(self.edit_frame,
                                                   text='Cast:')
            self.edit_cast_output_label.grid(row=3, column=2, sticky=tk.E)
            self.edit_cast_output_text = tk.Text(self.edit_frame, width=50,
                                              height=5)
            self.edit_cast_output_text.grid(row=3, column=3)

            self.edit_rating_output_label = ttk.Label(self.edit_frame,
                                                   text='Rating:')
            self.edit_rating_output_label.grid(row=0, column=2, sticky=tk.E)
            self.edit_rating_output_entry = ttk.Entry(self.edit_frame, width=40)
            self.edit_rating_output_entry.grid(row=0, column=3)

            self.edit_genre_output_label = ttk.Label(self.edit_frame,
                                                   text='Genre:')
            self.edit_genre_output_label.grid(row=1, column=2, sticky=tk.E)
            self.edit_genre_output_entry = ttk.Entry(self.edit_frame, width=40)
            self.edit_genre_output_entry.grid(row=1, column=3)

            self.edit_runtime_output_label = ttk.Label(self.edit_frame,
                                                  text='Runtime:')
            self.edit_runtime_output_label.grid(row=2, column=2, sticky=tk.E)
            self.edit_runtime_output_entry = ttk.Entry(self.edit_frame,
                                                       width=40)
            self.edit_runtime_output_entry.grid(row=2, column=3)

            self.edit_akas_output_label = ttk.Label(self.edit_frame,
                                            text='Alternate Title(s):')
            self.edit_akas_output_label.grid(row=3, column=0, sticky=tk.E)
            self.edit_akas_output_text = tk.Text(self.edit_frame, width=50,
                                                  height=5)
            self.edit_akas_output_text.grid(row=3, column=1)

            self.edit_format_input_label = ttk.Label(self.edit_frame,
                                                text='Format:')
            self.edit_format_input_label.grid(row=4, column=0, sticky=tk.E)

            self.edit_v = tk.StringVar()
            optionList = ['Choose a format', 'Blu-ray', 'DVD', 'VHS', 'Other']
            self.edit_v.set(optionList[0])
            self.edit_format_input_menu = ttk.OptionMenu(self.edit_frame,
                                                         self.edit_v,
                                             'Choose a format', 'Blu-ray',
                                             'DVD', 'VHS', 'Other')
            self.edit_format_input_menu.grid(row=4, column=1, sticky=(tk.W+tk.E))

            self.edit_studio_input_label = ttk.Label(self.edit_frame,
                                                text='Studio:')
            self.edit_studio_input_label.grid(row=5, column=0, sticky=tk.E)
            self.edit_studio_input_entry = ttk.Entry(self.edit_frame, width=40)
            self.edit_studio_input_entry.grid(row=5, column=1)

            self.edit_location_input_label = ttk.Label(self.edit_frame,
                                                  text='Location:')
            self.edit_location_input_label.grid(row=6, column=0, sticky=tk.E)
            self.edit_location_input_entry = ttk.Entry(self.edit_frame,
                                                       width=40)
            self.edit_location_input_entry.grid(row=6, column=1)


            self.edit_cancel_button = ttk.Button(self.edit_confirm_cancel,
                                                 text='Cancel',
                                                 command=self.edit_cancel)
            self.edit_confirm_button = ttk.Button(self.edit_confirm_cancel,
                                                  text='Confirm',
                                                  command=self.edit_confirm)
            self.edit_cancel_button.pack(side=tk.LEFT)
            self.edit_confirm_button.pack(side=tk.RIGHT)

            cur_item = self.results_tree.focus()
            item_dict = self.results_tree.item(cur_item)
            print(item_dict)

            self.edit_title_output_entry.insert(0, item_dict['text'])
            self.edit_year_output_entry.insert(0, item_dict['values'][0])
            self.edit_director_output_entry.insert(0, item_dict['values'][1])
            self.edit_rating_output_entry.insert(0, item_dict['values'][2])
            self.edit_genre_output_entry.insert(0, item_dict['values'][3])
            self.edit_runtime_output_entry.insert(0, item_dict['values'][4])
            self.edit_v.set(item_dict['values'][5])
            self.edit_studio_input_entry.insert(0, item_dict['values'][6])
            self.edit_location_input_entry.insert(0, item_dict['values'][7])

            for child in self.results_tree.get_children(cur_item):
                    child_dict = self.results_tree.item(child)
                    gchild_names = []
                    for gchild in self.results_tree.get_children(child):
                        gchild_dict = self.results_tree.item(gchild)
                        gchild_names.append(gchild_dict['text'])
                    gchild_names_str = '\n'.join(gchild_names)
                    if (child_dict['text'] == 'Alternate Titles'):
                        self.edit_akas_output_text.insert(tk.END,
                                                     gchild_names_str)
                    else:
                        self.edit_cast_output_text.insert(tk.END,
                                                     gchild_names_str)
        else:
            self.search_note_cell['text'] = ('Please select a result from '
                                             'the table.')
        
    def edit_cancel(self):
        """Cancels the edit window"""
        
        self.edit_window.destroy()

    def edit_confirm(self):
        """Sends an update command to the database"""
        
        orig_item = self.results_tree.focus()
        orig_item_dict = self.results_tree.item(orig_item)

        akas_list = []
        akas_country_list = []
        akas_raw = self.edit_akas_output_text.get(1.0, tk.END).split('\n')
        akas_raw.pop()
        paren_idx = 0
        for n in akas_raw:
            paren_idx = n.index('(')
            akas_list.append(n[:paren_idx - 1])
            akas_country_list.append(n[paren_idx:])

        vals = [self.edit_title_output_entry.get(),
                int(self.edit_year_output_entry.get()),
                self.edit_director_output_entry.get(),
                self.edit_rating_output_entry.get(),
                self.edit_genre_output_entry.get(),
                int(self.edit_runtime_output_entry.get()),
                self.edit_v.get(),
                self.edit_studio_input_entry.get(),
                self.edit_location_input_entry.get(),
                self.edit_cast_output_text.get(1.0, tk.END),
                str(akas_list),
                str(akas_country_list),
                orig_item_dict['text'],
                orig_item_dict['values'][0],
                orig_item_dict['values'][1]]
        
        conn = sql.connect('collection.db')
        c = conn.cursor()
        c.execute('''UPDATE films SET
                title=?,
                year=?,
                director=?,
                rating=?,
                genre=?,
                runtime=?,
                format=?,
                studio=?,
                location=?,
                "cast"=?,
                akas=?,
                akas_country=?
                WHERE
                title=? AND
                year=? AND
                director = ?''',
                vals)
        
        conn.commit()
        conn.close()          
        
        self.edit_window.destroy()
        self.search_my_list()
        self.search_note_cell['text'] = 'Entry Updated!' 

root = tk.Tk()
app = Application(master=root)
app.mainloop()
