import numpy as np
from queue import PriorityQueue, Queue
import csv
import matplotlib.pyplot as plt
import random

def calculate_center_of_mass(table, index):
    y, x = np.where(table == index)
    if len(x) == 0 or len(y) == 0:
        return None
    return int(np.mean(y)), int(np.mean(x))

def run_iteration(table, sources, queues, weights, areas):
    n = len(table)
    pq = PriorityQueue()
    for index in range(len(queues)):
        pq.put((areas[index], index))
    
    while not pq.empty():
        _, index = pq.get()
        q = queues[index]
        
        if not q.empty():
            x, y = q.get()
            
            if 0 <= x < n and 0 <= y < n and table[x, y] == -1:
                table[x, y] = index
                areas[index] += 1 / weights[index]
                
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < n:
                        q.put((nx, ny))
            
            pq.put((areas[index], index))

    new_sources = []
    for index, source in enumerate(sources):
        com = calculate_center_of_mass(table, index)
        if com:
            new_sources.append(com)
            queues[index] = Queue()
            queues[index].put(com)
        else:
            new_sources.append(source)
    
    return table, new_sources, queues, areas

def visualize_table(table):
    plt.figure(figsize=(10, 10))
    cmap = plt.get_cmap('tab20')
    norm = plt.Normalize(table.min(), table.max())
    plt.imshow(table, cmap=cmap, norm=norm)
    plt.colorbar(label='Source Index')
    plt.title('Visualization of Source Areas')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    plt.show()

def save_to_csv(table, filename='table.csv'):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(table)
    print(f"Table saved to {filename}")

def main():
    n = 32
    
    sources = []
    queues = []
    weights = []
    areas = [0] * 16

    for i in range(4):
        for j in range(4):
            #x = i * (n // 4) + n // 8
            #y = j * (n // 4) + n // 8
            x = random.randint(0, n-1)
            y = random.randint(0, n-1)
            sources.append((x, y))
            q = Queue()
            q.put((x, y))
            queues.append(q)
            weights.append(1)

    iteration = 1
    table = np.full((n, n), -1)
    table, sources, queues, areas = run_iteration(table, sources, queues, weights, areas)
    while True:
        print(f"\nCurrent iteration: {iteration}")
        print("1: Run next iteration")
        print("2: Save current state to CSV")
        print("3: Show current state plot")
        print("4: Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            table = np.full((n, n), -1)
            table, sources, queues, areas = run_iteration(table, sources, queues, weights, areas)
            iteration += 1
            print(f"Iteration {iteration} completed.")
        elif choice == '2':
            filename = input("Enter filename to save CSV (default: table.csv): ") or 'table.csv'
            save_to_csv(table, filename)
        elif choice == '3':
            visualize_table(table)
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
