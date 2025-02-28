from collections import Counter
from itertools import permutations
import random
from preference_matrix import PreferenceMatrix
from vote_counter import VoteCounter
from tva import TVA

class ATVA_MV(TVA):

    def __init__(self, n, m):
        super().__init__(n, m)

    def display_results(self, scheme):
        """Displays the voting results and strategic voting information."""
        print(self.preference_matrix)
        original_winner = self.get_winner(scheme)
        print(f"\nWinner using {scheme}: {original_winner}")

        tuple = self.check_strategic_voting(scheme)
        all_permutations = self.get_multiple_voting_permutations(tuple)
        tuple = self.check_permutations_happiness(tuple, all_permutations, scheme)
        
        if(len(all_permutations) > 0):
            print(f"All Voter Preferences with only multiple strategic voting:")
        else:
            print(f"No multiple strategic voting found.\n")
        
        for i in range(self.n):
            
            for result in tuple[i]:
                if(len(result)==7):
                    print(PreferenceMatrix(result[6]))
                    changed_votes = []
                    for j in range(self.n):
                        if result[6][j] != self.preference_matrix.matrix[j]:
                            changed_votes.append(j+1)
                    print(f"  - Changed Votes: {changed_votes}")
                    
                    print(f"  - Voter: {i + 1}")
                    print(f"  - Original vote: {' > '.join(map(str, self.preference_matrix.matrix[i]))}")
                    print(f"  → Strategic vote: {' > '.join(map(str, result[0]))}")
                    print(f"  - Original Winner: {original_winner}")        
                    print(f"  → New Winner: {result[1]}")
                    print(f"  - Voter's Original Happiness: {result[3]:.2f}")
                    print(f"  → Voter's Happiness Increases to: {result[2]:.2f}")
                    print(f"  - Original Overall Happiness: {result[5]:.2f}")
                    print(f"  → Overall Happiness changed to: {result[4]:.2f}\n")
            
        return tuple

    def check_strategic_voting(self, scheme):
        """Checks if a voter can change the election outcome by voting differently."""
        matrix = self.preference_matrix.matrix
        original_winner = self.get_winner(scheme)

        print("\nChecking for Strategic Voting...\n")

        for i in range(self.n):
            original_vote = matrix[i]
            original_happiness = self.calculate_happiness(original_vote, original_winner)
            
            # Calculate the overall happiness of the voters
            overall_happiness = self.calculate_overall_happiness(matrix, original_winner)

            # Skip if the voter's top choice is already the winner
            if original_happiness == 1:
                continue

            # Step 1: Generate all permutations of the original vote and check happiness
            better_results = []
            
            for permuted_vote in permutations(original_vote):
                
                # Create a new modified matrix with the permuted vote
                modified_matrix = matrix[:i] + [list(permuted_vote)] + matrix[i + 1:]
                modified_preference_matrix = PreferenceMatrix(modified_matrix)
                modified_winner = VoteCounter.show_results(scheme, modified_preference_matrix)[0][0]

                # Calculate happiness for the current permutation
                new_happiness = self.calculate_happiness(original_vote, modified_winner)

                # Check if this permutation results in higher happiness
                
                if new_happiness > original_happiness:
                    better_results.append({
                        "happiness": new_happiness,
                        "permutation": permuted_vote,
                        "new_winner": modified_winner
                    })
            
            # After checking all permutations, we return the best result
                
            if len(better_results) >= 1:
                for result in better_results:
                    
                    # Calculate new overall happiness
                    new_matrix = matrix[:i] + [list(result['permutation'])] + matrix[i + 1:]
                    new_overall_happiness = self.calculate_overall_happiness(new_matrix, result['new_winner'])
                    
                    # Save a better result for the current voter in the result_tuple
                    self.result_tuple[i].append([result['permutation'], result['new_winner'], result['happiness'], original_happiness, new_overall_happiness, overall_happiness])
        
        return self.result_tuple

    def get_multiple_voting_permutations(self, tuple_list):
        """Generates all permutations of the given matrix with at least two votes from the tuple_list."""
        def generate_permutations(matrix, index):
            if index == len(matrix):
                return [[]]
            current_permutations = []
            if len(tuple_list[index]) > 0:
                for result in tuple_list[index]:
                    for perm in generate_permutations(matrix, index + 1):
                        current_permutations.append([result[0]] + perm)
            else:
                for perm in generate_permutations(matrix, index + 1):
                    current_permutations.append([self.preference_matrix.matrix[index]] + perm)

            return current_permutations
        
        all_permutations = generate_permutations(self.preference_matrix.matrix, 0)
        
        # Remove the permutation where all votes are original
        original_permutation = [self.preference_matrix.matrix[i] for i in range(self.n)]
        all_permutations = [perm for perm in all_permutations if perm != original_permutation]
        
        # Filter permutations to include only those with at least two votes from tuple_list
        filtered_permutations = []
        for perm in all_permutations:
            count = sum(1 for i in range(self.n) if perm[i] != self.preference_matrix.matrix[i])
            if count >= 2:
                filtered_permutations.append(perm)
        
        return filtered_permutations
                    
    def check_permutations_happiness(self, tuple, all_permutations, scheme):
        print("\n==== Checking Tactical Permutations ====")
        for permutation in all_permutations:
            print([list(p) for p in permutation])
            for i in range(self.n):
                old_vote = self.preference_matrix.matrix[i]
                new_vote = permutation[i]
                #Check if the permutation includes a new vote permutation for the current voter
                if(old_vote != new_vote):
                    
                    #Check if the happiness increased for the current voter
                    original_winner = self.get_winner(scheme)
                    original_happiness = tuple[i][0][3]
                    original_overall_happiness = tuple[i][0][5]
                    new_winner = VoteCounter.show_results(scheme, PreferenceMatrix(permutation))[0][0]
                    new_happiness = self.calculate_happiness(old_vote, new_winner)
                    if(new_happiness > original_happiness):
                        
                        #Calculate the new overall happiness
                        new_matrix = list(permutation)
                        new_overall_happiness = self.calculate_overall_happiness(new_matrix, original_winner)
                        
                        #Save the new result in the result_tuple
                        tuple[i].append([new_vote, new_winner, new_happiness, original_happiness, new_overall_happiness, original_overall_happiness, new_matrix])
        print("====      Permutations Checked      ====\n")
        return tuple
    
    def display_risk(self, tuple):
        """Displays the risk of strategic voting."""
        print("\n==== Strategic Voting Risk ====")
        
        risk = 0
        for i in range(self.n):
            if len(tuple[i]) > 0:
                risk += 1
                
        risk = risk / self.n
        print(f"Risk of Strategic Voting: {risk:.2f}")
