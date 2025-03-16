import requests
import random

class FreeKeys:
    def __init__(self):
        self.tmdb_keys = [
            'fb7bb23f03b6994dafc674c074d01761',
            'e55425032d3d0f371fc776f302e7c09b',
            '8301a21598f8b45668d5711a814f01f6',
            '8cf43ad9c085135b9479ad5cf6bbcbda',
            'da63548086e399ffc910fbc08526df05',
            '13e53ff644a8bd4ba37b3e1044ad24f3',
            '269890f657dddf4635473cf4cf456576',
            'a2f888b27315e62e471b2d587048f32e',
            '8476a7ab80ad76f0936744df0430e67c',
            '5622cafbfe8f8cfe358a29c53e19bba0',
            'ae4bd1b6fce2a5648671bfc171d15ba4',
            '257654f35e3dff105574f97fb4b97035',
            '2f4038e83265214a0dcd6ec2eb3276f5',
            '9e43f45f94705cc8e1d5a0400d19a7b7',
            'af6887753365e14160254ac7f4345dd2',
            '06f10fc8741a672af455421c239a1ffc',
            'fb7bb23f03b6994dafc674c074d01761',
            '09ad8ace66eec34302943272db0e8d2c'
        ]
        self.imdb_keys = [
            '4b447405',
            'eb0c0475',
            '7776cbde',
            'ff28f90b',
            '6c3a2d45',
            'b07b58c8',
            'ad04b643',
            'a95b5205',
            '777d9323',
            '2c2c3314',
            'b5cff164',
            '89a9f57d',
            '73a9858a',
            'efbd8357'
        ]

    def get_keys(self):
        tmdb_key = random.choice(self.tmdb_keys)
        imdb_key = random.choice(self.imdb_keys)
        return {'tmdb_key': tmdb_key, 'imdb_key': imdb_key}

class MovieSearcher:
    def __init__(self):
        self.keys = FreeKeys().get_keys()
        self.tmdb_api_key = self.keys['tmdb_key']
        self.tmdb_base_url = 'https://api.themoviedb.org/3'

    def search_movie(self, query):
        """Search for movies by title"""
        url = f"{self.tmdb_base_url}/search/movie"
        params = {
            'api_key': self.tmdb_api_key,
            'query': query
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                print(f"\nFound {len(results)} results for '{query}':\n")
                for idx, movie in enumerate(results[:5], 1):  # Show top 5
                    print(f"{idx}. Title: {movie.get('title')}")
                    print(f"   Release Date: {movie.get('release_date')}")
                    print(f"   Overview: {movie.get('overview')}\n")
                return results
            else:
                print("No results found.")
        else:
            print("Error occurred:", response.status_code, response.text)

    def get_movie_details(self, movie_id):
        """Fetch detailed movie info"""
        # Main Movie Details
        url = f"{self.tmdb_base_url}/movie/{movie_id}"
        params = {
            'api_key': self.tmdb_api_key,
            'append_to_response': 'credits,images,videos,external_ids'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print("\n=== Movie Full Details ===")
            print(f"Title: {data.get('title')}")
            print(f"Release Date: {data.get('release_date')}")
            print(f"Genres: {[genre['name'] for genre in data.get('genres', [])]}")
            print(f"Languages: {[lang['name'] for lang in data.get('spoken_languages', [])]}")
            print(f"Runtime: {data.get('runtime')} minutes")
            print(f"Budget: ${data.get('budget')}")
            print(f"Revenue: ${data.get('revenue')}")
            print(f"Rating: {data.get('vote_average')}")
            print(f"Overview: {data.get('overview')}")
            print(f"IMDb Link: https://www.imdb.com/title/{data['external_ids'].get('imdb_id')}")

            # Production Companies
            print("\nProduction Companies:")
            for company in data.get('production_companies', []):
                print(f"- {company.get('name')} ({company.get('origin_country')})")

            # Cast
            print("\nTop Cast:")
            for cast in data['credits']['cast'][:10]:  # Top 10 actors
                print(f"{cast.get('name')} as {cast.get('character')}")

            # Crew (Directors, Writers)
            print("\nCrew:")
            for crew in data['credits']['crew']:
                if crew['job'] in ['Director', 'Writer', 'Screenplay', 'Producer']:
                    print(f"{crew['job']}: {crew.get('name')}")

            # Posters
            print("\nPosters URLs:")
            base_img_url = "https://image.tmdb.org/t/p/w500"
            for poster in data['images']['posters'][:3]:  # Show top 3 posters
                print(base_img_url + poster.get('file_path'))

            # Trailers / Videos
            print("\nVideos/Trailers:")
            for video in data['videos']['results']:
                if video['site'] == "YouTube":
                    print(f"{video['type']}: https://www.youtube.com/watch?v={video['key']}")

        else:
            print("Error fetching details:", response.status_code, response.text)

# --- Usage ---

if __name__ == "__main__":
    ms = MovieSearcher()
    search_query = input("Enter movie title to search: ")
    results = ms.search_movie(search_query)

    if results:
        movie_id = results[0]['id']  # Taking first result
        ms.get_movie_details(movie_id)
