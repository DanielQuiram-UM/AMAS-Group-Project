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

        #result += "\nVoter Happiness:\n"
        #for i, happiness in enumerate(self.voter_happiness):
        #    result += f"Voter {i + 1}: {happiness}\n"

        #result += "\nStrategic Voting Options:\n"
        #for i, strategies in enumerate(self.strategic_options):
        #    strategy_text = ', '.join(strategies) if strategies else "None"
        #    result += f"Voter {i + 1}: {strategy_text}\n"

        #result += "\nRisk of Strategic Voting:\n"
        #for i, risk in enumerate(self.risk_of_strategic_voting):
        #    result += f"Voter {i + 1}: {risk}\n"

        return result