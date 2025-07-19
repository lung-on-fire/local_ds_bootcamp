import sys

def find_name(email, tsv_file='employees.tsv'):
    with open(tsv_file, 'r') as file:
        lines = file.read().strip().split('\n')

    for line in lines[1:]:
        name, surname, email_address = line.split('\t')
        if email_address == email:
            return name
    return None

def generate_letter(name):
    return f"Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires."

def main():
    if len(sys.argv) != 2:
        raise Exception("Invalid number of arguments")

    email = sys.argv[1]
    name = find_name(email)

    if name:
        letter = generate_letter(name)
        print(letter)
    else:
        print(f"No name found for email: {email}")

if __name__ == "__main__":
    main()
