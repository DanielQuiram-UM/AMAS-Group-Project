from btva import BTVA
from vote_counter import VoteCounter
from election_report import ElectionReport

def main():
    n = 6
    m = 6

    TVA = BTVA(n, m)
    TVA.setup()

    tuple = TVA.display_results("borda")
    risk = TVA.display_risk(tuple)
    

if __name__ == "__main__":
    main()