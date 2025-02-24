from btva import BTVA
from output import OutputPrinter
from voting_setup import VotingSetup
from concurrent.futures import ProcessPoolExecutor, as_completed


def run_btvavote(i, n, m, scheme):
    preference_matrix = VotingSetup.generate_random_matrix(n, m)
    TVA = BTVA(n, m, scheme, preference_matrix)
    result = TVA.generate_output()
    return result


def main():
    n = 10  # Number of voters
    m = 5  # Number of candidates
    scheme = "plurality"

    # Number of iterations
    num_iterations = 1

    # Use a ProcessPoolExecutor to parallelize the computations
    results = []
    with ProcessPoolExecutor() as executor:
        futures = []

        # Submit tasks to the pool of workers
        for i in range(num_iterations):
            futures.append(executor.submit(run_btvavote, i, n, m, scheme))

        # Gather results as they complete
        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    # Once all results are gathered, calculate and print the averages
    OutputPrinter.print_average_results(scheme, n, m, results)


if __name__ == "__main__":
    main()
