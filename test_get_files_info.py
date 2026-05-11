from functions.get_files_info import get_files_info

def test():
    # Test with the current directory
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    print("")

    # Test with a subdirectory
    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)
    print("")

    # Test with an external directory
    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(result)
    print("")

    # Test with relative path in directory
    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(result)
    print("")

    # Test with a non-existent directory
    result = get_files_info("calculator", "non_existent_dir")
    print("Result for 'non_existent_dir' directory:")
    print(result)
    print("")

if __name__ == "__main__":
    test()