
# Spotify Account Migration Tool

This Python application assists in migrating playlists, including songs, descriptions, and cover images , between two Spotify accounts.

## Features

-   Transfer playlists and their contents from one Spotify account to another.
-   Leverage the Spotify Web API for data retrieval and manipulation.
-   Secure user authorization through the OAuth 2.0 authorization code flow (requires separate authorization for both accounts).

## Requirements

-   Python 3.x
-   A Spotify developer account and app credentials for both source and destination accounts ([https://developer.spotify.com/](https://developer.spotify.com/))

## Setup

1.  **Install Dependencies:**
    
    Bash
    
    ```
    pip install requests
    pip install colorama
    ```
    
2.  **Create a Spotify Developer App:**
    
    -   Visit  [https://developer.spotify.com/](https://developer.spotify.com/)  and create a developer account.
    -   Create a new app and note down the Client ID and Client Secret for both the primary(source) and secondary(destination) Spotify accounts.
3.  **Configure Credentials:**
    
    -   Copy the example file and fill in your credentials:
        
        ```
        cp .env.example .env
        ```
    
    -   Update the values in `.env`:
        
        ```
        SPOTIFY_PRIMARY_CLIENT_ID=your_primary_client_id
        SPOTIFY_PRIMARY_CLIENT_SECRET=your_primary_client_secret
        SPOTIFY_SECONDARY_CLIENT_ID=your_secondary_client_id
        SPOTIFY_SECONDARY_CLIENT_SECRET=your_secondary_client_secret
        ```
4.  **Execute the App:**
    
    -   Run  `python app.py`  (or `uv run app.py`) to start the migration process.

## Usage

1.  The application will print an OAuth 2.0 authorization URL for the **source account**. Open it, approve access, and copy the `code` parameter from the redirect URL.
2.  Repeat the authorization process for the **destination account**.
3.  Once both authorizations are complete, the app will retrieve playlists from the source account, create corresponding playlists in the destination account (with descriptions if available), and transfer song data (URIs) to populate the new playlists.
4.  (Optional) Cover image transfer might require additional libraries or workarounds due to limitations in the Spotify API.

## Notes

-   Ensure the redirect URI in your app's configuration matches the one used in `.env` (default: `http://127.0.0.1:8731/callback`).

## Contributing

Feel free to submit pull requests for improvements or additional features. Make sure to follow code style conventions and include proper documentation for your changes.