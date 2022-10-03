# search-ranking
Code to design a businesses search algorithm and calculate search and profile scores to return a table sorted by designated relevancy guidelines.

Ingest.py takes the user input in the form of a string designating a path to a csv file. 

Search_ranking.py performs the calculations behind the ranking scores and outputs them into another csv file, sorting the inputted data by relevancy.

Test.csv contains example data. Note that only the specified relevant columns are returned.

Test_output.csv is a real generated output file generated from Test.csv demonstrating how the search ranking works. Tiebreakers in search scoring are broken by the users name in alphabetical order.

Testing_functions.py is testing all the defined calculation and output functions. Please note hardcoded values were used as this is common practice in my field. It is also possible to take out hardcoding if different testing standards are defined.
