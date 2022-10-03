import pandas as pd
from os.path import exists
from search_ranking import searchRank

while True:
    #Takes user input
    file_name = input("Type 'exit' to exit program\nPlease enter your filename: ")

    #Breaks loop on user command
    if file_name == "exit":
        print("Operation Finished")
        break
    
    #Check if file exists to call search ranking, if not loop through again
    if exists(file_name):
        df = pd.read_csv(file_name, index_col=None)
        search_rank = searchRank(df)
        search_rank.write_to_output(file_name) 
    else:
        print("File does not exist, please try again")
        
    print("\n\n\n")
