from collections import Counter
from itertools import permutations
import random
from preference_matrix import PreferenceMatrix
from vote_counter import VoteCounter

class TVA:
    def __init__(self, n, m):
        self.n = n  # Number of voters
        self.m = m  # Number of candidates
        self.preference_matrix = None
        self.result_tuple = [[] for _ in range(self.n)]

    def setup(self):
        alternatives = [chr(65 + i) for i in range(self.m)]  # Candidate names: A, B, C, etc.
        votes = [random.sample(alternatives, len(alternatives)) for _ in range(self.n)]
        self.preference_matrix = PreferenceMatrix(votes)

    def get_winner(self, scheme):
        """Returns the winner based on the given voting scheme."""
        return VoteCounter.show_results(scheme, self.preference_matrix)[0][0]

    def calculate_happiness(self, vote, winner):
        """Calculate the voter's happiness based on their preference and the winner."""
        if vote[0] == winner:
            return 1  # Best choice wins
        elif vote[-1] == winner:
            return 0  # Worst choice wins
        else:
            # Gradually decrease happiness for lower preferences
            return 1 - (vote.index(winner) / (len(vote) - 1))
        
    def calculate_overall_happiness(self, matrix, winner):
        """Calculate the overall happiness of the voters."""
        overall_happiness = 0
        for vote in matrix:
            overall_happiness += self.calculate_happiness(vote, winner)
        return overall_happiness / self.n
    
    def get_matrix(self):
        return self.preference_matrix