from collections import Counter
from itertools import permutations
import random
from preference_matrix import PreferenceMatrix
from vote_counter import VoteCounter

class BTVA:
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

    def check_strategic_voting(self, scheme):
        """Checks if a voter can change the election outcome by voting differently."""
        matrix = self.preference_matrix.matrix
        original_winner = self.get_winner(scheme)

        print("\nChecking for Strategic Voting...\n")

        for i in range(self.n):
            original_vote = matrix[i]
            original_happiness = self.calculate_happiness(original_vote, original_winner)
            
            # Calculate the overall happiness of the voters
            overall_happiness = self.calculate_overall_happiness(matrix, original_winner)

            # Skip if the voter's top choice is already the winner
            if original_happiness == 1:
                continue

            print(f"\nVoter {i + 1} may influence the election:")
            print(f"  - Current vote: {' > '.join(original_vote)}")
            print(f"  - Original Winner: {original_winner}")
            print(f"  - Original Voter Happiness: {original_happiness:.2f}")

            # Step 1: Generate all permutations of the original vote and check happiness
            better_results = []
            
            for permuted_vote in permutations(original_vote):
                
                # Create a new modified matrix with the permuted vote
                modified_matrix = matrix[:i] + [list(permuted_vote)] + matrix[i + 1:]
                modified_preference_matrix = PreferenceMatrix(modified_matrix)
                modified_winner = VoteCounter.show_results(scheme, modified_preference_matrix)[0][0]

                # Calculate happiness for the current permutation
                new_happiness = self.calculate_happiness(original_vote, modified_winner)

                # Check if this permutation results in higher happiness
                
                if new_happiness > original_happiness:
                    better_results.append({
                        "happiness": new_happiness,
                        "permutation": permuted_vote,
                        "new_winner": modified_winner
                    })
            
            # After checking all permutations, we return the best result
                
            if len(better_results) >= 1:
                for result in better_results:
                    
                    # Calculate new overall happiness
                    new_matrix = matrix[:i] + [list(result['permutation'])] + matrix[i + 1:]
                    new_overall_happiness = self.calculate_overall_happiness(new_matrix, result['new_winner'])
                    
                    # Save a better result for the current voter in the result_tuple
                    self.result_tuple[i].append([result['permutation'], result['new_winner'], result['happiness'], original_happiness, new_overall_happiness, overall_happiness])
    
                    print(f"  - Strategic vote: {' > '.join(result['permutation'])} → New Winner: {result['new_winner']}")
                    print(f"    → Voter's Happiness Increases to: {result['happiness']:.2f}")
            else:
                print(f"  - No strategic vote found that increases happiness.")
        
        return self.result_tuple

    def display_results(self, scheme):
        """Displays the voting results and strategic voting information."""
        print(self.preference_matrix)
        original_winner = self.get_winner(scheme)
        print(f"\nWinner using {scheme}: {original_winner}")

        tuple = self.check_strategic_voting(scheme)
        
        return tuple
    
    def display_risk(self, tuple):
        """Displays the risk of strategic voting."""
        print("\n==== Strategic Voting Risk ====")
        
        risk = 0
        for i in range(self.n):
            if len(tuple[i]) > 0:
                risk += 1
                
        risk = risk / self.n
        print(f"Risk of Strategic Voting: {risk:.2f}")
        
        return risk

    def get_matrix(self):
        return self.preference_matrix
