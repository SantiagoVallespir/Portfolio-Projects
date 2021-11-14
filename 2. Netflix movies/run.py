import movie_3
import movie_2

movie = str(input("Enter movie's name: "))

year = int(input("Enter release year: "))

columns = str(input("Enter data: "))


movie_data = movie_2.get_movie_id(movie, year)

details = movie_3.get_movie_data(movie_data, columns)

print(details)