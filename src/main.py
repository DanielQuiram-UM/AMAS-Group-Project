from btva import BTVA
from atva_multiple_voting import ATVA_MV
from atva_imperfect_knowledge import ATVA_IK


def main():
    n = 5
    m = 5
    
    btva= BTVA(n, m)
    btva.setup()

    tuple = btva.display_results("anti_plurality")
    risk = btva.display_risk(tuple)

    ##############################
    # ATVA - imperfect knowledge
    ##############################

    #ATVA_3 = ATVA_IK(n, m)
    #ATVA_3.setup()

    #ATVA_3.display_results("anti_plurality")


    ##############################
    # ATVA - multiple voting
    ##############################
    
    #ATVA_4 = ATVA_MV(n, m)
    #ATVA_4.setup()
    
    #ATVA_4.display_results("anti_plurality")





    

if __name__ == "__main__":
    main()