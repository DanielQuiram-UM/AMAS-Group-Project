from btva import BTVA
from src.vote_counter import VoteCounter
from election_report import ElectionReport

def main():
    n = 5  
    m = 5  

    TVA = BTVA(n, m)
    TVA.setup()
    
    # Print detailed election report
    ElectionReport.print_results(TVA.get_matrix())

    # Print voting method outcomes
    ElectionReport.print_voting_outcomes(TVA.get_matrix())

if __name__ == "__main__":
    main()