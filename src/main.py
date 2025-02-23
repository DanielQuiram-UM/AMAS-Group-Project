from btva import BTVA
from output import OutputPrinter
from voting_setup import VotingSetup

def main():
    n = 4  # Number of voters
    m = 4  # Number of candidates

    # Voting scheme ("voting_for_two", "borda", "plurality", "anti_plurality")
    scheme = "plurality"

    preference_matrix = VotingSetup.generate_preference_matrix(n, m)

    TVA = BTVA(n, m, scheme, preference_matrix)

    print("Initial Voting (Preference Matrix):")
    for i, vote in enumerate(preference_matrix.matrix):
        print(f"Voter {i + 1}: {' < '.join(vote)}")

    result = TVA.generate_output()

    OutputPrinter.print_output(result)

if __name__ == "__main__":
    main()
