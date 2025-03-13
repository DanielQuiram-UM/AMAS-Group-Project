from collections import Counter
import itertools
import random

from src.preference_matrix import PreferenceMatrix
from src.vote_counter import VoteCounter


class ATVA3:
    def __init__(self, n, m, scheme, preference_matrix, max_knowledge_percentage=0.5):
        self.n = n  # Number of voters
        self.m = m  # Number of candidates
        self.scheme = scheme  # Voting scheme
        self.preference_matrix = preference_matrix
        self.max_knowledge_percentage = max_knowledge_percentage  # Max percentage of knowledge of strategical voter
        self.result_tuple = [[] for _ in range(self.n)]

    def get_winner(self, scheme, preference_matrix=None):
        if preference_matrix is None:
            preference_matrix = self.preference_matrix
        return VoteCounter.show_results(scheme, preference_matrix)[0][0]

    def calculate_happiness(self, vote, winner):
        if vote[0] == winner:
            return 1
        elif vote[-1] == winner:
            return 0
        else:
            return 1 - (vote.index(winner) / (len(vote) - 1))

    def calculate_overall_happiness(self, strategic_vote, scheme, voter_index):
        modified_matrix = [list(v) for v in self.preference_matrix.matrix]
        modified_matrix[voter_index] = list(strategic_vote)
        modified_preference_matrix = PreferenceMatrix(modified_matrix)
        new_winner = self.get_winner(scheme, modified_preference_matrix)

        total_happiness = sum(self.calculate_happiness(vote, new_winner) for vote in modified_matrix)
        return total_happiness / self.n

    def get_strategic_votes(self, scheme, voter_index):
        matrix = self.preference_matrix.matrix
        excluded_voters = set()

        # Calculate how many voters the strategic voter knows
        max_known_voters = int(self.n * self.max_knowledge_percentage)

        # Exclude the first 'max_known_voters' voters deterministically (no randomization)
        available_voters = [i for i in range(self.n) if i != voter_index]
        excluded_voters.update(available_voters[max_known_voters:])
        excluded_voters.discard(voter_index)

        # Create a temporary matrix excluding the specified voters and the strategic voter's original vote
        temp_matrix = [matrix[i] for i in range(self.n) if i not in excluded_voters and i != voter_index]

        for i in excluded_voters:
            print(f"Removing voter {i + 1} from the preference matrix.")

        # Get initial points and winner probabilities for the strategic voter's original vote
        original_vote = matrix[voter_index]
        original_matrix = temp_matrix + [original_vote]
        original_points = VoteCounter.get_points(original_matrix, scheme)
        original_winner_probs = self.calculate_winner_probabilities(original_points, excluded_voters, scheme)

        print(f"Original winner probabilities: {original_winner_probs}")

        # Identify last-ranked original preference
        last_original_pref = original_vote[-1]

        valid_votes = set()

        # Generate all permutations of the original vote
        for perm in itertools.permutations(original_vote):
            permuted_matrix = temp_matrix + [list(perm)]
            current_points = VoteCounter.get_points(permuted_matrix, scheme)
            winner_probabilities = self.calculate_winner_probabilities(current_points, excluded_voters, scheme)

            # Check if any candidate's probability improves compared to the original winner probabilities,
            # excluding the least preferred candidate.
            improves_other_than_last = any(
                winner != last_original_pref and winner_probabilities.get(winner, 0) > original_winner_probs.get(winner,
                                                                                                                 0)
                for winner in winner_probabilities
            )

            if improves_other_than_last:
                valid_votes.add(tuple(perm))

        final_valid_votes = []

        for vote in valid_votes:
            winner_probabilities = self.calculate_winner_probabilities(
                VoteCounter.get_points([list(vote)] + temp_matrix, scheme), excluded_voters, scheme
            )

            should_include = False  # Flag to determine if we should include the vote

            for candidate in original_vote:  # Iterate from most preferred to least preferred
                original_prob = original_winner_probs.get(candidate, 0)
                new_prob = winner_probabilities.get(candidate, 0)

                if new_prob > original_prob:
                    should_include = True  # Found an improvement at the same preference level
                    break
                elif new_prob < original_prob:
                    should_include = False  # A more preferred candidate is hurt → invalid strategy
                    break

            if should_include:
                final_valid_votes.append((vote, winner_probabilities))

        return final_valid_votes

        return final_valid_votes

    def calculate_winner_probabilities(self, current_points, excluded_voters, scheme):
        matrix = self.preference_matrix.matrix
        candidate_wins = Counter()
        total_cases = 0

        # Extract all unique candidates from the preference matrix
        all_candidates = list({candidate for vote in matrix for candidate in vote})

        # Get the original preference orders of excluded voters
        excluded_ballots = [matrix[i] for i in excluded_voters]

        # Generate all possible full rankings of all excluded voters together
        for vote_combination in itertools.product(*[itertools.permutations(ballot) for ballot in excluded_ballots]):
            # vote_combination now contains a full ranking per excluded voter

            simulated_points = current_points.copy()

            # Assign points according to the voting scheme for each voter
            for voter_ranking in vote_combination:
                for depth, candidate in enumerate(voter_ranking):
                    point_value = VoteCounter.get_points_for_scheme(scheme, depth, self.m)
                    simulated_points[candidate] += point_value

            # Determine the winner based on the highest score
            winner = sorted(simulated_points.items(), key=lambda x: (-x[1], x[0]))[0][0]
            candidate_wins[winner] += 1
            total_cases += 1

        # Normalize probabilities
        return {candidate: count / total_cases for candidate, count in
                candidate_wins.items()} if total_cases > 0 else {}

    def display_results(self, scheme):
        print(self.preference_matrix)
        original_winner = self.get_winner(scheme)
        print(f"\nWinner using {scheme}: {original_winner}")

        strategic_votes = [self.get_strategic_votes(scheme, i) for i in range(self.n)]
        print("\n=== Valid Strategic Votes ===")

        for i, votes in enumerate(strategic_votes):
            if votes:
                print(f"Voter {i + 1}:")
                for vote, winner_probabilities in votes:  # Unpacking the tuple
                    happiness = self.calculate_overall_happiness(vote, scheme, i)
                    probabilities_str = ", ".join(
                        f"{candidate}: {prob:.2f}" for candidate, prob in winner_probabilities.items())
                    print(f"  - {' > '.join(vote)} (Overall Happiness: {happiness:.2f})")
                    print(f"    Winner Probabilities: {probabilities_str}")

        return strategic_votes
