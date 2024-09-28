import requests

# Constants for API and base URL
BASE_URL = "https://api.themoviedb.org/3"
API_KEY = "92a329a2d1ebf208d63c8108adafe5fa"  # Replace with your actual API key

# Function to search for a movie by title
def search_movie(title):
    # Define the query parameters
    params = {
        "api_key": API_KEY,  # API key for authentication
        "query": title  # Movie title to search for
    }
    
    try:
        # Make the GET request to the search movie endpoint
        response = requests.get(f"{BASE_URL}/search/movie", params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        # Parse the JSON response into a dictionary
        return response.json()  # This will return {} if response is empty
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}  # Return empty dictionary on error

# Function to get watch providers for a movie by ID
def get_watch_providers(movie_id):
    try:
        # Make the GET request to the watch/providers endpoint
        response = requests.get(f"{BASE_URL}/movie/{movie_id}/watch/providers", params={"api_key": API_KEY})
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        # Parse the JSON response into a dictionary
        return response.json().get('results', {})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching watch providers: {e}")
        return {}

# Function to display search results
def display_search_results(results):
    print("\nSearch Results:")
    
    # Check if 'results' key exists in the dictionary
    if 'results' in results:
        if results['results']:
            for index, movie in enumerate(results['results'], start=1):
                movie_id = movie['id']
                title = movie['title']
                release_date = movie.get('release_date', 'N/A')
                providers = get_watch_providers(movie_id)
                
                print(f"{index}. {title} (Release Date: {release_date})")
                
                if 'US' in providers:
                    us_providers = providers['US']
                    provider_names = [provider['provider_name'] for provider in us_providers.get('flatrate', [])]
                    if provider_names:
                        print(f"   Available on: {', '.join(provider_names)}")
                    else:
                        print("   No streaming providers available in the US.")
                else:
                    print("   No information on streaming providers available.")
        else:
            print("No results found.")
    else:
        print("Invalid response format. Please try again later.")

# Main function for the CLI application
def main():
    """
    Main function to run the CLI application.
    Provides a menu-driven interface for user interaction.
    """
    # Infinite loop to keep the CLI running until the user decides to exit
    while True:
        # Display the menu
        print("\nMovie Search CLI")
        print("1. Search for a movie")
        print("2. Exit")
        
        # Get user input for menu choice
        choice = input("Choose an option: ")
        
        if choice == '1':
            # Search for a movie
            title = input("Enter the movie title: ")
            search_results = search_movie(title)
            display_search_results(search_results)
            
        elif choice == '2':
            # Exit the application
            print("Exiting the application. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please choose a valid option.")

# Check if the script is being run directly
if __name__ == "__main__":
    main()
