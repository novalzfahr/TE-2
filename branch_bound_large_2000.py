import time, tracemalloc

def bypass_branch(subset, i):
    # Bypass a branch
    for j in range(i - 1, -1, -1):
        if subset[j] == 0:
            subset[j] = 1
            return subset, j + 1
    return subset, 0

def next_vertex(subset, i, m):
    if i < m:
        subset[i] = 0
        return subset, i + 1
    else:
        for j in range(m - 1, -1, -1):
            if subset[j] == 0:
                subset[j] = 1
                return subset, j + 1
    return subset, 0

def BB(universe, sets, costs):
    subset = [1 for x in range(len(sets))]
    subset[0] = 0
    bestCost = sum(costs)
    i = 1
    bestSubset = None  # Inisialisasi bestSubset
    
    while i > 0:
        if i < len(sets):
            cost, tSet = 0, set()  # Temporary set
            for k in range(i):
                cost += subset[k] * costs[k]
                if subset[k] == 1:
                    tSet.update(set(sets[k]))
                    
            if cost > bestCost:
                subset, i = bypass_branch(subset, i)
                continue
                    
            for k in range(i, len(sets)):
                tSet.update(set(sets[k]))
                    
            if tSet != universe:
                subset, i = bypass_branch(subset, i)
            else:
                subset, i = next_vertex(subset, i, len(sets))
        else:
            cost, fSet = 0, set()  # Final set
            for k in range(i):
                cost += subset[k] * costs[k]
                if subset[k] == 1:
                    fSet.update(set(sets[k]))
                    
            if cost < bestCost and fSet == universe:
                bestCost = cost
                bestSubset = subset[:]  # Update bestSubset
            subset, i = next_vertex(subset, i, len(sets))
                
    return bestCost, bestSubset

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

# Implementasi fungsi main untuk pengujian
def main():
    try:
        tracemalloc.start()

        # Read dataset
        universe, subsets, costs = read_dataset('dataset_2000.txt')
        z = time.time()

        output = ""

        # Measure memory usage before set_cover function
        snapshot1 = tracemalloc.take_snapshot()

        if universe and subsets and costs:
            X = BB(universe, subsets, costs)
            if X is not None:
                cost = X[0]
                sets = X[1]
                cover = []
                for x in range(len(subsets)):
                    if sets and sets[x] == 1:
                        cover.append(subsets[x])
                # output += 'Covering sets: ' + str(cover[0]) + '\n'
                output +=  'Cost: ' + str(cost) + ' $' + '\n'

        # Measure memory usage after set_cover function
        snapshot2 = tracemalloc.take_snapshot()

        top_stats = snapshot2.compare_to(snapshot1, 'lineno')

        # Calculate total allocated size
        total_allocated_size = sum(stat.size for stat in top_stats)

        output += f"Execution Time: {(time.time() - z) * 1000} ms\n"
        output += f"Total allocated size: {total_allocated_size / (1024):.1f} KiB\n"

        save_to_file(output, 'output_branch_bound_large.txt')
    finally:
        tracemalloc.stop()

if __name__ == '__main__':
    main()
