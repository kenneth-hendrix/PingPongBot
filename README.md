# Discord Ping Pong Elo Bot

This Discord bot tracks and updates Elo ratings for users playing ping pong.

## Features

- **Elo Rating System**: Utilizes the Elo rating system to rank players based on match outcomes.
- **Commands**: Provides Discord slash commands for viewing Elo ratings, recording match results, and displaying rankings.
- **Persistence**: Uses a JSON file to persistently store Elo ratings outside the Docker container.

## Requirements

- Docker
- Docker Compose
- A Discord Bot Token
- A Guild (Server) ID where the bot will operate

## Setup Instructions

1. **Clone the Repository**

   Ensure you have Git installed on your system, then clone this repository to your local machine.

   ```bash
   git clone git@github.com:kenneth-hendrix/PingPongBot.git
   cd PingPongBot
   ```
2. **Configuration**

    Open the `docker-compose.yml` file in a text editor. Replace `"YOUR BOT TOKEN HERE"` and `"YOUR GUILD ID HERE"` with your actual Discord bot token and the guild ID, respectively.

3. **Building and Running the Bot**

    Navigate to the root directory of your project (where `docker-compose.yml` is located) and run:

    ```bash
    docker-compose up --build -d
    ```

    This will build the Docker image and start the container. The bot should now be running and connected to your Discord server.

4. **Interacting with the Bot**

    Use the following slash commands in your Discord server:

    - `/rankings`: Displays the top 10 players based on their Elo ratings.
    - `/bottom_rankings`: Lists the bottom 10 players.
    - `/match <@user>`: Initiates a match result recording. The mentioned user needs to confirm the loss.
    - `/myelo`: Displays the user's current Elo rating.
    - `/elo <@user>`: Displays the mentioned user's current Elo rating.

5. **Getting updates**
    In the event the bot is updates, use the following commands to get the update:

    ```bash
    docker-compose down
    git fetch --all
    git pull
    docker build -t ping-pong-bot:latest .
    docker-compose build
    docker-compose up -d
    ```

## File Persistence

Elo data is stored in `elo_data.json` at the root of the project directory and is mapped into the Docker container. This file is used to persist Elo ratings across bot restarts.

## Customization

Feel free to modify the Python script to add more features or change existing functionalities according to your preferences.

## Troubleshooting

- If the bot does not appear online or does not respond to commands, check the bot token and guild ID in the `docker-compose.yml` file.
- Ensure that the bot has the necessary permissions on your Discord server to read messages and send responses.

## Contributing

Contributions to the project are welcome. Please create a pull request or raise an issue for bugs and feature requests.
