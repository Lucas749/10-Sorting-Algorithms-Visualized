# Import packages
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


############################################################################
# Define functions
############################################################################
# Function required to update animation
def update(array):
    # Retrieve new values
    xdata = np.linspace(1, len(array), len(array))
    ydata = array

    # Assign current step to sorting operations variable
    global steps
    steps = steps + 1

    # Clear chart and assign new values
    ax.clear()
    ax.bar(xdata, ydata, color="lightskyblue")
    ax.set_title(chart_title, fontsize=25)
    ax.text(0, 1.1, "Number of steps: {}".format(steps), fontsize=20, transform=ax.transAxes)


# Pigeonhole sort O(N+n)
def pigeonhole_sort(array):
    minimum = min(array)
    size = max(array) - minimum + 1
    holes = [0] * size
    for num in array:
        holes[num - minimum] += 1
    i = 0
    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            array[i] = count + minimum
            i += 1
            yield array
    yield array


# Merge sort O(n log n)
def merge_sort(array, start, end):
    # Merge sort helper function
    def merge(array, start, mid, end):
        left = array[start:mid + 1]
        right = array[mid + 1:end + 1]
        empty_list = []
        while len(left) > 0 and len(right) > 0:
            if left[0] <= right[0]:
                empty_list.append(left[0])
                left = left[1:]
            else:
                empty_list.append(right[0])
                right = right[1:]
        if len(left) > 0:
            empty_list = empty_list + left.tolist()
        if len(right) > 0:
            empty_list = empty_list + right.tolist()
        array[start:end + 1] = empty_list
        yield array

    if end <= start:
        yield array
    else:
        mid = start + (end - start) // 2
        yield from merge_sort(array, start, mid)
        yield from merge_sort(array, mid + 1, end)
        yield from merge(array, start, mid, end)
        yield array


# Heap sort O(n log n)
def heap_sort(array):
    # Heap sort help function sift_down
    def sift_down(array, count, size):
        left_pos = 2 * count + 1
        right_pos = 2 * count + 2
        largest_pos = count
        if left_pos < size and array[left_pos] > array[largest_pos]:
            largest_pos = left_pos
        if right_pos < size and array[right_pos] > array[largest_pos]:
            largest_pos = right_pos
        if largest_pos != count:
            array[largest_pos], array[count] = array[count], array[largest_pos]
            yield from sift_down(array, largest_pos, size)
        yield array

    # Heap sort help function heapify
    def heapify(array):
        parent_pos = len(array) // 2 - 1
        while parent_pos >= 0:
            yield from sift_down(array, parent_pos, len(array))
            parent_pos = parent_pos - 1
            yield array
        yield array

    length = len(array)
    yield from heapify(array)
    end = length - 1
    while end > 0:
        array[0], array[end] = array[end], array[0]
        yield from sift_down(array, 0, end)
        end = end - 1
        yield array
    yield array


# Quick sort O(n**2)
def quick_sort(array, start, end):
    if start < end:
        pivot = array[end]
        current_pos = start
        for i in range(start, end):
            if array[i] < pivot:
                array[i], array[current_pos] = array[current_pos], array[i]
                current_pos = current_pos + 1
        array[current_pos], array[end] = array[end], array[current_pos]
        yield from quick_sort(array, start, current_pos - 1)
        yield from quick_sort(array, current_pos + 1, end)
        yield array
    else:
        yield array


# Insertion sort O(n**2)
def insertion_sort(array):
    for i in range(1, len(array)):
        current_pos = i
        while current_pos > 0 and array[current_pos] < array[current_pos - 1]:
            array[current_pos - 1], array[current_pos] = array[current_pos], array[current_pos - 1]
            current_pos = current_pos - 1
            yield array
    yield array


# Bubble sort O(n**2)
def bubble_sort(array):
    for i in range(0, len(array) - 1):
        for j in range(0, len(array) - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
            yield array
    yield array


# Gnome sort O(n**2)
def gnome_sort(array):
    current_pos = 0
    while current_pos < len(array):
        if (current_pos == 0) or (array[current_pos] >= array[current_pos - 1]):
            current_pos = current_pos + 1
        else:
            array[current_pos], array[current_pos - 1] = array[current_pos - 1], array[current_pos]
            current_pos = current_pos - 1
        yield array
    yield array


# Comb sort O(n**2)
def comb_sort(array, k):
    length = len(array)
    gap = length
    unsorted = True

    while unsorted:
        gap = (gap / k)
        gap_int = 1 if gap < 1 else int(gap)
        if gap_int == 1: unsorted = False
        for i in range(length - gap_int):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                unsorted = True
                yield array
    yield array


# Selection sort O(n**2)
def selection_sort(array):
    for i in range(0, len(array)):
        current_pos = i
        for j in range(i + 1, len(array)):
            if array[j] < array[current_pos]:
                current_pos = j
        if current_pos != i:
            array[i], array[current_pos] = array[current_pos], array[i]
        yield array
    yield array


# Bogo sort O(n*n!)
def bogo_sort(array):
    while all((array[:len(array) - 1] - array[1:]) < 0) == False:
        np.random.shuffle(array)
        yield array
    yield array


############################################################################
# Run animation
############################################################################
# Assing parameters
array_length = int(input("Enter array length: "))
algo = input("Enter algorithm [pigeonhole, merge, heap, quick, insertion, bubble, gnome, comb, selection, bogo]: ")

# Generate array
array = np.random.randint(1, array_length, array_length)

# Create dictionary for the sorting algorithms
algo_dic = {"pigeonhole": ["Pigeonhole Sort", pigeonhole_sort(array.copy())],
            "merge": ["Merge Sort", merge_sort(array.copy(), 0, len(array))],
            "heap": ["Heap Sort", heap_sort(array.copy())],
            "quick": ["Quick Sort", quick_sort(array.copy(), 0, len(array) - 1)],
            "insertion": ["Insertion Sort", insertion_sort(array.copy())],
            "bubble": ["Bubble Sort", bubble_sort(array.copy())],
            "gnome": ["Gnome Sort", gnome_sort(array.copy())],
            "comb": ["Comb Sort", comb_sort(array.copy(), 1.3)],
            "selection": ["Selection Sort", selection_sort(array.copy())],
            "bogo": ["Bogo Sort", bogo_sort(array.copy())]
            }

# Initialize chart paramater and array
steps = 1
chart_title = algo_dic[algo][0]
sorting_algo = algo_dic[algo][1]
fig, ax = plt.subplots(figsize=(15, 8))
xdata, ydata = np.linspace(1, len(array), len(array)), array
ax.bar(xdata, ydata, color="lightskyblue")
ax.set_title(chart_title, fontsize=25)

# Run animation
ani = FuncAnimation(fig, update, frames=sorting_algo, repeat=False)
plt.show()
