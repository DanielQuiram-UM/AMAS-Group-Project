from btva import BTVA
from vote_counter import VoteCounter
from election_report import ElectionReport
from voting_setup import VotingSetup  # Import the VotingSetup class

def main():
    n = 3  # Number of voters
    m = 4  # Number of candidates
    scheme = "voting_for_two"  # Voting scheme (e.g., "voting_for_two", "borda", etc.)

    preference_matrix = VotingSetup.generate_preference_matrix(n, m)

    TVA = BTVA(n, m, scheme, preference_matrix)

    tuple = TVA.display_results(scheme)
    risk = TVA.display_risk(tuple)

if __name__ == "__main__":
    main()
