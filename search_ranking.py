import pandas as pd
import os
import numpy as np
from abc import ABC, abstractmethod
 
class scoringFunction(ABC):
 
    @abstractmethod
    def ratings_score(self):
        pass

    @abstractmethod
    def search_score(self):
        pass

    @abstractmethod
    def profile_score(self):
        pass
    
    @abstractmethod
    def format_output(self):
        pass
    
    @abstractmethod
    def write_to_output(self):
        pass

    
    
class searchRank(scoringFunction):
    #class to score and rank pet sitters based on their customer ratings and profile score
    #input: dataframe of customer/sitter info
    #output: sorted and scored info stored in csv

    def __init__(self, df):
        self.df = df.sort_values("sitter")

    #No input
    #Outputs two column df of sitter names and their average rating
    #Purpose is to calculate average rating for each sitter
    def ratings_score(self):
        #takes the sitter and ratings and averages the sum total of ratings by the number of visits
        temp_df = self.df[['sitter', 'rating']]
        temp_df = temp_df.groupby('sitter').mean().reset_index()
        return temp_df
    
    #No input
    #Outputs two column df of sitter names and their profile score
    #Purpose is to calculate profile score 
    def profile_score(self):
        #instantiates temp df
        temp_df = pd.DataFrame()
        temp_df["sitter"] = self.df['sitter'].drop_duplicates().reset_index(drop=True)
        temp_df["profile_score"] = temp_df["sitter"]

        #cleans string to only be lower case characters a-z
        temp_df["profile_score"] = temp_df["profile_score"].str.replace(" ","")
        temp_df["profile_score"] = temp_df["profile_score"].str.replace(".","")
        temp_df["profile_score"] = temp_df["profile_score"].str.lower()

        #calculates profile score by finding unique letters and dividing by 26 then multiplying by 5
        temp_df["profile_score"] = (temp_df["profile_score"].apply(set).apply(len)/26) * 5
        return temp_df

    #Input is formated df with sitter_name, email, profile_scores, ratinga_scores, and stay counts
    #Output is df with calculated search score appended
    #Purpose is to calculate the search score based on sitter stay count
    def search_score(self, df):
        df["search_score"] = 0
        #if count >= 10 search score is equal to ratings average
        df["search_score"] = np.where(df["counts"] >= 10 , df["ratings_score"], df["search_score"])
        #if 0 < count < 10 search score is a weighted average calculated with both ratings and profile score
        df["search_score"] = np.where((df["counts"]  > 0) & (df["counts"]  < 10) , (df["profile_score"] * ((10 - df["counts"])/10) ) + (df["ratings_score"] * (df["counts"]/10)), df["search_score"])
        #if stays == 0 search score is equal to profile score
        df["search_score"] = np.where(df["ratings_score"] == 0 , df["profile_score"], df["search_score"])
        return df

    #No input
    #Output returns specified output df in correct format
    #Purpose is to format df so it matches specified output
    def format_output(self):
        #selecting unique user/email combo
        temp_df = self.df[["sitter", "sitter_email"]].drop_duplicates().reset_index(drop=True)

        #calculating and adding generated scores to the df
        ratings_df = self.ratings_score()
        profile_df = self.profile_score()
        temp_df["profile_score"] = profile_df["profile_score"]
        temp_df["ratings_score"] = ratings_df["rating"]

        #creating df of sitters with their total stays
        value_df = pd.DataFrame(self.df["sitter"].value_counts().reset_index())
        value_df.columns = ["sitter", "counts"]
        value_df = value_df.sort_values("sitter").reset_index(drop=True)

        
        #move counts over to temp_df and perform search scoring
        temp_df["counts"] = value_df["counts"]
        temp_df = self.search_score(temp_df)
        temp_df = temp_df.drop(columns= "counts")

        #rounding off scores
        temp_df["search_score"] = round(temp_df["search_score"], 2)
        temp_df["ratings_score"] = round(temp_df["ratings_score"], 2)
        temp_df["profile_score"] = round(temp_df["profile_score"], 2)
        
        #sorting by search score with sitter name as tiebreaker
        temp_df = temp_df.sort_values(['search_score', 'sitter'], ascending=[False, True]).reset_index(drop=True)
        return temp_df

    #Input is filename
    #Output is <filename>_output.csv
    #Purpose is to write format_output result to csv
    def write_to_output(self, file_name):
        output_df = self.format_output()
        output_df = output_df.rename(columns={'sitter': 'name', "sitter_email":"email"})

        #grabs file name in event of file_name being a file path
        if "/" in file_name:
            file_name = os.path.basename(file_name)
            
        file_name = file_name.split(".")[0]

        print("Writing df below to " + file_name + '_output.csv\n\n\n')
        print(output_df)

        #write to output using original file name + output.csv
        output_df.to_csv(file_name + '_output.csv')  
