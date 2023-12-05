import tracemalloc, time

def set_cover(universe, subsets, costs):
    cost = 0
    elements = set(e for s in subsets for e in s)
    
    if elements != universe:
        return None
    
    covered = set()
    cover = []
    
    while covered != elements:
        subset = max(subsets, key=lambda s: len(set(s).difference(covered)) / costs[subsets.index(s)])
        cover.append(subset)
        cost += costs[subsets.index(subset)]
        covered |= set(subset)
    
    return cover, cost

def read_dataset(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        universe = eval(lines[0].split("Universe: ")[1])
        subsets = eval(lines[1].split("Subsets: ")[1])
        costs = eval(lines[2].split("Costs: ")[1])
        return universe, subsets, costs

def save_to_file(output, filename):
    with open(filename, 'w') as file:
        file.write(output)

def main():
    try:
        tracemalloc.start()

        # Read dataset
        universe, subsets, costs = read_dataset('dataset_2000.txt')
        z=time.time()


        output = ""

        # Measure memory usage before set_cover function
        snapshot1 = tracemalloc.take_snapshot()

        cover = set_cover(universe, subsets, costs)
        # output += 'Covering sets: ' + str(cover[0]) + '\n'
        output += 'Cost: ' + str(cover[1]) + ' $\n'

        # Measure memory usage after set_cover function
        snapshot2 = tracemalloc.take_snapshot()

        top_stats = snapshot2.compare_to(snapshot1, 'lineno')

        # Calculate total allocated size
        total_allocated_size = sum(stat.size for stat in top_stats)

        output += f"Execution Time: {(time.time() - z) * 1000} ms\n"
        output += f"Total allocated size: {total_allocated_size / (1024):.1f} KiB\n"

        save_to_file(output, 'output_greedy_large.txt')

    finally:
        tracemalloc.stop()

if __name__ == '__main__':
    main()
