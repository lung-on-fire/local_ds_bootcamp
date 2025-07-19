def main ():
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
        dictionary = {}
        for tuple_country, tuple_number in list_of_tuples:
                if tuple_number in dictionary:
                        dictionary[tuple_number].append(tuple_country)
                else:
                        dictionary[tuple_number] = [tuple_country]
      
        for number, countries in dictionary.items():
                for country in countries:
                        print (number, ':', country)

        #print(type(dictionary))


if __name__ == '__main__':({'tuple_number': 'tuple_country'})
main()
        
      
