from functions.get_file_content import get_file_content

def test():
    # Test with an existing file with content greater than MAX_CHARS
    result = get_file_content("calculator", "lorem.txt")
    print("Result for 'lorem.txt':")
    print(result)
    print("")

    # Test with an existing file
    result = get_file_content("calculator", "main.py")
    print("Result for 'main.py':")
    print(result)
    print("")

    # Test with an existing file in a subdirectory
    result = get_file_content("calculator", "pkg/calculator.py")
    print("Result for 'pkg/calculator.py':")
    print(result)
    print("")

    # Test with a file that outside the working directory
    result = get_file_content("calculator", "/bin/cat")
    print("Result for '/bin/cat':")
    print(result)
    print("")

    # Test with a non-existent file in subdirectory
    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Result for 'pkg/does_not_exist.py':")
    print(result)
    print("")

    # Test with a non-existent file
    result = get_file_content("calculator", "non_existent_file.txt")
    print("Result for 'non_existent_file.txt':")
    print(result)
    print("")

    # Test with a file outside the working directory
    result = get_file_content("calculator", "../main.py")
    print("Result for '../main.py':")
    print(result)
    print("")

if __name__ == "__main__":
    test()