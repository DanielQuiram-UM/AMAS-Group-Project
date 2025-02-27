from btva import BTVA
from atva_multiple_voting import ATVA_MV
from vote_counter import VoteCounter
from election_report import ElectionReport

def main():
    n = 4
    m = 3
    
    #TVA.setup()

    #tuple = TVA.display_results("borda")
    #risk = TVA.display_risk(tuple)
    
    
    ##############################
    # ATVA - multiple voting
    ##############################
    
    ATVA_4 = ATVA_MV(n, m)
    ATVA_4.setup()
    
    tuple_list = ATVA_4.display_results("borda")

    

if __name__ == "__main__":
    main()