import random

def generate_random_dataset(size):
    universe = set(range(1, size + 1))
    
    subsets = []
    if size == 2000:
        num_subsets = 300
    else:
        num_subsets = size
    
    for _ in range(num_subsets):
        subset_size = random.randint(1, size)
        subset = random.sample(universe, subset_size)
        subsets.append(subset)
    
    costs = [random.randint(1, 100) for _ in range(len(subsets))]
    
    return universe, subsets, costs

def save_to_file(output, filename):
    with open(filename, 'w') as file:
        file.write(output)

def main():
    dataset_sizes = [20, 200, 2000]
    for size in dataset_sizes:
        universe, subsets, costs = generate_random_dataset(size)
        output = ""

        output += "Universe: " + str(universe) + "\n"
        output += "Subsets: " + str(subsets) + "\n"
        output += "Costs: " + str(costs) + "\n"

        filename = f"dataset_{size}.txt"  # Define filename based on dataset size
        save_to_file(output, filename)

if __name__ == "__main__":
    main()
