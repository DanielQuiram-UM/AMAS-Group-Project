import random
from preference_matrix import PreferenceMatrix

class BTVA:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.preference_matrix = None

    def setup(self):
        alternatives = [chr(65 + i) for i in range(self.m)]  
        votes = [random.sample(alternatives, len(alternatives)) for _ in range(self.n)]
        self.preference_matrix = PreferenceMatrix(votes)

    def get_matrix(self):
        return self.preference_matrix