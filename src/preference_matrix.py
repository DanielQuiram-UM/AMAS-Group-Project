class PreferenceMatrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.n = len(matrix)
        self.m = len(matrix[0])

        # Placeholder values
        self.voter_happiness = [0] * self.n
        self.strategic_options = [[] for _ in range(self.n)]
        self.risk_of_strategic_voting = [0] * self.n

    def __str__(self):
        result = "\nVoter Preferences:\n"
        for i, vote in enumerate(self.matrix):
            result += f"Voter {i + 1}: {' > '.join(vote)}\n"

        return result