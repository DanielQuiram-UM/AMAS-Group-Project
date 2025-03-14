from collections import Counter
import itertools
import random

from preference_matrix import PreferenceMatrix
from vote_counter import VoteCounter
from voting_setup import VotingSetup

class ATVA_IK:
    def __init__(self, n, m, max_knowledge_percentage=0.5, mc_sample_size=1000):
        self.n = n  # Number of voters
        self.m = m  # Number of candidates
        self.max_knowledge_percentage = max_knowledge_percentage  # Max percentage of knowledge of strategic voter
        self.mc_sample_size = mc_sample_size
        self.preference_matrix = None

    def setup(self):
        self.preference_matrix = VotingSetup.generate_random_matrix(self.n, self.m)

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

    def calculate_winner_probabilities(self, current_points, excluded_voters, scheme):
        matrix = self.preference_matrix.matrix
        candidate_wins = Counter()
        total_cases = 0

        excluded_ballots = [matrix[i] for i in excluded_voters]

        for _ in range(self.mc_sample_size):
            vote_combination = [random.sample(ballot, len(ballot)) for ballot in excluded_ballots]
            simulated_points = current_points.copy()

            for voter_ranking in vote_combination:
                for depth, candidate in enumerate(voter_ranking):
                    point_value = VoteCounter.get_points_for_scheme(scheme, depth, self.m)
                    simulated_points[candidate] += point_value

            winner = sorted(simulated_points.items(), key=lambda x: (-x[1], x[0]))[0][0]
            candidate_wins[winner] += 1
            total_cases += 1

        return {candidate: count / total_cases for candidate, count in candidate_wins.items()} if total_cases > 0 else {}

    def get_strategic_votes(self, scheme, voter_index):
        matrix = self.preference_matrix.matrix
        excluded_voters = set()
        max_known_voters = int(self.n * self.max_knowledge_percentage)

        available_voters = [i for i in range(self.n) if i != voter_index]
        excluded_voters.update(available_voters[max_known_voters:])
        excluded_voters.discard(voter_index)

        temp_matrix = [matrix[i] for i in range(self.n) if i not in excluded_voters and i != voter_index]
        original_vote = matrix[voter_index]
        original_matrix = temp_matrix + [original_vote]
        original_points = VoteCounter.get_points(original_matrix, scheme)
        original_winner_probs = self.calculate_winner_probabilities(original_points, excluded_voters, scheme)

        expected_original_happiness = sum(
            self.calculate_happiness(original_vote, winner) * probability
            for winner, probability in original_winner_probs.items()
        )

        last_original_pref = original_vote[-1]
        valid_votes = set()

        for perm in itertools.permutations(original_vote):
            permuted_matrix = temp_matrix + [list(perm)]
            current_points = VoteCounter.get_points(permuted_matrix, scheme)
            winner_probabilities = self.calculate_winner_probabilities(current_points, excluded_voters, scheme)

            improves_other_than_last = any(
                winner != last_original_pref and winner_probabilities.get(winner, 0) > original_winner_probs.get(winner, 0) + 0.05
                for winner in winner_probabilities
            )

            if improves_other_than_last and tuple(perm) != tuple(original_vote):
                valid_votes.add(tuple(perm))

        final_valid_votes = []
        for vote in valid_votes:
            winner_probabilities = self.calculate_winner_probabilities(
                VoteCounter.get_points([list(vote)] + temp_matrix, scheme), excluded_voters, scheme
            )
            should_include = any(
                winner_probabilities.get(candidate, 0) > original_winner_probs.get(candidate, 0)
                for candidate in original_vote
            )

            expected_strategic_happiness = expected_original_happiness

            if should_include:
                expected_strategic_happiness = sum(
                    self.calculate_happiness(original_vote, winner) * probability
                    for winner, probability in winner_probabilities.items()
                )
                if expected_strategic_happiness > expected_original_happiness + 0.02:
                    final_valid_votes.append((vote, expected_strategic_happiness))

        return final_valid_votes, expected_original_happiness

    def display_results(self, scheme):
        print(self.preference_matrix)
        original_winner = self.get_winner(scheme)
        print(f"\nWinner using {scheme}: {original_winner}")

        strategic_votes_data = [self.get_strategic_votes(scheme, i) for i in range(self.n)]
        print("\n=== Strategic Votes ===")

        strategic_voters_set = set()
        tactical_happiness_before = []
        strategic_happiness_after = []

        for i, (votes, original_happiness) in enumerate(strategic_votes_data):
            print(f"Processing Voter {i + 1}:")
            original_vote = self.preference_matrix.matrix[i]
            tactical_happiness_before.append(original_happiness)
            print(f"  Tactical Voter's Happiness Before: {original_happiness:.2f}")

            if votes:
                print(f"  Valid Strategic Votes:")
                for vote, strategic_happiness_value in votes:
                    print(f"    - {' > '.join(vote)}")
                    print(f"      Strategic Voter's Happiness After: {strategic_happiness_value:.2f}")
                strategic_voters_set.add(i)
                for vote, strategic_happiness_value in votes:
                    strategic_happiness_after.append(strategic_happiness_value)
            else:
                print(f"  No valid strategic votes for Voter {i + 1}")
                strategic_happiness_after.append(original_happiness)

        avg_tactical_happiness_before = sum(tactical_happiness_before) / len(tactical_happiness_before) if tactical_happiness_before else 0
        avg_strategic_happiness_after = sum(strategic_happiness_after) / len(strategic_happiness_after) if strategic_happiness_after else 0

        print(f"\n=== Averages ===")
        print(f"Average Tactical Voter's Happiness Before: {avg_tactical_happiness_before:.2f}")
        print(f"Average Strategic Voter's Happiness After: {avg_strategic_happiness_after:.2f}")

        risk = len(strategic_voters_set) / self.n if self.n > 0 else 0
        print(f"\nRisk: {risk}")

        return strategic_votes_data, risk, avg_tactical_happiness_before, avg_strategic_happiness_after
