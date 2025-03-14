from btva import BTVA
from atva_multiple_voting import ATVA_MV
from atva_imperfect_knowledge import ATVA_IK
from atva1 import ATVA1


def main():
    n = 5
    m = 5
    
    ##############################
    # BTVA
    ##############################
    btva= BTVA(n, m)
    btva.setup()

    tuple = btva.display_results("anti_plurality")
    btva.display_risk(tuple)

    print("--------------------------------------------")
    print("ATVA 1 - Collusive Voting")
    print("--------------------------------------------")

    ##############################
    # ATVA_1
    ##############################
    
    ##single run of ATVA1 (collusive voting)    
    TVA = BTVA(n, m)
    TVA.setup()
    pref_mat = TVA.get_matrix()            
    TVA1 = ATVA1(pref_mat)            
    risk, alert = TVA1.get_strategic_options(0, "borda")
    
    ##100 ATVA1 runs of each voting scheme
    #voting schemes ["plurality", "voting_for_two", "anti_plurality", "borda"
    # for scheme in voting_schemes:
    #     cumulative_risk = 0
    #     cumulative_alert = 0
    #     for i in range(100):
    #         TVA = BTVA(n, m)
    #         TVA.setup()
    #         pref_mat = TVA.get_matrix()            
    #         TVA1 = ATVA1(pref_mat)            
    #         #voting schemes ["plurality", "voting_for_two", "anti_plurality", "borda"
    #         risk, alert = TVA1.get_strategic_options(0, scheme)
    #         cumulative_risk += risk
    #         cumulative_alert += int(alert)
    #         print("")
    #         print("")
    #         print(f"{scheme=}, {i=}, ")
    #         print("")
    #         print("")
    #     with open("output.txt", "a") as file:
    #         file.write(f"{scheme=}, {cumulative_risk/100=}, {cumulative_alert/100=} \n") 

    print("--------------------------------------------")
    print("ATVA 3 - Imperfect Knowledge")
    print("--------------------------------------------")

    ##############################
    # ATVA_3 - imperfect knowledge
    ##############################

    ATVA_3 = ATVA_IK(n, m)
    ATVA_3.setup()

    ATVA_3.display_results("anti_plurality")

    print("--------------------------------------------")
    print("ATVA 4 - Multiple Voting")
    print("--------------------------------------------")

    ##############################
    # ATVA_4 - multiple voting
    ##############################
    
    #Single run
    
    ATVA_4 = ATVA_MV(n, m)
    ATVA_4.setup()
    ATVA_4.display_results("voting_for_two")

    #Multiple runs (10 runs)
    
    # overall_happiness = 0
    # new_overall_happiness = 0
    # average_risk = 0
    # for i in range(10):
    #     ATVA_4.setup()
    #     result = ATVA_4.display_results("borda")
    #     risk=0
    #     if not isinstance(result, float):
    #         #risk
    #         for i in range(n):
    #             if len(result[i]) > 0:
    #                 risk += 1
    #         risk = risk / n
    #         print(f"Risk: {risk}")
    #         #happiness
    #         for i in range(n):
    #             if len(result[i]) > 0:
    #                 new_overall_happiness += result[i][0][4]
    #                 overall_happiness += result[i][0][5]
    #                 break;
    #     else:
    #         new_overall_happiness += result
    #         overall_happiness += result
    #     average_risk  += risk  
    # average_risk = average_risk / 10
    # overall_happiness = overall_happiness / 10
    # new_overall_happiness = new_overall_happiness / 10
    # print(f"Average Risk: {average_risk}")
    # print(f"Overall Happiness: {overall_happiness}")
    # print(f"New Overall Happiness: {new_overall_happiness}")

if __name__ == "__main__":
    main()