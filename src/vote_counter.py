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
        return sorted(frequency.items(), key=lambda x: x[1], reverse=True)

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

        return sorted(borda_scores.items(), key=lambda x: x[1], reverse=True)
