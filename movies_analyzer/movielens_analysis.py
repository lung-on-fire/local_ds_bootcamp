import os
import json
import requests
from datetime import datetime
from collections import defaultdict
import pytest

##Vovchik's functions
def find_median(list_of_numbers: list[float]) -> float:
    list_of_numbers = sorted(list_of_numbers)
    n = len(list_of_numbers)
    
    if n % 2 == 0:
        median = (list_of_numbers[n//2 - 1] + list_of_numbers[n//2]) / 2
    else:
        median = list_of_numbers[n//2]
    return round(median, 2)

def find_variance(list_of_numbers: list[float]) -> float:
    length = len(list_of_numbers)
    if length == 0:
        return 0
    mean = sum(list_of_numbers) / length
    if length == 1:
        return mean
    variance = sum((x - mean)**2 for x in list_of_numbers) / (length - 1)
    return round(variance, 2)

def extract_title(line):
    title = ''
    if line.find(',"') != -1:
        title = line.split(',"')[1].split('",')[-2]
    else:
        title = line.split(',')[1]
    if title.find(', The') != -1:
        title = title.replace(', The', '')
        title = 'The ' + title
    return title

def replace_id_with_name(movie_id:dict):
    result = {}
    generator = read_file_generator(Movies().ifilename)
    for line in generator:
        id = line.split(',')[0]
        if id in movie_id.keys():
            name = extract_title(line)
            result[name] = movie_id[id]
        if len(result) == len(movie_id):
            break
    return result

def extract_title_and_genre_count(line, isreturnedid=0):
    id = ''
    title = ''
    genres = line.strip().split(',')[-1]
    if line.find(',"') != -1:
        id = line.split(',"')[0]
        title = line.split(',"')[1].split('",')[-2]
    else:
        id = line.split(',')[0]
        title = line.split(',')[1].split(',')[-1]
    if title.find(', The') != -1:
        title = title.replace(', The', '')
        title = 'The ' + title
    if genres == '(no genres listed)':
                genres_count = 0
    else:
        genres_count = genres.count('|')+1

    if isreturnedid == 1:
        return id, genres_count
    else:
        return title, genres_count

def extract_year(title):
    parts = title.split(')')
    for part in reversed(parts):
        stripped = part.strip()
        if '(' in stripped:
            content = stripped.split('(')[-1].strip()
            if len(content) == 4 and content.isdigit():
                return content
    return 'not specified'

def read_file_generator(file):
        with open(file, 'r') as f:
            next(f)
            for line in f:
                    yield line.strip()

def read_file_generator2(file):
    with open(file, 'r') as f:
        next(f)
        for line in f:
            yield line.strip().split(',')


##Dasha's functions
def dict_topn(elem_list, n):
    elem_counts = {}
    for elem in elem_list:
        if elem in elem_counts:
            elem_counts[elem] += 1
        else:               
            elem_counts[elem] = 1
        
    top_elements = {k: v for k, v in sorted(elem_counts.items(), key=lambda item: item[1], reverse=True)[:n]}
    return top_elements

def runtime_to_minutes(runtime):
    parts = runtime.split()
    minutes = 0
    if "min" in runtime:
        minutes = int(parts[-2]) 
    return minutes

##Vovchik's classes
class Movies:
    """
    Analyzing data from movies.csv
    """
    
    ifilename = ''

    def __init__(self, path_to_the_file='../datasets/ml-latest-small/movies.csv'):
        """
        Put here any fields that you think you will need.
        """ 
        try:
            self.ifilename = path_to_the_file
        except Exception as e:
            print(e)
    

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        try:
            release_years = {}
            generator = read_file_generator(self.ifilename)
            for line in generator:
                name = line.strip().split(',')[-2]
                year = extract_year(name)
                release_years[year] = release_years.get(year,0)+1
            
            release_years = dict(sorted(release_years.items(), key=lambda x: x[1], reverse=True))
            return release_years
        except Exception as e:
            print(e)
            return {}
    

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """
        try:
            genres = {}
            generator = read_file_generator(self.ifilename)
            for line in generator:
               genres_line = line.strip().split(',')[-1]
               for genre in genres_line.split('|'):
                   genres[genre] = genres.get(genre,0)+1
            genres = dict(sorted(genres.items(), key = lambda x: x[1], reverse=True))
            return genres
        except Exception as e:
            print(e)
            return {}
        
    def most_genres(self, n, isreturnedid=0):
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        try:
            movies = {}
            generator = read_file_generator(self.ifilename)
            title = ''
            for line in generator:
                title, movies[title] = extract_title_and_genre_count(line, isreturnedid)
                movies = dict(sorted(movies.items(), key=lambda x: x[1], reverse=True)[:n])
            return movies
        except Exception as e:
            print(e)
            return {}

class Ratings:
    """
    Analyzing data from ratings.csv
    """
    
    def __init__(self, path_to_the_file='../datasets/ml-latest-small/ratings.csv'):
        """
        Put here any fields that you think you will need.
        """
        try:
            self.ifilename_ratings = path_to_the_file
            self.Movies.ifilename_ratings = self.Users.ifilename_ratings = path_to_the_file
        except Exception as e:
            print(e)
        
    
    class Movies:    
        def __init__(self):
            try:
                self.default_number_of_field = 1
                self.default_field_for_count = 2
            except Exception as e:
                print(e)

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts. 
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            try:
                ratings_by_year = {}
                generator = read_file_generator2(self.ifilename_ratings)
                for line in generator:
                    timestamp = line[3]
                    dt_object = datetime.fromtimestamp(int(timestamp))
                    year = dt_object.year
                    ratings_by_year[year] = ratings_by_year.get(year, 0) + 1
                
                
                ratings_by_year = dict(sorted(ratings_by_year.items(), key=lambda x: x[0]))
                return ratings_by_year
            except Exception as e:
                print(e)
                return {}
            
       
        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ... and the values are counts.
            Sort it by ratings ascendingly.
            """
            try:
                field_for_count = self.default_field_for_count
                distribution = {}
                generator = read_file_generator2(self.ifilename_ratings)
                for line in generator:
                    key = line[field_for_count]
                    distribution[key] = distribution.get(key, 0) + 1
                # movies class
                if field_for_count == 2:
                    distribution = dict(sorted(distribution.items(), key=lambda x: x[0]))
                # users class
                else:
                    distribution = dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))
                return distribution
            except Exception as e:
                print(e)
                return {}
        
        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings. 
            It is a dict where the keys are movie titles and the values are numbers.
            Sort it by numbers descendingly.
            """
            try:
                top_movies = {}
                top_movies_id = {}
                generator = read_file_generator2(self.ifilename_ratings)
                for line in generator:
                    movie_id = line[1]
                    top_movies_id[movie_id] = top_movies_id.get(movie_id, 0) + 1
    
                top_movies_id = dict((sorted(top_movies_id.items(), key=lambda x: x[1], reverse=True))[:n])
                top_movies = replace_id_with_name(top_movies_id)
                top_movies = dict(sorted(top_movies.items(), key=lambda x: x[1], reverse=True))
                return top_movies
            except Exception as e:
                print(e)
                return {}
        
        def top_by_ratings(self, n=-1, metric='average',isreturnedid=0):
            """
            The method returns top-n keys by the average or median of the ratings.
            It is a dict where the keys are ... and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            try:
                number_of_field = self.default_number_of_field
                top_keys_names = {}
                top_keys = defaultdict(list)
                generator = read_file_generator2(self.ifilename_ratings)
                if metric == 'average':
                    for line in generator:
                        key = line[number_of_field]
                        rating = line[2]
                        top_keys[key] = [(top_keys.get(key, [0,0])[0] + float(rating)), (top_keys.get(key, [0,0])[1] + 1)]
                
                    for key in top_keys:
                        top_keys_names[key] = round(top_keys[key][0] / top_keys[key][1], 2)
                    
                elif metric == 'median':
                    for line in generator:
                        key = line[number_of_field]
                        rating = float(line[2])
                        top_keys[key].append(rating)
                
                    for key in top_keys:
                        top_keys_names[key] = find_median(top_keys[key])
                    
                if number_of_field == 1:
                    top_keys_names = dict((sorted(top_keys_names.items(), key=lambda x: x[1], reverse=True)[:n]))
                    if isreturnedid==1:
                        return dict(sorted(top_keys_names.items(), key=lambda x: x[1], reverse=True))
                    else:
                        top_keys_names = replace_id_with_name(top_keys_names)
                return dict(sorted(top_keys_names.items(), key=lambda x: x[1], reverse=True))
            except Exception as e:
                print(e)
                return {}
        
        
        def top_controversial(self, n, isreturnedid=0):
            """
            The method returns top-n keys by the variance of the ratings.
            It is a dict where the keys are ... and the values are the variances.
            Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            try:
                number_of_field = self.default_number_of_field
                top_n_keys = {}
                dict_with_lists = defaultdict(list)
                generator = read_file_generator2(self.ifilename_ratings)
                for line in generator:
                    key = line[number_of_field]
                    rating = float(line[2])
                    dict_with_lists[key].append(rating)
                
                for key in dict_with_lists:
                    top_n_keys[key] = round(find_variance(dict_with_lists[key]), 2)
                
                top_n_keys = dict((sorted(top_n_keys.items(), key=lambda x: x[1], reverse=True)[:n]))
                if number_of_field == 1:
                    if isreturnedid==1:
                        return top_n_keys
                    else:
                        top_n_keys = replace_id_with_name(top_n_keys)
                        top_n_keys = dict(sorted(top_n_keys.items(), key=lambda x: x[1], reverse=True))
                return top_n_keys
            except Exception as e:
                print(e)
                return {}

    class Users(Movies):

        def __init__(self):
            try:
                self.default_number_of_field = 0
                self.default_field_for_count = 0
            except Exception as e:
                print(e)

        """
        In this class, three methods should work. 
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
        Inherit from the class Movies. Several methods are similar to the methods from it.
        """

###Dasha's classes
class Tags:
    def __init__(self, path_to_the_file='../datasets/ml-latest-small/tags.csv'):
        try:
            ##Put here any fields that you think you will need.
            self.path = path_to_the_file
            self.all_tags = []
            with open(self.path, "r") as f:
                lines = f.readlines()
                if lines:
                    for line in lines[1:]:
                        line = line.strip()
                        self.all_tags.append(line.lower().split(",")[2])
            self.unique_tags = set(self.all_tags)
        except Exception as e:
            print(e)

    def most_words(self, n):
        #The method returns top-n tags with most words inside. It is a dict where the keys are tags and the values are the number of words inside the tag.
        #Drop the duplicates. Sort it by numbers descendingly.
        try:
            big_tags = {tag: len(tag.split()) for tag in self.unique_tags}
            big_tags = {k: v for k, v in sorted(big_tags.items(), key=lambda item: item[1], reverse=True)[:n]}
            return big_tags
        except Exception as e:
            print(e)
            return {}

    def longest(self, n):
        #The method returns top-n longest tags in terms of the number of characters.
        #It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        try:
            big_tags = {tag: len(tag) for tag in self.unique_tags}
            big_tags = {k: v for k, v in sorted(big_tags.items(), key=lambda item: item[1], reverse=True)[:n]}
            big_tags = list(big_tags.keys())
            return big_tags
        except Exception as e:
            print(e)
            return []

    def most_words_and_longest(self, n):
        #The method returns the intersection between top-n tags with most words inside and top-n longest tags in terms of the number of characters.
        #Drop the duplicates. It is a list of the tags.
        try:
            most_words = self.most_words(n)
            longest = self.longest(n)
            big_tags = list(set(most_words.keys()) & set(longest))
            return big_tags
        except Exception as e:
            print(e)
            return []
        
    def most_popular(self, n):
        #The method returns the most popular tags. It is a dict where the keys are tags and the values are the counts.
        #Drop the duplicates. Sort it by counts descendingly.
        try:
            tag_counts = {}
            for tag in self.all_tags:
                if tag in tag_counts:
                    tag_counts[tag] += 1
                else:
                    tag_counts[tag] = 1
            popular_tags = {k: v for k, v in sorted(tag_counts.items(), key=lambda item: item[1], reverse=True)[:n]}
            return popular_tags
        except Exception as e:
            print(e)
            return {}
        
    def tags_with(self, word):
        #The method returns all unique tags that include the word given as the argument.
        #Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        try:
            tags_with_word = []
            for string in self.unique_tags:
                if (word.lower() in string.lower()):
                    tags_with_word.append(string)
            tags_with_word.sort()   
            return tags_with_word
        except Exception as e:
            print(e)
            return []

class Links:
    def __init__(self, path_to_the_file='../datasets/ml-latest-small/links.csv'):
             #Put here any fields that you think you will need.
        try:
            self.path1 = path_to_the_file
            self.path2 = "./links_parsed_data.csv"
            self.all_moviesId = []
            self.all_imdbId = []
            self.all_tmdbId = []
            self.upd_moviesId = []

            self.imdb_api_key = ""
            self.tmdb_api_key = ""
            generator1 = read_file_generator(self.path1)
            for line in generator1:
                    #line = line.strip()
                    self.all_moviesId.append(line.lower().split(",")[0])
                    self.all_imdbId.append(line.lower().split(",")[1])
                    self.all_tmdbId.append(line.lower().split(",")[2])

            if os.path.getsize(self.path2) != 0:
                generator2 = read_file_generator(self.path2)
                for line in generator2:
                    self.upd_moviesId.append(line.lower().split(",")[0])
        except Exception as e:
            print(e)


    def csv_init(self, movieId):
        try:
            with open (self.path2, "a") as f:
                imdb_info = []
                imdbId = self.all_imdbId[self.all_moviesId.index(movieId)]
                tmdbId = self.all_tmdbId[self.all_moviesId.index(movieId)]
                movie_data_imdb = self.get_movie_data_imdb(imdbId)
                movie_data_tmdb= self.get_movie_data_tmdb(tmdbId)    

                movie_info = []
                for field in ['movieId', 'Title', 'Director', 'Budget', 'Cumulative Worldwide Gross', 'Runtime']:
                    if field == "movieId":  
                        movie_info = [movieId]
                        self.upd_moviesId.append(movieId)
                    else:
                        value = str(self.parse_field(movie_data_imdb, movie_data_tmdb, field))
                        if value:
                            if  "," in value:
                                movie_info.append(f'"{value}"')
                            else:
                                movie_info.append(value)
                        else: 
                            raise ValueError(f"Error fetching {field} for movieId {movieId}")
                
                if  movie_data_imdb != None:
                    imdb_info.append(movie_info)
                
                    for row in imdb_info:
                        row = ",".join(row)
                        f.write(row + '\n')
        except Exception as e:
            print(e)

    def csv_init_for_dct(self, dct):
        try:
            lst = list(dct.keys())
            for movieId in lst:
                if movieId not in self.upd_moviesId:
                    self.csv_init(movieId)
            return lst
        except Exception as e:
            print(e)
            return []

    def analyze_csv(self, movieId, n):
        try:
            with open (self.path2, "r") as f:
                for line in f:
                    quoted = False
                    field = ''
                    fields = []

                    for char in line.strip():
                        if char == '"':
                            quoted = not quoted
                        elif char == ',' and not quoted:
                            fields.append(field)
                            field = ''
                            continue
                        field += char
                    fields.append(field)

                    if len(fields) == 6:
                        current_movieId = fields[0].strip('"')
                        title = fields[1]
                        director = fields[2].strip('"')
                        budget = fields[3].strip('"')
                        gross = fields[4].strip('"')
                        runtime = fields[5].strip('"')
                        if current_movieId == str(movieId):
                            if n == 1: 
                                return title
                            elif n == 2:
                                return director
                            elif n == 3:
                                return budget
                            elif n == 4:
                                return gross
                            elif n == 5:
                                return runtime
        except Exception as e:
            print(e)


    def get_movie_data_imdb(self, imdb_id):
        try:
            params = {"i": f"tt{imdb_id}","apikey": self.imdb_api_key}
            response = requests.get("http://www.omdbapi.com", params=params)
            response.raise_for_status()
            # time.sleep(0.5)
            movie_data = response.json()
            if movie_data.get("Response") == "False":
                raise ValueError(movie_data.get('Error'))
            return movie_data
        except Exception as e:
            print(f"Error fetching data for IMDb ID {imdb_id}: {e}")
            return None
        

    def get_movie_data_tmdb(self, tmdb_id):
        try:
            params = {"api_key": self.tmdb_api_key}
            response = requests.get(f"https://api.themoviedb.org/3/movie/{tmdb_id}", params=params)
            response.raise_for_status()
            # time.sleep(0.5)
            movie_data = response.json()
            if movie_data.get("status_code") == 7:
                raise ValueError(movie_data.get('status_message'))
            return movie_data
        except Exception as e:
            print(f"Error fetching data for TMDB ID {tmdb_id}: {e}")
            return None
    



    def parse_field(self, movie_data_imdb, movie_data_tmdb, field):
        try:
            if movie_data_imdb:
                if field == "Title":
                    return movie_data_imdb.get("Title", "N/A")
                if field == "Director":
                    return movie_data_imdb.get("Director", "N/A")
                elif field == "Runtime":
                    return movie_data_imdb.get("Runtime", "N/A")

            if movie_data_tmdb:
                if field == "Budget":
                    return movie_data_tmdb.get("budget", "N/A")
                elif field == "Cumulative Worldwide Gross":
                    return movie_data_tmdb.get("revenue", "N/A")
                
            if not movie_data_imdb:
                print(f"Error fetching IMDB data:{field}")
                raise ValueError(f"Error fetching IMDB data:{field}")

            if not movie_data_tmdb:
                print(f"Error fetching TMDB data:{field}")
                raise ValueError(f"Error fetching TMDB data:{field}")
            
        except Exception as e:
            print(e)
            return None
    
    def get_imdb(self, list_of_movies, list_of_fields):
        #The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        #For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        #The values should be parsed from the IMDB webpages of the movies.
        #Sort it by movieId descendingly.
        try:
            imdb_info = []
            for movieId in list_of_movies:
                if movieId in self.all_moviesId:
                    if (movieId in self.upd_moviesId and os.path.exists(self.path2)):
                            title = self.analyze_csv(movieId, 1)
                            director = self.analyze_csv(movieId, 2)
                            budget = self.analyze_csv(movieId, 3)
                            gross = self.analyze_csv(movieId, 4)
                            runtime = self.analyze_csv(movieId, 5)

                    else:
                        self.csv_init(movieId)
                        title = self.analyze_csv(movieId, 1)
                        director = self.analyze_csv(movieId, 2)
                        budget = self.analyze_csv(movieId, 3)
                        gross = self.analyze_csv(movieId, 4)
                        runtime = self.analyze_csv(movieId, 5)


                    movie_info = []
                    for field in list_of_fields:
                        if field not in ['movieId', 'Title', 'Director', 'Budget', 'Cumulative Worldwide Gross', 'Runtime']:
                            raise ValueError(f"{field} is invalid field. \nAllowed fields: movieId, Title, Director, Budget, Cumulative Worldwide Gross, Runtime")
                        if field=="movieId":
                            movie_info.append(movieId)
                        if field=="Title":
                            movie_info.append(title)
                        if field=="Director":
                            movie_info.append(director)
                        if field=="Budget":
                            movie_info.append(budget)
                        if field=="Cumulative Worldwide Gross":
                            movie_info.append(gross)
                        if field=="Runtime":
                            movie_info.append(runtime)

                    imdb_info.append(movie_info)

                else:
                    raise(ValueError(f"{movieId} is invalid movieId"))

            imdb_info.sort(key=lambda x: x[0], reverse=True)
            return imdb_info
        except Exception as e:
            print(e)
            return []
            
    def top_directors(self, n):
        #The method returns a dict with top-n directors where the keys are directors and 
        #the values are numbers of movies created by them. Sort it by numbers descendingly.
        try:
            top_directors = {}
            director_list = []

            for movieId in self.upd_moviesId:
                if os.path.getsize(self.path2) != 0:
                    director = self.analyze_csv(movieId, 2)
                else:
                    self.csv_init(movieId)
                    director = self.analyze_csv(movieId, 2)

                if director:
                    director_list.append(director)

            top_directors = dict_topn(director_list, n)
            return top_directors
        except Exception as e:
            print(e)
            return {}
    
    def all_movies_by_director(self, top_directors, cur_director):
        try:
            if top_directors:
                director_list = []
                title_list = []
                final_list = []
                generator = read_file_generator(self.path2)
                for line in generator:
                    director = line.strip().split(',')[2]
                    title = line.strip().split(',')[1]
                    director_list.append(director)
                    title_list.append(title)
                
                    if director == cur_director and cur_director in top_directors:
                        final_list.append(title)
                return final_list
            else:
                raise ValueError("Top directors are not defined")
        except Exception as e:
            print(e)
            return []
        
    def most_expensive(self, n):
        #The method returns a dict with top-n movies where the keys are movie titles and
        #the values are their budgets. Sort it by budgets descendingly.
        try:
            top_movies = {}
            budget_list = []
            title_list = []

            for movieId in self.upd_moviesId:
                if os.path.getsize(self.path2) != 0:
                    title = self.analyze_csv(movieId, 1)
                    budget = self.analyze_csv(movieId, 3)
                else:
                    self.csv_init(movieId)
                    title = self.analyze_csv(movieId, 1)
                    budget = self.analyze_csv(movieId, 3)

                if title and budget:
                    budget_list.append(budget)
                    title_list.append(title)

                
            for i in range(len(budget_list)):
                if budget_list[i] != 'None':
                    budget = int(budget_list[i])
                    budget_list[i] = int(budget)

            top_movies = dict(zip(title_list, budget_list))
            top_movies = {k: v for k, v in top_movies.items() if v != 'None'}
            top_movies = {k: v for k, v in sorted(top_movies.items(), key=lambda item: item[1], reverse=True)[:n]}

            return top_movies
        except Exception as e:
            print(e)
            return {}
        
    def most_profitable(self, n):
        #The method returns a dict with top-n movies where the keys are movie titles and
        #the values are the difference between cumulative worldwide gross and budget.
        #Sort it by the difference descendingly.
        try:
            profits = {}
            title_list = []
            budget_list = []
            gross_list = []

            for movieId in self.upd_moviesId:
                if os.path.getsize(self.path2) != 0:
                    title = self.analyze_csv(movieId, 1)
                    budget = self.analyze_csv(movieId, 3)
                    gross = self.analyze_csv(movieId, 4)

                else:
                    self.csv_init(movieId)
                    title = self.analyze_csv(movieId, 1)
                    budget = self.analyze_csv(movieId, 3)
                    gross = self.analyze_csv(movieId, 4)

                if title and budget and gross:
                    budget_list.append(budget)
                    title_list.append(title)
                    gross_list.append(gross)

            for i in range(len(budget_list)):
                if budget_list[i] != 'None' and  gross_list[i] != 'None':
                    budget = float(budget_list[i])
                    gross = float(gross_list[i])
                    profits[self.all_moviesId[i]] = float(gross - budget)



            profits = dict(zip(title_list, list(profits.values())))
            profits = {k: v for k, v in profits.items() if v != 'None'}
            profits = {k: v for k, v in sorted(profits.items(), key=lambda item: item[1], reverse=True)[:n]}
            return profits
        except Exception as e:
            print(e)
            return {}
            
    def longest(self, n):
        #The method returns a dict with top-n movies where the keys are movie titles and
        #the values are their runtime. If there are more than one version – choose any.
        #Sort it by runtime descendingly.
        try:
            runtimes = {}
            title_list = []
            runtime_list = []

            for movieId in self.upd_moviesId:
                if os.path.getsize(self.path2) != 0:
                    title = self.analyze_csv(movieId, 1)
                    runtime = self.analyze_csv(movieId, 5)
                else:
                    self.csv_init(movieId)
                    title = self.analyze_csv(movieId, 1)
                    runtime = self.analyze_csv(movieId, 5)

                if title and runtime:
                    title_list.append(title)
                    runtime_list.append(runtime)
            
            runtimes= dict(zip(title_list, runtime_list))
            runtimes = {k: (v if v is not None else '0') for k, v in runtimes.items()}
            sorted_runtimes = {k: v for k, v in sorted(runtimes.items(), key=lambda item: runtime_to_minutes(item[1]), reverse=True)[:n]}
            return sorted_runtimes
        except Exception as e:
            print(e)
            return {}

        
    def top_cost_per_minute(self, n):
        #The method returns a dict with top-n movies where the keys are movie titles and
        #the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it. 
        #The values should be rounded to 2 decimals. Sort it by the division descendingly.
        try:
            costs = {}
            title_list = []
            runtime_list = []
            budget_list = []
            valid_ids = []

            for movieId in self.upd_moviesId:
                if os.path.getsize(self.path2) != 0:
                    title = self.analyze_csv(movieId, 1)
                    budget = self.analyze_csv(movieId, 3)
                    runtime = self.analyze_csv(movieId, 5)

                else:
                    self.csv_init(movieId)
                    title = self.analyze_csv(movieId, 1)
                    budget = self.analyze_csv(movieId, 3)
                    runtime = self.analyze_csv(movieId, 5)

                if (title != 'None') and (budget != 'None') and (runtime != 'None'):
                    valid_ids.append(movieId)
                    title_list.append(title)
                    budget_list.append(budget)
                    runtime_list.append(runtime)

            for i in range(len(budget_list)):
                    budget = int(budget_list[i])
                    runtime = int(runtime_to_minutes(runtime_list[i]))
                    costs[valid_ids[i]] = budget / runtime

            formatted_costs =  {k: round(v, 2) for k, v in costs.items()}
            costs = dict(zip(title_list, list(formatted_costs.values())))
            costs = {k: (v if v is not None else 'No data') for k, v in costs.items()}
            costs = {k: v for k, v in sorted(costs.items(), key=lambda item: item[1], reverse=True)[:n]}
            return costs
        except Exception as e:
            print(e)
            return {}

class Graph:
    def text_histogram(self, data, number=100, sortBy=1):
        try:
            lines = []
            max_count = max(data.values())
            max_length = max(len(str(movie)) for movie in data.keys())
            width = max_length + 2
            
            for movie, count in sorted(data.items(), key=lambda x: -x[sortBy]):
                percentage = count / max_count * number
                line = f"{str(movie)[:width]:<{width}} {'■' * int(percentage//5)} {count}"
                lines.append(line)
                
            return lines
        
        except Exception as e:
            return [str(e)]


class Tests:
    """Unified test class for Movies and Ratings functionality"""
    ##Vovchik's tests    
    # Fixtures
    @pytest.fixture
    def movies_instance(self):
        return Movies('../datasets/ml-latest-small/movies.csv')
    
    @pytest.fixture
    def ratings_instance(self):
        return Ratings('../datasets/ml-latest-small/ratings.csv')
    
    @pytest.fixture
    def ratings_movies_instance(self, ratings_instance):
        return ratings_instance.Movies()
    
    @pytest.fixture
    def ratings_users_instance(self, ratings_instance):
        return ratings_instance.Users()

    # Movies class tests
    def test_movies_dist_by_release_type(self, movies_instance):
        result = movies_instance.dist_by_release()
        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, str)
            assert isinstance(value, int)

    def test_movies_dist_by_release_sorted(self, movies_instance):
        result = movies_instance.dist_by_release()
        values = list(result.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1))

    def test_movies_dist_by_genres_type(self, movies_instance):
        result = movies_instance.dist_by_genres()
        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, str)
            assert isinstance(value, int)

    def test_movies_dist_by_genres_sorted(self, movies_instance):
        result = movies_instance.dist_by_genres()
        values = list(result.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1))

    def test_movies_most_genres_type(self, movies_instance):
        result = movies_instance.most_genres(5)
        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, str)
            assert isinstance(value, int)

    def test_movies_most_genres_sorted(self, movies_instance):
        result = movies_instance.most_genres(5)
        values = list(result.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1))

    # Ratings.Movies class tests
    def test_ratings_dist_by_year_type(self, ratings_movies_instance):
        result = ratings_movies_instance.dist_by_year()
        assert isinstance(result, dict)
        for key in result:
            assert isinstance(key, int)
        for value in result.values():
            assert isinstance(value, int)

    def test_ratings_dist_by_year_sorted(self, ratings_movies_instance):
        result = ratings_movies_instance.dist_by_year()
        years = list(result.keys())
        assert all(years[i] <= years[i+1] for i in range(len(years)-1))

    def test_ratings_dist_by_rating_type(self, ratings_movies_instance):
        result = ratings_movies_instance.dist_by_rating()
        assert isinstance(result, dict)
        for key in result:
            assert isinstance(key, str)  # Ratings stored as strings in CSV
        for value in result.values():
            assert isinstance(value, int)

    def test_ratings_dist_by_rating_sorted(self, ratings_movies_instance):
        result = ratings_movies_instance.dist_by_rating()
        ratings = [float(k) for k in result.keys()]
        assert all(ratings[i] <= ratings[i+1] for i in range(len(ratings)-1))

    def test_ratings_top_by_num_type(self, ratings_movies_instance):
        result = ratings_movies_instance.top_by_num_of_ratings(5)
        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, str)
            assert isinstance(value, int)

    def test_ratings_top_by_num_sorted(self, ratings_movies_instance):
        result = ratings_movies_instance.top_by_num_of_ratings(5)
        values = list(result.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1))
    
    
    """
    The method returns top-n keys by the average or median of the ratings.
    It is a dict where the keys are ... and the values are metric values.
    Sort it by metric descendingly.
    The values should be rounded to 2 decimals.
    """
    def test_ratings_top_avg_type(self, ratings_movies_instance):
        result = ratings_movies_instance.top_by_ratings(5, metric='average')
        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, str)
            assert isinstance(value, float)

    def test_ratings_top_avg_sorted(self, ratings_movies_instance):
        result = ratings_movies_instance.top_by_ratings(5, metric='average')
        values = list(result.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1))

    def test_ratings_top_median_type(self, ratings_movies_instance):
        result = ratings_movies_instance.top_by_ratings(5, metric='median')
        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, str)
            assert isinstance(value, float)

    def test_ratings_top_median_sorted(self, ratings_movies_instance):
        result = ratings_movies_instance.top_by_ratings(5, metric='median')
        values = list(result.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1))


    """
    The method returns top-n keys by the variance of the ratings.
    It is a dict where the keys are ... and the values are the variances.
    Sort it by variance descendingly.
    The values should be rounded to 2 decimals.
    """
    def test_ratings_controversial_type(self, ratings_movies_instance):
        result = ratings_movies_instance.top_controversial(5)
        assert isinstance(result, dict)
        for key, value in result.items():
            assert isinstance(key, str)
            assert isinstance(value, float)

    def test_ratings_controversial_sorted(self, ratings_movies_instance):
        result = ratings_movies_instance.top_controversial(5)
        values = list(result.values())
        assert all(values[i] >= values[i+1] for i in range(len(values)-1))

    # Ratings.Users class tests
    """
    The 1st returns the distribution of users by the number of ratings made by them.
    """
    def test_users_dist_by_rating_type(self, ratings_users_instance):
        result = ratings_users_instance.dist_by_rating()
        assert isinstance(result, dict)
        for key in result:
            assert isinstance(key, str)  # User IDs from CSV are strings
        for value in result.values():
            assert isinstance(value, int)

    def test_users_dist_by_rating_sorted(self, ratings_users_instance):
        result = ratings_users_instance.dist_by_rating()
        counts = list(result.values())
        assert all(counts[i] >= counts[i+1] for i in range(len(counts)-1))
    
    # Ratings.Users class tests
    def test_users_dist_by_num_ratings_type(self, ratings_users_instance):
        """Test distribution of users by number of ratings (type checks)"""
        result = ratings_users_instance.dist_by_rating()  # Inherited method from Movies
        assert isinstance(result, dict)
        for user_id, count in result.items():
            assert isinstance(user_id, str)  # User IDs are strings from CSV
            assert isinstance(count, int)

    def test_users_dist_by_num_ratings_sorted(self, ratings_users_instance):
        """Test if user rating counts are sorted ascendingly (default behavior)"""
        result = ratings_users_instance.dist_by_rating()
        counts = list(result.values())
        assert all(counts[i] >= counts[i+1] for i in range(len(counts)-1))

    def test_users_dist_by_avg_rating_type(self, ratings_users_instance):
        """Test distribution of users by average rating (type checks)"""
        result = ratings_users_instance.top_by_ratings(metric='average')  # Inherited method
        assert isinstance(result, dict)
        for user_id, avg in result.items():
            assert isinstance(user_id, str)
            assert isinstance(avg, float)

    def test_users_dist_by_avg_rating_sorted(self, ratings_users_instance):
        """Test if average ratings are sorted descendingly"""
        result = ratings_users_instance.top_by_ratings(metric='average')
        averages = list(result.values())
        assert all(averages[i] >= averages[i+1] for i in range(len(averages)-1))

    def test_users_top_controversial_type(self, ratings_users_instance):
        """Test top controversial users (type checks)"""
        result = ratings_users_instance.top_controversial(5)  # Inherited method
        assert isinstance(result, dict)
        for user_id, var in result.items():
            assert isinstance(user_id, str)
            assert isinstance(var, float)

    def test_users_top_controversial_sorted(self, ratings_users_instance):
        """Test if variances are sorted descendingly"""
        result = ratings_users_instance.top_controversial(5)
        variances = list(result.values())
        assert all(variances[i] >= variances[i+1] for i in range(len(variances)-1))


    ###Dasha's tests
    @pytest.fixture
    def links_instance(self):
        return Links('../datasets/ml-latest-small/links.csv')
    
    # Test for csv_init
    def test_csv_init(self, links_instance):
        # Ensure the CSV file is created
        links_instance.csv_init('1')
        assert os.path.exists("links_parsed_data.csv")
    
    #Test for csv_init_for_dict
    def test_csv_init_for_dict(self, links_instance):
        links_instance.upd_moviesId = []
        test_dict = {'81132': 10, '26701': 8}
        lst = links_instance.csv_init_for_dct(test_dict)
        assert "81132" in links_instance.upd_moviesId
        assert "26701" in links_instance.upd_moviesId

        assert isinstance(lst, list)
            
        for id in lst:
            assert isinstance(id, str)


    # Test for analyze_csv
    def test_analyze_csv(self,links_instance):
        # Ensure the CSV file is created
        links_instance.csv_init('1')
    
        # Test with a valid movieId
        movieId = links_instance.all_moviesId[0]
        title = links_instance.analyze_csv(movieId, 1)
        assert isinstance(title, str)
    
        director = links_instance.analyze_csv(movieId, 2)
        assert isinstance(director, str)
    
        budget = links_instance.analyze_csv(movieId, 3)
        assert isinstance(budget, str)
    
        gross = links_instance.analyze_csv(movieId, 4)
        assert isinstance(gross, str)
    
        runtime = links_instance.analyze_csv(movieId, 5)
        assert isinstance(runtime, str)
    
    # Test for get_movie_data_imdb
    def test_get_movie_data_imdb(self,links_instance):
        # Test with a valid IMDb ID
        imdb_id = links_instance.all_imdbId[0]
        movie_data = links_instance.get_movie_data_imdb(imdb_id)
        assert isinstance(movie_data, dict)
    
        # Test with an invalid IMDb ID
        invalid_movie_data = links_instance.get_movie_data_imdb("invalid_id")
        assert invalid_movie_data is None
    
    # Test for get_movie_data_tmdb
    def test_get_movie_data_tmdb(self, links_instance):
        # Test with a valid TMDb ID
        tmdb_id = links_instance.all_tmdbId[0]
        movie_data = links_instance.get_movie_data_tmdb(tmdb_id)
        assert isinstance(movie_data, dict)
    
        # Test with an invalid TMDb ID
        invalid_movie_data = links_instance.get_movie_data_tmdb("invalid_id")
        assert invalid_movie_data is None
    
    
    # Test for parse_field
    def test_parse_field(self, links_instance):
        imdb_data = {"Title": "The Shawshank Redemption", "Director": "Frank Darabont", "Runtime": "142 min"}
        tmdb_data = {"budget": 25000000, "revenue": 28341469}
        
        title = links_instance.parse_field(imdb_data, None, "Title")
        assert isinstance(title, str)
        assert title == "The Shawshank Redemption"
        
        director = links_instance.parse_field(imdb_data, None, "Director")
        assert isinstance(director, str)
        assert director == "Frank Darabont"
        
        budget = links_instance.parse_field(None, tmdb_data, "Budget")
        assert isinstance(budget, int)
        assert budget == 25000000
        
        gross = links_instance.parse_field(None, tmdb_data, "Cumulative Worldwide Gross")
        assert isinstance(gross, int)
        assert gross == 28341469
    
    
        # Test for get_imdb
    def test_get_imdb(self, links_instance):
        list_of_movies = links_instance.all_moviesId[:5]  # Use first 5 movies for testing
        list_of_fields = ["movieId", "Title", "Director", "Budget", "Cumulative Worldwide Gross", "Runtime"]
        imdb_info = links_instance.get_imdb(list_of_movies, list_of_fields)
        assert isinstance(imdb_info, list)
        
        for movie_info in imdb_info:
            assert isinstance(movie_info, list)
            assert isinstance(movie_info[0], str)  
            assert isinstance(movie_info[1], str)  
            assert isinstance(movie_info[2], str)  
            assert isinstance(movie_info[3], str)  
            assert isinstance(movie_info[4], str)  
            assert isinstance(movie_info[5], str)  
    
        movie_ids = [int(movie_info[0]) for movie_info in imdb_info]
        assert movie_ids == sorted(movie_ids, reverse=True)

    # Test for top_directors
    def test_top_directors(self, links_instance):
        top_directors = links_instance.top_directors(5)
        assert isinstance(top_directors, dict)

        for top_director, count in top_directors.items():
            assert isinstance(top_director, str)
            assert isinstance(count, int)

        counts = list(top_directors.values())
        assert counts == sorted(counts, reverse=True)
    
    # Test for most_expensive
    def test_most_expensive(self, links_instance):
        top_movies = links_instance.most_expensive(5)
        assert isinstance(top_movies, dict)

        for title, budget in top_movies.items():
            assert isinstance(title, str)
            assert isinstance(budget, int)

        budgets = [int(budget) for budget in top_movies.values()]
        assert budgets == sorted(budgets, reverse=True)
    
    
    # Test for most_profitable
    def test_most_profitable(self, links_instance):
        top_movies = links_instance.most_profitable(5)
        assert isinstance(top_movies, dict)

        for title, profit in top_movies.items():
            assert isinstance(title, str)
            assert isinstance(profit, float)

        profits = [int(profit) for profit in top_movies.values()]
        assert profits == sorted(profits, reverse=True)
    
    # Test for longest
    def test_longest(self, links_instance):
        top_movies = links_instance.longest(5)
        assert isinstance(top_movies, dict)

        for title, runtime in top_movies.items():
            assert isinstance(title, str)
            assert isinstance(runtime, str)

        runtimes = [runtime_to_minutes(runtime) for runtime in top_movies.values()]
        assert runtimes == sorted(runtimes, reverse=True)
    
    
    # Test for top_cost_per_minute
    def test_top_cost_per_minute(self, links_instance):
        top_movies = links_instance.top_cost_per_minute(5)
        assert isinstance(top_movies, dict)

        for title, cost in top_movies.items():
            assert isinstance(title, str)
            assert isinstance(cost, float)

        costs = list(top_movies.values())
        assert costs == sorted(costs, reverse=True)


    # Test for all_movies_by_director
    def test_all_movies_by_director(self, links_instance):
        top_directors = links_instance.top_directors(5)
        cur_director = list(top_directors.keys())[0]
        movies = links_instance.all_movies_by_director(top_directors, cur_director)
        assert isinstance(movies, list)

        for movie in movies:
            assert isinstance(movie, str)
    
    
    @pytest.fixture
    def tags_instance(self):
        return Tags('../datasets/ml-latest-small/tags.csv')
    
    # Test for most_words
    def test_most_words(self, tags_instance):
        top_tags = tags_instance.most_words(5)
        assert isinstance(top_tags, dict)
        
        word_counts = list(top_tags.values())
        assert word_counts == sorted(word_counts, reverse=True)
    
        for tag in top_tags.keys():
            assert isinstance(tag, str)
    
    # Test for longest
    def test_longest(self, tags_instance):
        longest_tags = tags_instance.longest(5)
        assert isinstance(longest_tags, list)
        
        tag_lengths = [len(tag) for tag in longest_tags]
        assert tag_lengths == sorted(tag_lengths, reverse=True)
    
        for tag in longest_tags:
            assert isinstance(tag, str)
    
    # Test for most_words_and_longest
    def test_most_words_and_longest(self, tags_instance):
        intersection_tags = tags_instance.most_words_and_longest(5)
        assert isinstance(intersection_tags, list)
    
        for tag in intersection_tags:
            assert isinstance(tag, str)
    
        assert len(intersection_tags) == len(set(intersection_tags))
    
    # Test for most_popular
    def test_most_popular(self, tags_instance):
        popular_tags = tags_instance.most_popular(5)
        assert isinstance(popular_tags, dict)
        
        counts = list(popular_tags.values())
        assert counts == sorted(counts, reverse=True)

        for tag in popular_tags.keys():
            assert isinstance(tag, str)
    
    # Test for tags_with
    def test_tags_with(self, tags_instance):
        word = "funny"
        tags_with_word = tags_instance.tags_with(word)
        
        assert isinstance(tags_with_word, list)
        
        assert tags_with_word == sorted(tags_with_word)
    
        for tag in tags_with_word:
            assert isinstance(tag, str)

        for tag in tags_with_word:
            assert word in tag
    
        non_existent_word = "nonexistentword"
        tags_with_non_existent_word = tags_instance.tags_with(non_existent_word)
        assert isinstance(tags_with_non_existent_word, list)
        assert len(tags_with_non_existent_word) == 0    

    @pytest.fixture
    def graph_instance(self):
        return Graph()
    
    def test_return_type_and_element_types(self, graph_instance):
        sample_movie_data = {
            "The Shawshank Redemption": 95,
            "The Godfather": 92,
            "The Dark Knight": 90,
            "Pulp Fiction": 89,
            "Fight Club": 88
        }
        
        result = graph_instance.text_histogram(sample_movie_data)
        assert isinstance(result, list)
        assert all(isinstance(line, str) for line in result)
    

if __name__ == "__main__":
    try:
            links= Links('../datasets/ml-latest-small/links.csv')
            tags = Tags('../datasets/ml-latest-small/tags.csv')
            ratings = Ratings('../datasets/ml-latest-small/ratings.csv')
            movies = Movies('../datasets/ml-latest-small/movies.csv')


    except Exception as e:
        print(f"Error! {e}")