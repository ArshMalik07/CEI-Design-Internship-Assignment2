#an empty array
array = []

#take input for size of array
size = int(input("Enter the size of array: "))

print("Enter array elements:")
#take input for elements of array
for i in range(size):
    element = int(input())
    array.append(element)

#print the final array
print("The final array is: ", array)