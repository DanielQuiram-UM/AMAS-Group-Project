from src.ATVA.atva3 import ATVA3
from src.voting_setup import VotingSetup


def main():
    n = 3  # Number of voters
    m = 5  # Number of candidates
    scheme = "borda"  # Voting scheme

    # Generate a single random preference matrix
    preference_matrix = VotingSetup.generate_random_matrix(n, m)

    # Create an instance of ATVA3 with the generated matrix
    ATVA = ATVA3(n, m, scheme, preference_matrix)

    # Call the display_results method to show the strategic voting results
    strategic_votes = ATVA.display_results(scheme)

if __name__ == "__main__":
    main()
