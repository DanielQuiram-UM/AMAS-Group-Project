class OutputPrinter:
    @staticmethod
    def print_output(result):
        # Non-strategic voting outcome (Winner)
        print("Non-strategic voting outcome (Winner):", result['non_strategic_winner'])

        # Individual happiness levels (old happiness before strategic voting)
        print("\nIndividual happiness levels (before strategic voting):")
        for i, happiness in enumerate(result['individual_happiness_levels']):
            print(f"Voter {i + 1}: Happiness = {happiness:.2f}")

        # Overall happiness (old overall happiness before strategic voting)
        print(f"\nOverall happiness (before strategic voting): {result['overall_happiness']:.2f}")

        # Strategic voting options
        print("\nStrategic voting options:")
        for i, options in enumerate(result['strategic_voting_options']):
            print(f"Voter {i + 1}:")
            if options:
                for option in options:
                    # New happiness, old happiness, new overall happiness, old overall happiness
                    print(f"  - Modified Vote: {' > '.join(option['modified_vote'])}, "
                          f"Modified Winner: {option['modified_winner']}, "
                          f"New Happiness (H̃i): {option['modified_happiness']:.2f}, "
                          f"Old Happiness (Hi): {option['original_happiness']:.2f}, "
                          f"New Overall Happiness (H̃): {option['modified_overall_happiness']:.2f}, "
                          f"Old Overall Happiness (H): {option['overall_happiness']:.2f}")
            else:
                print("  No strategic voting options available.")

        # Risk of strategic voting
        print(f"\nRisk of strategic voting: {result['risk_of_strategic_voting']:.2f}")
