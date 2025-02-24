from btva import BTVA
from output import OutputPrinter
from voting_setup import VotingSetup
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm  # Import tqdm for the progress bar

def run_btvavote(i, n, m, scheme):
    preference_matrix = VotingSetup.generate_random_matrix(n, m)
    TVA = BTVA(n, m, scheme, preference_matrix)
    result = TVA.generate_output()
    return result


def main():
    n = 5  # Number of voters
    m = 3  # Number of candidates
    scheme = "voting_for_two"

    # Number of iterations
    num_iterations = 10000

    # Use a ProcessPoolExecutor to parallelize the computations
    results = []
    with ProcessPoolExecutor() as executor:
        futures = []

        # Submit tasks to the pool of workers
        for i in range(num_iterations):
            futures.append(executor.submit(run_btvavote, i, n, m, scheme))

        # Wrap the futures in a tqdm progress bar
        for future in tqdm(as_completed(futures), total=num_iterations, desc="Processing", unit="iteration"):
            result = future.result()
            results.append(result)

    # Once all results are gathered, calculate and print the averages
    if num_iterations == 1:
        OutputPrinter.print_output(result)
    else:
        OutputPrinter.print_average_results(scheme, n, m, results)


if __name__ == "__main__":
    main()
