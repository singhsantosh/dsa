"""
Asymptotic complexity in terms of size of 'arr' 'n':
* Time: O(n ^ 2).
* Auxiliary space: O(1).
* Total space: O(n).
"""


def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        # Assume the smallest element is the current element
        min_index = i
        # Iterate through the unsorted part of the list
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                # Update the min_index if a smaller element is found
                min_index = j
        # Swap the found minimum element with the first element of the unsorted part
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


if __name__ == "__main__":
    arr = [5, 8, 3, 9, 4, 1, 7]
    output_arr = [1, 3, 4, 5, 7, 8, 9]
    input_arr = arr.copy()
    sorted_arr = selection_sort(arr)
    print(f'Input array  - {input_arr}')
    if output_arr == sorted_arr:
        print(f'Output array - {sorted_arr} => Test pass!')
    else:
        print(f'Output - {sorted_arr} => Test failed!')
