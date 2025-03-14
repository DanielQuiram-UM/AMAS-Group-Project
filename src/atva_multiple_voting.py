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
        new_permutation = self.get_multiple_voting_permutation(tuple)
            
        if(new_permutation != []):
            tuple = self.check_permutations_happiness(tuple, new_permutation, scheme)
            self.display_risk(tuple)
            return tuple
        else:
            overall_happiness = self.calculate_overall_happiness(self.preference_matrix.matrix, original_winner)
            print(f"Original Overall Happiness: {overall_happiness:.2f}")
            print(f"No multiple strategic voting found.\n")
            return overall_happiness

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
            best_happiness = original_happiness
            best_result = None
            
            for permuted_vote in permutations(original_vote):
                
                # Create a new modified matrix with the permuted vote
                modified_matrix = matrix[:i] + [list(permuted_vote)] + matrix[i + 1:]
                modified_preference_matrix = PreferenceMatrix(modified_matrix)
                modified_winner = VoteCounter.show_results(scheme, modified_preference_matrix)[0][0]

                # Calculate happiness for the current permutation
                new_happiness = self.calculate_happiness(original_vote, modified_winner)

                # Check if this permutation results in higher happiness
                
                if new_happiness > best_happiness:
                    best_happiness = new_happiness
                    best_result = {
                        "happiness": new_happiness,
                        "permutation": permuted_vote,
                        "new_winner": modified_winner
                    }
            
            # After checking all permutations, we return the best results
                
            if best_happiness != original_happiness:    
                # Calculate new overall happiness
                new_overall_happiness = self.calculate_overall_happiness(matrix, best_result['new_winner'])
                
                # Save the best result for the current voter in the result_tuple
                self.result_tuple[i].append([best_result['permutation'], best_result['new_winner'], best_result['happiness'], original_happiness, new_overall_happiness, overall_happiness])
    
        return self.result_tuple

    def get_multiple_voting_permutation(self, tuple_list):
        """Generates all permutations of the given matrix with at least two votes from the tuple_list."""
        def generate_permutation(matrix, index):
            if index == len(matrix):
                return [[]]
            current_permutation = []
            if len(tuple_list[index]) == 1:
                for perm in generate_permutation(matrix, index + 1):
                    current_permutation.append([tuple_list[index][0][0]] + perm)
            else:
                for perm in generate_permutation(matrix, index + 1):
                    current_permutation.append([self.preference_matrix.matrix[index]] + perm)

            return current_permutation
        
        new_vote_permutation = generate_permutation(self.preference_matrix.matrix, 0)[0]
        
        # Filter permutations to include only those with at least two votes from tuple_list
        filtered_permutation = []
        count = sum(1 for i in range(self.n) if new_vote_permutation[i] != self.preference_matrix.matrix[i])
        if count >= 2:
            filtered_permutation = new_vote_permutation
        
        return filtered_permutation
                    
    def check_permutations_happiness(self, tuple, new_permutation, scheme):
        print("\n==== Checking Multiple Tactical Voting Permutation of the best tactical votes ====")
        print(PreferenceMatrix(new_permutation))
        print(f"All multiple strategic voter: \n")
        
        for i in range(self.n):
            old_vote = self.get_matrix().matrix[i]
            new_vote = new_permutation[i]
            #Check if the permutation includes a new vote permutation for the current voter
            if(old_vote != new_vote):
                
                #Check if the happiness increased for the current voter
                original_winner = self.get_winner(scheme)
                original_happiness = tuple[i][0][3]
                original_overall_happiness = tuple[i][0][5]
                new_winner = VoteCounter.show_results(scheme, PreferenceMatrix(new_permutation))[0][0]
                new_happiness = self.calculate_happiness(old_vote, new_winner)
                    
                #Calculate the new overall happiness
                new_overall_happiness = self.calculate_overall_happiness(self.get_matrix().matrix, new_winner)
                
                #Calculate the happiness of the single strategic vote
                new_single_strategic_voting_matrix = self.get_matrix().matrix[:i] + [list(new_permutation[i])] + self.get_matrix().matrix[i + 1:]
                new_single_strategic_voting_winner = VoteCounter.show_results(scheme, PreferenceMatrix(new_single_strategic_voting_matrix))[0][0]
                new_single_strategic_voting_happiness = self.calculate_happiness(old_vote, new_single_strategic_voting_winner)
                
                #Save the new result in the result_tuple
                tuple[i] = [([new_vote, new_winner, new_happiness, original_happiness, new_overall_happiness, original_overall_happiness, new_single_strategic_voting_happiness])]
                
                self.display_multiple_strategic_voting(tuple, i, original_winner, scheme)
                        
        print("====      Permutations Checked      ====")
        return tuple
    
    def display_multiple_strategic_voting(self, tuple, i, original_winner, scheme):
        """Displays the strategic voting information for multiple strategic voting."""
        for result in tuple[i]:
                    if(len(result)>0):                        
                        print(f"  Voter: {i + 1}")
                        print(f"  - Original vote: {' > '.join(map(str, self.preference_matrix.matrix[i]))}")
                        print(f"  → Strategic vote: {' > '.join(map(str, result[0]))}")
                        print(f"  - Original Winner: {original_winner}")        
                        print(f"  → New Winner: {result[1]}")
                        print(f"  - Voter's Original Happiness: {result[3]:.2f}")
                        print(f"  → Voter's Happiness Changed to: {result[2]:.2f}")
                        print(f"  → Voter's actual Happiness for single strategic voting : {result[6]:.2f}")
                        print(f"  - Original Overall Happiness: {result[5]:.2f}")
                        print(f"  → Overall Happiness changed to: {result[4]:.2f}\n")
    
    def display_risk(self, tuple):
        """Displays the risk of strategic voting."""
        print("\n==== Strategic Voting Risk ====")
        
        risk = 0
        for i in range(self.n):
            if len(tuple[i]) > 0:
                risk += 1
                
        risk = risk / self.n
        print(f"Risk of Strategic Voting: {risk:.2f}\n")
