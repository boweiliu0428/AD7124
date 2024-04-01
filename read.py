# Displaying the contents of the a file
file = open("test_data.csv", "r")
content = file.read()
 
print("\nContent in file2.txt:\n", content)
print(type(content))
file.close()