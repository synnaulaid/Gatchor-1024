from hash import gatchor1024
def string_hash():
    input_str = input("Enter a string to hash: ")
    hash_result = gatchor1024(input_str)
    print(f"Gatchor-1024 hash: {hash_result}")

def hash_strings():
    hash_to_verify = input("Enter a hash to verify: ")
    original_string = input("Enter the original string: ")
    # Verify the hash
    if gatchor1024(original_string) == hash_to_verify:
        print("Valid hash!")
    else:
        print("Invalid hash!")


if __name__ == "__main__":
    string_hash()
    print("\nRunning predefined test cases:")
    hash_strings()
