# IMDB-Movie-Organizer
This program prompts the user for a movie title (required) and a year (optional) and searches IMDB with those parameters. 
It then displays information about the results, including: 
* Title
* Alternate Titles
* Director
* Year
* Runtime of all versions
The user is then given the option to add information on what format they own the title in and what release studio its from, and export the results to a tsv file.
The user can later search this list by any combination of the following: title, director, year, or decade.

TODO:
* Speed up searching datasets (current search time = 45 seconds)
  * reducing dataset sizes by deleting irrelevant entries
    * look through name.basics, filter out any entries that are not also present in title.crew
  * organizing title.basics alphabetically by title?
  * implement binary search 
  * use a while not found loop instead of a for loop
* Create Search tab widgets
  * Search by Title
  * Search by Year
  * Search by Director
  * Search by Decade
  * Search by Runtime?
* addToList Button
* show alternative titles (title.akas)
* Progress bar?
