import numpy as np

# Create a numpy array
arr = [1, 2, 3, 4, 5]
def get_max(arr):
    if len(arr) == 0:
        return None  # Return None if the list is empty
    max_value = arr[0]
    for num in arr:
        if num > max_value:
            max_value = num
    return max_value
numbers = [1, 2, 3, 10, 5]
print(get_max(numbers))  # Output: array([1, 3, 5])