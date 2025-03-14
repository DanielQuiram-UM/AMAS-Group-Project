import numpy as np
from preference_matrix import PreferenceMatrix
from vote_counter import VoteCounter
from itertools import permutations, product, combinations
import time

#VOTER COLLUSION
class ATVA1:
    def __init__(self, matrix):
        self.preference_matrix = matrix

    def get_matrix(self):
        return self.preference_matrix
    
    def get_strategic_options(self, max_colluder_count = 0, voting_scheme = 'plurality'):
        #colluder count [0,n], voting schemes ["plurality", "voting_for_two", "anti_plurality", "borda"
        default_winner = VoteCounter.show_results(voting_scheme, self.preference_matrix)[0][0]          
        candidates = sorted(self.preference_matrix.matrix[0])
        
        #add an all-caps alert line at the end of the output if strategic voting ever increased overall happiness
        alert = False
        
        #stores candidates that can already be elected by a set of voters
        #if a subset of a team of colluders can force a candidate, no need to check the superset
        candidate_voter_sets = {candidate: set() for candidate in candidates}
        
        #compute and store all permutations for all rows
        #store one row for each candidate instead if plurality or anti-plurality to save enormous amounts of time later
        preference_permutations = {
            i: [tuple([char] * len(self.preference_matrix.matrix[i])) for char in self.preference_matrix.matrix[i]]
            if voting_scheme in {"plurality","anti_plurality"} 
            else list(permutations(self.preference_matrix.matrix[i]))
            for i in range(self.preference_matrix.n)
        }
        
        #content voters will not participate in strategic voting
        content_voters = []
        for i in range(self.preference_matrix.n):
            if self.calculate_happiness(self.preference_matrix.matrix[i], default_winner)== 1:
                content_voters.append(i)

        starting_overall_happiness = self.calculate_overall_happiness(self.preference_matrix.matrix, default_winner)
        
        print(f"{voting_scheme=}")
        print(f"{default_winner=}")
        print(f"{starting_overall_happiness=}")
        print("Original Preference Matrix:")
        print(self.preference_matrix)
        display_content_voters = [x + 1 for x in content_voters]
        print(f"Content voters that will not participate in strategic voting: {display_content_voters}")

        #looping over all combinations of voters up to defined maximum.
        #if defined max is larger than number of voters (array length), use number of voters
        #if defined max is 0, use number of voters.
        if max_colluder_count == 0 or max_colluder_count > self.preference_matrix.n:
            max_colluder_count = self.preference_matrix.n        
        
        cumulative_risk_vector = np.zeros(self.preference_matrix.n + 1)
        risk_vector = np.zeros(self.preference_matrix.n)             
            
        for num_colludors in range(1, max_colluder_count + 1):
            print(f"\n### Combinations with groups of {num_colludors}:")
            for voter_idx in combinations(range(self.preference_matrix.n), num_colludors):          
                if any(value in content_voters for value in voter_idx):
                    continue  # at least one voter in this set is perfectly content, skip
                
                #matrix is zero-indexed, voters are indexed from 1, adding 1 to displayed values for readability
                display_voter_idx = [x + 1 for x in voter_idx]
                desired_winners = []
                for candidate in candidates:
                    unhappy_voter = False
                    for voter in voter_idx:
                        if self.calculate_happiness(self.preference_matrix.matrix[voter], candidate) \
                            <= self.calculate_happiness(self.preference_matrix.matrix[voter], default_winner):
                                unhappy_voter = True
                                break
                    if not unhappy_voter:
                        desired_winners.append(candidate)
                if len(desired_winners) == 0:
                    print(f"Voters {display_voter_idx} do not share goals.")
                else:
                    print(f"Voters {display_voter_idx} prefer candidates {desired_winners}.")
                    start = time.time()
                    electable_desired_winners = []
                    
                    for target_candidate in desired_winners:
                        #if a subset of our strategic voters can force a candidate, no need to look for a new solution
                        if any(set(subset).issubset(set(voter_idx)) for subset in candidate_voter_sets[target_candidate]):
                            candidate_voter_sets[target_candidate].add(frozenset(voter_idx))
                            electable_desired_winners.append(target_candidate)
                            print(f"A subset of {display_voter_idx} can elect {target_candidate}.")
                    
                    if len(desired_winners) > len(electable_desired_winners):
                        for combination in product(*[preference_permutations[i] for i in voter_idx]):
                            #copying the original matrix, and replacing rows with permutations
                            temp_list = [row.copy() for row in self.preference_matrix.matrix]                    
                            for idx, row_idx in enumerate(voter_idx):
                                temp_list[row_idx] = list(combination[idx])
        
                                new_preference_matrix = PreferenceMatrix(temp_list)
                                new_winner = VoteCounter.show_results(voting_scheme, new_preference_matrix)[0][0]   
                                
                                if new_winner in desired_winners and not new_winner in electable_desired_winners:  
                                    electable_desired_winners.append(new_winner)
                                    candidate_voter_sets[new_winner].add(frozenset(voter_idx))
                                    
                                    #we found something! print it.
                                    print(new_preference_matrix)
                                    print(f"{default_winner=} {new_winner=}")
                                    
                            if len(desired_winners) == len(electable_desired_winners):
                                #nothing left to find
                                break  
                    end = time.time()                                  
                    if len(electable_desired_winners) > 0:
                        for voter in voter_idx:
                            risk_vector[voter] = 1
                        print(f"Voters {display_voter_idx} can force a win for {electable_desired_winners}, {end-start} seconds.")    
                        voter_cumulative_happiness = 0
                        for voter in voter_idx:
                            voter_cumulative_happiness =  self.calculate_happiness(self.preference_matrix.matrix[voter], default_winner)
                        strategic_voter_starting_average_happiness = voter_cumulative_happiness / len(voter_idx)
                        for candidate in electable_desired_winners:
                            voter_cumulative_happiness = 0
                            for voter in voter_idx:
                                voter_cumulative_happiness =  self.calculate_happiness(self.preference_matrix.matrix[voter], candidate)
                            strategic_voter_new_average_happiness = voter_cumulative_happiness / len(voter_idx)
                            new_average_happiness = self.calculate_overall_happiness(self.preference_matrix.matrix, candidate)
                            print(f"after electing candidate {candidate}: ")
                            print(f"average happiness of voters {display_voter_idx} changed from {strategic_voter_starting_average_happiness:.2f}" 
                                  f" to {strategic_voter_new_average_happiness:.2f}, "
                                  f"net change {strategic_voter_new_average_happiness - strategic_voter_starting_average_happiness:.2f} ")
                            print(f"overall changed from {starting_overall_happiness:.2f} to {new_average_happiness:.2f}"
                                  f", net change {new_average_happiness - starting_overall_happiness:.2f} ")
                            if new_average_happiness > starting_overall_happiness:
                                print("OVERALL HAPPINESS INCREASED!!!")
                                alert = True
                            
                    else:
                        print(f"No strategic options for voters {display_voter_idx}, {end-start} seconds.")     
            print(f"{risk_vector=}")
            print(f"Cumulative risk = {np.mean(risk_vector)}")
            cumulative_risk_vector[num_colludors] = np.mean(risk_vector)
        
        if alert:
            print("STRATEGIC VOTING INCREASED OVERALL HAPPINESS.")
        
        # returning risk vector to calculate risk over a few hundred runs
        return cumulative_risk_vector, alert
        
            

                        
                
        
    def calculate_happiness(self, vote, winner):
        """Calculate the voter's happiness based on their preference and the winner."""
        if vote[0] == winner:
            return 1  # Best choice wins
        elif vote[-1] == winner:
            return 0  # Worst choice wins
        else:
            # Gradually decrease happiness for lower preferences
            return 1 - (vote.index(winner) / (len(vote) - 1))
        
    def calculate_overall_happiness(self, matrix, winner):
        """Calculate the overall happiness of the voters."""
        overall_happiness = 0
        for vote in matrix:
            overall_happiness += self.calculate_happiness(vote, winner)
        return overall_happiness / len(matrix)
        
