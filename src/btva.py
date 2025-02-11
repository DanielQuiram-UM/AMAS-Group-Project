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

    def check_strategic_voting(self, scheme):
        """Checks if a voter can change the election outcome by voting differently."""
        matrix = self.preference_matrix.matrix
        original_winner = self.get_winner(scheme)

        print("\nChecking for Strategic Voting...\n")

        for i in range(self.n):
            original_vote = matrix[i]
            original_happiness = self.calculate_happiness(original_vote, original_winner)

            # Skip if the voter's top choice is already the winner
            if original_happiness == 1:
                continue

            # Remove voter's vote and check new winner
            temp_matrix = matrix[:i] + matrix[i + 1:]
            temp_preference_matrix = PreferenceMatrix(temp_matrix)
            new_winner_without_voter = VoteCounter.show_results(scheme, temp_preference_matrix)[0][0]

            print(f"\nVoter {i + 1} may influence the election:")
            print(f"  - Current vote: {' > '.join(original_vote)}")
            print(f"  - Original Winner: {original_winner}")
            print(f"  - Original Voter Happiness: {original_happiness:.2f}")

            # Step 1: Generate all permutations of the original vote and check happiness
            best_happiness = original_happiness
            best_permutation = original_vote
            best_new_winner = original_winner

            for permuted_vote in permutations(original_vote):

                # Create a new modified matrix with the permuted vote
                modified_matrix = matrix[:i] + [list(permuted_vote)] + matrix[i + 1:]
                modified_preference_matrix = PreferenceMatrix(modified_matrix)
                modified_winner = VoteCounter.show_results(scheme, modified_preference_matrix)[0][0]

                # Calculate happiness for the current permutation
                new_happiness = self.calculate_happiness(original_vote, modified_winner)

                # Check if this permutation results in higher happiness
                if new_happiness > best_happiness:
                    best_happiness = new_happiness
                    best_permutation = permuted_vote
                    best_new_winner = modified_winner

            # After checking all permutations, we return the best result
            if best_happiness > original_happiness:
                print(f"  - Strategic vote: {' > '.join(best_permutation)} → New Winner: {best_new_winner}")
                print(f"    → Voter's Happiness Increases to: {best_happiness:.2f}")
            else:
                print(f"  - No strategic vote found that increases happiness.")

    def display_results(self, scheme):
        """Displays the voting results and strategic voting information."""
        print(self.preference_matrix)
        original_winner = self.get_winner(scheme)
        print(f"\nWinner using {scheme}: {original_winner}")

        self.check_strategic_voting(scheme)

    def get_matrix(self):
        return self.preference_matrix
