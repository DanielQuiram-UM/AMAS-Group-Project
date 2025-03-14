from collections import Counter

class VoteCounter:

    @staticmethod
    def show_results(scheme, preference_matrix):
        matrix = preference_matrix.matrix

        schemes = {
            "plurality": VoteCounter.plurality,
            "voting_for_two": VoteCounter.voting_for_two,
            "anti_plurality": VoteCounter.anti_plurality,
            "borda": VoteCounter.borda
        }

        if scheme not in schemes:
            raise ValueError(f"Unknown voting scheme: {scheme}")

        return schemes[scheme](matrix)

    @staticmethod
    def count_and_sort(votes):
        frequency = Counter(votes)
        return sorted(frequency.items(), key=lambda x: (-x[1], x[0]))

    @staticmethod
    def plurality(matrix):
        first_votes = [preferences[0] for preferences in matrix]
        result_list = VoteCounter.count_and_sort(first_votes)
        return result_list

    @staticmethod
    def voting_for_two(matrix):
        first_two_votes = [preferences[i] for preferences in matrix for i in range(2)]
        result_list = VoteCounter.count_and_sort(first_two_votes)
        return result_list

    @staticmethod
    def anti_plurality(matrix):
        all_but_last_votes = [preferences[i] for preferences in matrix for i in range(len(preferences) - 1)]
        result_list = VoteCounter.count_and_sort(all_but_last_votes)
        return result_list

    @staticmethod
    def borda(matrix):
        num_candidates = len(matrix[0])  
        borda_scores = Counter()

        for row in matrix:
            for position, candidate in enumerate(row):
                borda_scores[candidate] += (num_candidates - 1 - position)

        return sorted(borda_scores.items(), key=lambda x: (-x[1], x[0]))

    @staticmethod
    def get_points(matrix, scheme):
        """Returns a dictionary mapping each candidate to their points in the given voting scheme."""
        schemes = {
            "plurality": lambda: Counter([row[0] for row in matrix]),
            "voting_for_two": lambda: Counter([row[i] for row in matrix for i in range(2)]),
            "anti_plurality": lambda: Counter([row[i] for row in matrix for i in range(len(row) - 1)]),
            "borda": lambda: VoteCounter._borda_points(matrix),
        }

        if scheme not in schemes:
            raise ValueError(f"Unknown voting scheme: {scheme}")

        return schemes[scheme]()

    @staticmethod
    def _borda_points(matrix):
        """Helper function to calculate Borda points."""
        num_candidates = len(matrix[0])
        borda_scores = Counter()

        for row in matrix:
            for position, candidate in enumerate(row):
                borda_scores[candidate] += (num_candidates - 1 - position)

        return borda_scores

    @staticmethod
    def get_points_for_scheme(scheme, depth, m):
        """Returns the points for the given voting scheme."""
        if scheme == "plurality":
            return 1 if depth == 0 else 0  # Only the top candidate gets points.

        elif scheme == "voting_for_two":
            return 1 if depth < 2 else 0  # First two candidates get points.

        elif scheme == "anti_plurality":
            return 1 if depth < m - 1 else 0  # All but the last candidate get points.

        elif scheme == "borda":
            return m - 1 - depth  # Borda: first gets m-1 points, second gets m-2, ..., last gets 0 points.

        else:
            raise ValueError("Unsupported voting scheme")
