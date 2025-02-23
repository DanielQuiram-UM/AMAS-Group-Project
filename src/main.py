from btva import BTVA
from output import OutputPrinter
from voting_setup import VotingSetup

def main():
    n = 3  # Number of voters
    m = 4  # Number of candidates
    scheme = "voting_for_two"  # Voting scheme (e.g., "voting_for_two", "borda", etc.)

    preference_matrix = VotingSetup.generate_preference_matrix(n, m)  # Generate the preference matrix

    TVA = BTVA(n, m, scheme, preference_matrix)  # Initialize the BTVA object with scheme and matrix

    print("Initial Voting (Preference Matrix):")
    for i, vote in enumerate(preference_matrix.matrix):
        print(f"Voter {i + 1}: {' < '.join(vote)}")

    result = TVA.generate_output()  # Generate the output using the generate_output method

    # Print the result using the OutputPrinter static class
    OutputPrinter.print_output(result)

if __name__ == "__main__":
    main()
