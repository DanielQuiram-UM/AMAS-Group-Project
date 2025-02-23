from collections import Counter
import random
from preference_matrix import PreferenceMatrix
from vote_counter import VoteCounter


class BTVA:
    def __init__(self, n, m, scheme, preference_matrix):
        self.n = n  # Number of voters
        self.m = m  # Number of candidates
        self.scheme = scheme  # Voting scheme
        self.preference_matrix = preference_matrix
        self.result_tuple = [[] for _ in range(self.n)]

    def get_winner(self, scheme, preference_matrix=None):
        """Returns the winner based on the given voting scheme."""
        # If preference_matrix is not provided, use the default one (self.preference_matrix)
        if preference_matrix is None:
            preference_matrix = self.preference_matrix
        return VoteCounter.show_results(scheme, preference_matrix)[0][0]

    def calculate_happiness(self, vote, winner):
        """Calculate the voter's happiness based on their preference and the winner."""
        if vote[0] == winner:
            return 1  # Best choice wins
        elif vote[-1] == winner:
            return 0  # Worst choice wins
        else:
            return 1 - (vote.index(winner) / (len(vote) - 1))

    def calculate_overall_happiness(self, strategic_vote, scheme, voter_index):
        """Calculates the overall happiness after applying a strategic vote."""
        modified_matrix = [list(v) for v in self.preference_matrix.matrix]  # Copy original votes
        modified_matrix[voter_index] = list(strategic_vote)  # Remove the old vote and apply the new strategic vote
        modified_preference_matrix = PreferenceMatrix(modified_matrix)
        new_winner = self.get_winner(scheme, modified_preference_matrix)

        total_happiness = sum(self.calculate_happiness(vote, new_winner) for vote in modified_matrix)
        return total_happiness / self.n

    def get_strategic_votes(self, scheme, voter_index):
        """Returns a set of valid strategic voting options for the given voter index."""
        matrix = self.preference_matrix.matrix
        original_winner = self.get_winner(scheme)
        original_vote = matrix[voter_index]
        preferred_candidates = [c for c in original_vote if
                                c != original_winner and original_vote.index(c) < original_vote.index(original_winner)]

        if not preferred_candidates:
            return set()

        temp_matrix = matrix[:voter_index] + matrix[voter_index + 1:]
        initial_points = VoteCounter.get_points(temp_matrix, scheme)

        strategic_vote = []
        remaining_candidates = set(original_vote)
        current_points = initial_points.copy()
        valid_votes = set()

        def backtrack(depth=0):
            nonlocal current_points, strategic_vote, remaining_candidates
            highest_score = max(current_points.values())
            potential_winners = [c for c, p in current_points.items() if p == highest_score]

            max_remaining_points = self.m - depth - 1
            preferred_candidate_can_win = any(
                (current_points[p] + (max_remaining_points if p not in strategic_vote else 0)) > highest_score or
                ((current_points[p] + (max_remaining_points if p not in strategic_vote else 0)) == highest_score
                 and p <= min(potential_winners))
                for p in preferred_candidates
            )

            if not preferred_candidate_can_win:
                return

            if depth == len(original_vote):
                highest_score = max(current_points.values())
                potential_winners = [c for c, p in current_points.items() if p == highest_score]
                final_winner = min(potential_winners)

                if final_winner in preferred_candidates:
                    valid_votes.add(tuple(strategic_vote))
                return

            for candidate in list(remaining_candidates):
                strategic_vote.append(candidate)
                remaining_candidates.remove(candidate)

                # Get points for the current voting scheme
                point_value = VoteCounter.get_points_for_scheme(scheme, depth, self.m)
                current_points[candidate] += point_value

                backtrack(depth + 1)

                strategic_vote.pop()
                remaining_candidates.add(candidate)
                current_points[candidate] -= point_value

        backtrack()

        return valid_votes

    def display_results(self, scheme):
        """Displays the voting results and strategic voting information."""
        print(self.preference_matrix)
        original_winner = self.get_winner(scheme)
        print(f"\nWinner using {scheme}: {original_winner}")

        strategic_votes = [self.get_strategic_votes(scheme, i) for i in range(self.n)]
        print("\n=== Valid Strategic Votes ===")
        for i, votes in enumerate(strategic_votes):
            if votes:
                print(f"Voter {i + 1}:")
                for vote in votes:
                    happiness = self.calculate_overall_happiness(vote, scheme, i)  # Pass voter_index (i)
                    print(f"  - {' > '.join(vote)} (Overall Happiness: {happiness:.2f})")

        return strategic_votes

    def display_risk(self, tuple):
        """Displays the risk of strategic voting."""
        print("\n==== Strategic Voting Risk ====")
        risk = sum(1 for i in range(self.n) if len(tuple[i]) > 0) / self.n
        print(f"Risk of Strategic Voting: {risk:.2f}")
        return risk

    def get_matrix(self):
        return self.preference_matrix
