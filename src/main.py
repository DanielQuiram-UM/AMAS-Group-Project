from btva import BTVA
from vote_counter import VoteCounter
from election_report import ElectionReport

def main():
    n = 4
    m = 4

    TVA = BTVA(n, m)
    TVA.setup()

    tuple = TVA.display_results("borda")
    

if __name__ == "__main__":
    main()