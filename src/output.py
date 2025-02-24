from tabulate import tabulate


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
                          f"New Happiness: {option['modified_happiness']:.2f}, "
                          f"Old Happiness: {option['original_happiness']:.2f}, "
                          f"New Overall Happiness: {option['modified_overall_happiness']:.2f}, "
                          f"True (Old) Overall Happiness: {option['overall_happiness']:.2f}")
            else:
                print("  No strategic voting options available.")

        # Risk of strategic voting
        print(f"\nRisk of strategic voting: {result['risk_of_strategic_voting']:.2f}")

    @staticmethod
    def print_average_results(scheme, n, m, results):
        # Extract metadata
        voting_scheme = scheme
        num_voters = n
        num_candidates = m

        # Compute averages
        avg_happiness = sum(r['overall_happiness'] for r in results) / len(results)
        avg_risk = sum(r['risk_of_strategic_voting'] for r in results) / len(results)
        avg_individual_happiness = [
            sum(r['individual_happiness_levels'][i] for r in results) / len(results)
            for i in range(len(results[0]['individual_happiness_levels']))
        ]

        new_happiness_values, old_happiness_values = [], []
        new_overall_happiness_values, true_old_overall_happiness_values = [], []
        total_strategic_options = 0
        total_voters_with_strategic_voting = 0
        total_candidates_with_strategic_options = 0
        total_voting_options = 0

        for result in results:
            # Track if there are any strategic voting options
            has_strategic_voting = False
            num_voters_with_options = 0
            total_options_for_voters_with_options = 0

            for options in result['strategic_voting_options']:
                if options:
                    has_strategic_voting = True
                    num_voters_with_options += 1
                    total_options_for_voters_with_options += len(options)
                    for option in options:
                        new_happiness_values.append(option['modified_happiness'])
                        old_happiness_values.append(option['original_happiness'])
                        new_overall_happiness_values.append(option['modified_overall_happiness'])
                        true_old_overall_happiness_values.append(option['overall_happiness'])

            if has_strategic_voting:
                total_voters_with_strategic_voting += 1
            total_candidates_with_strategic_options += num_voters_with_options
            total_voting_options += total_options_for_voters_with_options

        # Calculate averages for strategic voting impact
        avg_new_happiness = sum(new_happiness_values) / len(new_happiness_values) if new_happiness_values else 0
        avg_old_happiness = sum(old_happiness_values) / len(old_happiness_values) if old_happiness_values else 0
        avg_new_overall_happiness = sum(new_overall_happiness_values) / len(
            new_overall_happiness_values) if new_overall_happiness_values else 0
        avg_true_old_overall_happiness = sum(true_old_overall_happiness_values) / len(
            true_old_overall_happiness_values) if true_old_overall_happiness_values else 0

        # Calculate percentage of votings dependent on strategic voting
        percentage_strategic_voting = (total_voters_with_strategic_voting / len(results)) * 100 if len(
            results) > 0 else 0

        # Calculate average number of candidates with strategic voting options
        avg_candidates_with_strategic_options = total_candidates_with_strategic_options / len(results) if len(
            results) > 0 else 0

        # Calculate average number of voting options (only for voters with at least one strategic option)
        avg_voting_options = total_voting_options / total_voters_with_strategic_voting if total_voters_with_strategic_voting > 0 else 0

        # Print summary table
        print("\n=== Average Results Over {} Runs ===".format(len(results)))
        summary_table = [
            ["Voting Scheme", voting_scheme],
            ["Number of Voters", num_voters],
            ["Number of Candidates", num_candidates],
            ["Average Overall Happiness", f"{avg_happiness:.2f}"],
            ["Average Risk of Strategic Voting", f"{avg_risk:.2f}"],
            ["Total Strategic Voting Options", total_strategic_options],
            ["Percentage of Votings Dependent on Strategic Voting", f"{percentage_strategic_voting:.2f}%"],
            ["Average Candidates with Strategic Voting Options", f"{avg_candidates_with_strategic_options:.2f}"],
            ["Average Voting Options for Voters with Strategic Voting", f"{avg_voting_options:.2f}"]
        ]
        print(tabulate(summary_table, tablefmt="grid"))

        # Print strategic voting impact table
        strategy_impact_table = [
            ["Average New Happiness", f"{avg_new_happiness:.2f}"],
            ["Average Old Happiness", f"{avg_old_happiness:.2f}"],
            ["Average New Overall Happiness", f"{avg_new_overall_happiness:.2f}"],
            ["Average True Old Overall Happiness", f"{avg_true_old_overall_happiness:.2f}"]
        ]
        print("\nAverage Strategic Voting Impact:")
        print(tabulate(strategy_impact_table, tablefmt="grid"))
