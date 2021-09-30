import external_movie_data
import fresh_tomatoes
import json
import media
from random import randint
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()
def validate_movie_info(movie_info):
    # TODO: Aritmethic Error handling
    # Convert and round rating range
    rating = round(movie_info['rating'] * 5 / 10, 1)

    # TODO: Supply the list to the view and loop through it
    # Check if genres list is empty
    genres_list = movie_info['genres'] if movie_info['genres'] else ['Uncategorized']

    # Check if genres list is empty
    overview = movie_info['overview'] if movie_info['overview'] else 'No overview available'

    # Check if tagline is empty
    tagline = movie_info['tagline'] if movie_info['tagline'] else '--'

    return rating, genres_list, overview, tagline


def construct_movie(movie_info, movies_list):
    # Obtain validated movie's info
    rating, genres_list, overview, tagline = validate_movie_info(movie_info)

    # Create a custom media 'Movie' object and populate a list of movies
    movie = media.Movie(movie_info['title'].encode('utf-8'), overview.encode('utf-8'), movie_info['poster_image'],
                        movie_info['video_trailer'], tagline, genres_list, movie_info['release_date'],
                        movie_info['runtime'], rating)
    movies_list.append(movie)

# List of favourite movies, fill in with yours
target = open('movie.txt','r')
strn = target.read()
mv_searchlist = []
movies_searchlist = strn.split("\n")
for i in movies_searchlist:
	if ':' in i:
		continue
	mv_searchlist.append(i)


# Empty list to be populated with media 'Movie' objects
movies = []

print str(len(mv_searchlist)) + " movies found"
print "Connecting 'themoviedb' to get some movie data.."

# Loop through movies to grab some cool info
l = randint(0,len(mv_searchlist))
for index, movie in enumerate(mv_searchlist[l:l+3]):
    index += 1
    movie_id = external_movie_data.get_movie_id(movie)
    if movie_id != -1:
        movie_json = external_movie_data.get_movie_info(movie_id)
        print 'Movie #' + str(index) + ' fetched!'
        # Create own 'Movie' object and append to list
        construct_movie(json.loads(movie_json), movies)

# Call the helper function to build dynamically an static HTML page
fresh_tomatoes.open_movies_page(movies)
