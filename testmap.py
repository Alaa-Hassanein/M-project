def read_file_line_by_line(file_path):
  """
  Reads a file line by line.

  Args:
      file_path: Path to the file.

  Returns:
      A list of lines from the file, or None if the file is not found.
  """
  try:
    with open(file_path, 'r') as file:
      lines = file.readlines()
      return lines
  except FileNotFoundError:
    return None

def convert_to_array(data):
  """
  Converts data with quotes and newlines into a nested array.

  Args:
      data: A list of strings, where each string represents a line from the file.

  Returns:
      A nested list representing the data as a 2D array.
  """
  outer_array = []
  for line in data:  # Loop through lines in the list
    inner_array = []
    for element in line.strip().split(","):
      inner_array.append(element.strip('[""]'))
    outer_array.append(inner_array)
  return outer_array

# Read the file and store the lines
data = read_file_line_by_line("testmap.txt")

# Check if the file was read successfully (optional)
if data is not None:
  # Convert the lines to a 2D array
  array = convert_to_array(data)
  print(array)
else:
  print("Error: Could not read the file 'testmap.txt'.")
