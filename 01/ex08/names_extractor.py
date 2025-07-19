import sys

def extract_names(email_file):
    with open(email_file, 'r') as file:
        emails = file.read().strip().split('\n')

    results = []
    for email in emails:
        name, surname = email.split('@')[0].split('.')
        name = name.capitalize()
        surname = surname.capitalize()
        results.append(f"{name}\t{surname}\t{email}")

    return results

def write_to_tsv(results, output_file='employees.tsv'):
    with open(output_file, 'w') as file:
        file.write("Name\tSurname\tE-mail\n")
        file.write("\n".join(results))

def main():
    if len(sys.argv) != 2:
        raise Exception("Invalid number of arguments")

    email_file = sys.argv[1]
    results = extract_names(email_file)
    write_to_tsv(results)

if __name__ == "__main__":
    main()
    email_file = "file.txt"
