import sqlite3

# Create a SQLite database
def create_database():
    conn = sqlite3.connect('playlist.db')
    cursor = conn.cursor()

    # Create tables to store songs and favorite artists
    cursor.execute('''CREATE TABLE IF NOT EXISTS songs
                      (id INTEGER PRIMARY KEY, title TEXT, genre TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS artists
                      (id INTEGER PRIMARY KEY, name TEXT)''')

    conn.commit()
    conn.close()

# Function to add a song to the playlist
def add_song_to_db(title, genre):
    conn = sqlite3.connect('playlist.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO songs (title, genre) VALUES (?, ?)", (title, genre,))
    conn.commit()

    conn.close()

# Function to add an artist to favorites
def add_artist_to_db(name):
    conn = sqlite3.connect('playlist.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO artists (name) VALUES (?)", (name,))
    conn.commit()

    conn.close()

# Function to list all songs in the playlist
def list_songs_from_db():
    conn = sqlite3.connect('playlist.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM songs")
    songs = cursor.fetchall()

    conn.close()

    return songs

# Function to search for songs by title
def search_song_by_title(title):
    conn = sqlite3.connect('playlist.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM songs WHERE title LIKE ?", ('%' + title + '%',))
    songs = cursor.fetchall()

    conn.close()

    return songs

# Function to list favorite artists
def list_artists_from_db():
    conn = sqlite3.connect('playlist.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM artists")
    artists = cursor.fetchall()

    conn.close()

    return artists

# Function to remove a song from the playlist and reposition song IDs
def remove_song_from_db(song_id):
    conn = sqlite3.connect('playlist.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM songs WHERE id=?", (song_id,))
    conn.commit()

    # Retrieve all remaining songs after deletion
    cursor.execute("SELECT id FROM songs")
    remaining_songs = cursor.fetchall()

    # Reposition song IDs
    for idx, song in enumerate(remaining_songs, start=1):
        cursor.execute("UPDATE songs SET id=? WHERE id=?", (idx, song[0]))
        conn.commit()

    conn.close()


class Playlist:
    def __init__(self):
        self.songs = []

    def add_song(self, title, genre):
        self.songs.append(Song(title, genre))
        add_song_to_db(title, genre)

    def list_songs(self):
        songs = list_songs_from_db()
        if not songs:
            print("Playlist is empty.")
        else:
            print("Playlist:")
            for song in songs:
                print(f"{song[0]}. {song[1]} - {song[2]}")

    def search_song(self, title):
        songs = search_song_by_title(title)
        if not songs:
            print("Song not found.")
        else:
            print("Search Results:")
            for song in songs:
                print(f"{song[0]}. {song[1]} - {song[2]}")

    def remove_song(self, song_id):
        remove_song_from_db(song_id)

    def list_songs_by_genre(self, genre):
        conn = sqlite3.connect('playlist.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM songs WHERE genre=?", (genre,))
        songs = cursor.fetchall()

        conn.close()

        if not songs:
            print("No songs found in this genre.")
        else:
            print(f"Songs in genre '{genre}':")
            for song in songs:
                print(f"{song[0]}. {song[1]}")

class Song:
    def __init__(self, title, genre):
        self.title = title
        self.genre = genre

def main():
    create_database()

    playlist = Playlist()

    while True:
        print("\n****Here is your Menu!****")
        print("1. Add a song to the playlist")
        print("2. List all songs in the playlist")
        print("3. Search for a song by title")
        print("4. Remove a song from the playlist")
        print("5. Add a favorite artist")
        print("6. List favorite artists")
        print("7. List songs by genre")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter the title of the song: ")
            genre = input("Enter the genre of the song: ")
            playlist.add_song(title, genre) 
        elif choice == "2":
            playlist.list_songs()
        elif choice == "3":
            title = input("Enter the title of the song to search: ")
            playlist.search_song(title)
        elif choice == "4":
            playlist.list_songs()
            song_id = int(input("Enter the ID of the song to remove: "))
            playlist.remove_song(song_id)
        elif choice == "5":
            name = input("Enter the name of the favorite artist: ")
            add_artist_to_db(name)
            print("Artist added to favorites.")
        elif choice == "6":
            artists = list_artists_from_db()
            if not artists:
                print("No favorite artists.")
            else:
                print("Favorite Artists:")
                for artist in artists:
                    print(f"{artist[0]}. {artist[1]}")
        elif choice == "7":
            genre = input("Enter the genre to list songs: ")
            playlist.list_songs_by_genre(genre)
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()