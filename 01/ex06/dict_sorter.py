list_of_tuples = [
  ('Russia', '25'),
  ('France', '132'),
  ('Germany', '132'),
  ('Spain', '178'),
  ('Italy', '162'),
  ('Portugal', '17'),
  ('Finland', '3'),
  ('Hungary', '2'),
  ('The Netherlands', '28'),
  ('The USA', '610'),
  ('The United Kingdom', '95'),
  ('China', '83'),
  ('Iran', '76'),
  ('Turkey', '65'),
  ('Belgium', '34'),
  ('Canada', '28'),
  ('Switzerland', '26'),
  ('Brazil', '25'),
  ('Austria', '14'),
  ('Israel', '12')
  ]


def create_dictionary(list_of_tuples):
    dictionary = {country: int(number) for country, number in list_of_tuples}
    return dictionary

def sort_and_display(dictionary):
    sorted_countries = sorted(dictionary, key=lambda country: (-dictionary[country], country))
    for country in sorted_countries:
        print(country)

def main():
    dictionary = create_dictionary(list_of_tuples)
    sort_and_display(dictionary)

if __name__ == "__main__":
    main()