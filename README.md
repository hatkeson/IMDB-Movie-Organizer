# IMDB-Movie-Organizer
This program prompts the user for a movie title (required) and a year (optional) and searches IMDB with those parameters. 
It then displays information about the results, including: 
* Title
* Alternate Titles
* Director
* Year
* Runtime

The user is then given the option to add information on what format they own the title in and what release studio its from, and export the results to a tsv file.
The user can later search this list by any combination of the following: title, director, year, or decade.

TODO:
* Implement UPDATE and DELETE functions
* Have initial search show multiple results in a treeview
* Make it so that "the" "a" "an" aren't counted for alphabetizing
