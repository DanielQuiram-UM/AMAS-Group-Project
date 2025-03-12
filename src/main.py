from btva import BTVA
from atva_multiple_voting import ATVA_MV

def main():
    n = 7
    m = 7
    
    #btva= BTVA(n, m)
    #btva.setup()

    #tuple = btva.display_results("anti_plurality")
    #risk = btva.display_risk(tuple)
    
    
    ##############################
    # ATVA - multiple voting
    ##############################
    
    ATVA_4 = ATVA_MV(n, m)
    ATVA_4.setup()
    
    ATVA_4.display_results("plurality")

    

if __name__ == "__main__":
    main()