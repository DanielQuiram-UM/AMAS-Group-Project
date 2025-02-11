from btva import BTVA
from src.vote_counter import VoteCounter
from election_report import ElectionReport

def main():
    n = 2
    m = 2

    TVA = BTVA(n, m)
    TVA.setup()

    TVA.display_results("borda")

if __name__ == "__main__":
    main()