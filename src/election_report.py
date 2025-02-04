from src.vote_counter import VoteCounter

class ElectionReport:
    @staticmethod
    def print_results(preference_matrix):
        print("\n==== Election Report ====")
        print(preference_matrix)

    @staticmethod
    def print_voting_outcomes(preference_matrix):
        print("\n==== Voting Outcomes ====")
        for scheme in ["plurality", "voting_for_two", "anti_plurality", "borda"]:
            results = VoteCounter.show_results(scheme, preference_matrix)
            print(f"{scheme.capitalize()} Results: {results}")