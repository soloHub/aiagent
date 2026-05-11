from functions.write_file import write_file

def test():
    # Test case 1: Valid file path and content
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)

    # Test case 2: Attempt to write outside the working directory
    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result) 

    # Test case 3: Attempt to write to a external file
    result =  write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)

    # Test case 4: Attempt to write to a directory
    result = write_file('.', 'testdir', 'This should fail.')
    print(result)  # Expected: Error: Cannot write to "test_dir" as it is a directory       


if __name__ == "__main__":
    test()