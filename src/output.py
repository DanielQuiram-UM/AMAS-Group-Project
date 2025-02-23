class OutputPrinter:
    @staticmethod
    def print_output(result):
        print("Non-strategic voting outcome (Winner):", result['non_strategic_winner'])

        print("\nIndividual happiness levels:")
        for i, happiness in enumerate(result['individual_happiness_levels']):
            print(f"Voter {i + 1}: Happiness = {happiness:.2f}")

        print(f"\nOverall happiness: {result['overall_happiness']:.2f}")

        print("\nStrategic voting options:")
        for i, options in enumerate(result['strategic_voting_options']):
            print(f"Voter {i + 1}:")
            if options:
                for option in options:
                    print(f"  - Modified Vote: {' > '.join(option['modified_vote'])}, "
                          f"Modified Winner: {option['modified_winner']}, "
                          f"Modified Happiness: {option['modified_happiness']:.2f}, "
                          f"Original Happiness: {option['original_happiness']:.2f}, "
                          f"Overall Happiness: {option['overall_happiness']:.2f}")
            else:
                print("  No strategic voting options available.")

        print(f"\nRisk of strategic voting: {result['risk_of_strategic_voting']:.2f}")
