import random
from preference_matrix import PreferenceMatrix

class VotingSetup:
    @staticmethod
    def generate_preference_matrix(n, m):
        alternatives = [chr(65 + i) for i in range(m)]
        votes = []
        for _ in range(n):
            vote = random.sample(alternatives, len(alternatives))
            votes.append(vote)
        return PreferenceMatrix(votes)
