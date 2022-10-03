import unittest
from search_ranking import searchRank
import pandas as pd
from os.path import exists

class TestScoringFunctions(unittest.TestCase):

    #tests ratings score calculation
    def test_ratings_score(self):
        try:
            df = pd.read_csv("test.csv", index_col=None)
            search_rank = searchRank(df)
            df = search_rank.ratings_score()
            assert(df.iloc[[2]]["rating"].values[0] == 2.5)

            print("test_search_rank: Passed")
            
        except AssertionError as msg:
            raise Exception("Incorrect Average Calculated")
    
    #tests profile score calculation 
    def test_profile_score(self):
        try:
            df = pd.read_csv("test.csv", index_col=None)
            search_rank = searchRank(df)
            df = search_rank.profile_score()
            self.assertTrue(df.iloc[[2]]["profile_score"].values[0] == (4/26)*5)

            print("test_profile_rank: Passed")
            
        except AssertionError:
            raise Exception("Incorrect Average Calculated")

    #tests output format function
    def test_format_output(self):
        try:
            df = pd.read_csv("test.csv", index_col=None)
            search_rank = searchRank(df)
            df = search_rank.format_output()
            assert df.shape == (6,5), "Incorrect number of results returned"

            print("test_format_output: Passed")

        except AssertionError as msg:
            raise Exception(msg)

    #tests scoring for sitters with above ten stays: ratings only score
    def test_search_score_above_10(self):
        try:
            df = pd.read_csv("test.csv", index_col=None)
            search_rank = searchRank(df)
            df = search_rank.format_output()
            
            assert df.iloc[[0]]["sitter"].values[0] == "John", "Incorrect Search Ranking for count > 10"
            assert df.iloc[[0]]["search_score"].values[0] == 5, "Incorrect Search Score for count > 10"

            print("test_search_score_above_10: Passed")
            
        except AssertionError as msg:
            raise Exception(msg)

    #tests scoring for sitters that meet weighted score values
    def test_weighted_search_score(self):
        try:
            df = pd.read_csv("test.csv", index_col=None)
            search_rank = searchRank(df)
            df = search_rank.format_output()
            
            assert df.iloc[[1]]["sitter"].values[0] == "Margaret", "Incorrect Search Ranking for 0 < count < 10"
            assert round(df.iloc[[1]]["search_score"].values[0],2) == 1.52, "Incorrect Search Score 0 < count < 10"

            print("test_weighted_search_score: Passed")
            
        except AssertionError as msg:
            raise Exception(msg)

    #tests scoring for sitters that have no ratings
    def test_no_ratings(self):
        try:
            df = pd.read_csv("test.csv", index_col=None)
            search_rank = searchRank(df)
            df = search_rank.format_output()
            
            assert df.iloc[[5]]["sitter"].values[0] == "Josie", "Incorrect Search Ranking for no ratings"
            assert round(df.iloc[[5]]["search_score"].values[0],2) == 0.96, "Incorrect Search Score for no ratings"

            print("test_no_ratings: Passed")
            
        except AssertionError as msg:
            raise Exception(msg)
        
    #tests output function
    def test_output_csv(self):
        try:
            df = pd.read_csv("test.csv", index_col=None)
            search_rank = searchRank(df)
            search_rank.write_to_output("test.csv")
            
            assert exists("test_output.csv"), "No output file was generated"

            print("test_output_csv: Passed")
            
        except AssertionError as msg:
            raise Exception(msg)
        
        
        

if __name__ == '__main__':
    unittest.main(failfast=False)
