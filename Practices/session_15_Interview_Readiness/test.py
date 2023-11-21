# 1 Print the first 3 elements
arr = list('abcedfghijklmnopqrstuvwxyz')
print(
  arr[:3]
)

# 2 Print the last 5 elements
arr = list('abcedfghijklmnopqrstuvwxyz')
print(
  arr[-5:]
)

# 3 Print the repeated elements betwee arr_a and arr_b
arr_a = list('abcedfghijklmnopqrstuvwxyz')
arr_b = list('abc')

# lists does not support set operations
set_a = set(arr_a)
set_b = set(arr_b)

print(
  set_a.intersection(set_b)
)

# 4 Format the number to print 5 digits
num = 123

print(
  f"{num:05d}"
)
# You can also use str(num).zfill(5)

# 5 Find the difference between strings
string_a = "eueiieo"
string_b = "iieoedue"

print([char for char in string_b if char not in string_a])

# 6 Check if the string contains repeated characters
string_a = "eueiieo"
string_b = "abcdefg"

def repeated(string: str):
  seen = set()
  for char in string:
    if char in seen:
      return True
    seen.add(char)
  return False

print(repeated(string_a), repeated(string_b))

# 7 Give the count of repeated elements
set_a = {"a", "b", "c"}
set_b = {"a", "f", "c"}

print(
  len(
    set_a.intersection(set_b)
  )
)
