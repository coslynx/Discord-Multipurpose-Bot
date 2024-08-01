<h1 align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
  <br>Discord-Multipurpose-Bot
</h1>
<h3 align="center">◦ A versatile Discord bot designed to enhance server management, provide entertainment options, and facilitate community interaction.</h3>
<h3 align="center">◦ Developed with the software and tools below.</h3>
<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue" alt="">
  <img src="https://img.shields.io/badge/Framework-Discord.py-red" alt="">
  <img src="https://img.shields.io/badge/Database-PostgreSQL%20or%20MySQL-blue" alt="">
  <img src="https://img.shields.io/badge/API-Discord-black" alt="">
</p>
<p align="center">
  <img src="https://img.shields.io/github/last-commit/spectra-ai-codegen/Discord-Multipurpose-Bot?style=flat-square&color=5D6D7E" alt="git-last-commit" />
  <img src="https://img.shields.io/github/commit-activity/m/spectra-ai-codegen/Discord-Multipurpose-Bot?style=flat-square&color=5D6D7E" alt="GitHub commit activity" />
  <img src="https://img.shields.io/github/languages/top/spectra-ai-codegen/Discord-Multipurpose-Bot?style=flat-square&color=5D6D7E" alt="GitHub top language" />
</p>

## 📑 Table of Contents
- [📍 Overview](#overview)
- [📦 Features](#features)
- [📂 Repository Structure](#repository-structure)
- [💻 Installation](#installation)
- [🏗️ Usage](#usage)
- [🌐 Hosting](#hosting)
- [📄 License](#license)
- [👏 Authors and Acknowledgments](#authors-and-acknowledgments)

## 📍 Overview

This repository contains the code for a Discord multipurpose bot project, aiming to create a versatile bot capable of handling various tasks and functionalities within a Discord server. The bot will enhance server management, provide entertainment options, and facilitate community interaction, ultimately contributing to a more engaging and vibrant server environment.

## 📦 Features

**Moderation & Management:**

- **Auto-moderation:**  Filters messages for spam, offensive language, and inappropriate content.
- **Role Management:** Creates, manages, and assigns roles based on user attributes and server settings.
- **Customizable Command System:** Allows users to define their own commands for server-specific actions.
- **Member Tracking:** Tracks user activity, message count, voice channel usage, and time spent online.

**Entertainment:**

- **Music Playback:** Integrates with music streaming services like YouTube, Spotify, and SoundCloud.
- **Trivia & Games:** Hosts interactive trivia games, word games, and simple logic puzzles.
- **Image & Meme Generation:** Generates random memes, images, and text-based content.
- **Randomized Content:** Provides random facts, jokes, or quotes based on pre-defined datasets.

**Community Tools:**

- **Poll & Survey Creation:** Enables users to create polls and surveys to gather opinions from server members.
- **Event Scheduling & Reminders:** Provides a system for scheduling events, deadlines, or reminders.
- **Customizable Announcements:** Allows server administrators to create and schedule announcements.
- **Discussion Forums:** Creates dedicated channels for structured discussions and conversations.

**Integration & Automation:**

- **API Integration:** Leverages various external APIs to access and integrate functionalities.
- **Automation:** Automates repetitive tasks such as welcoming new members, assigning roles, and triggering actions based on events.
- **Customizable Triggers:** Allows server administrators to set up triggers based on specific keywords or actions.
- **Advanced Analytics:** Tracks bot usage, command popularity, user engagement, and feature utilization.

## 📂 Repository Structure

```
└── bot
    ├── commands
    │   ├── fun
    │   │   ├── meme.py
    │   │   ├── trivia.py
    │   │   └── random_content.py
    │   ├── moderation
    │   │   ├── automod.py
    │   │   ├── role_management.py
    │   │   └── member_tracking.py
    │   ├── music
    │   │   └── music_player.py
    │   ├── utility
    │   │   ├── poll.py
    │   │   ├── event_reminder.py
    │   │   ├── announce.py
    │   │   └── help.py
    │   └── custom_commands
    │       └── custom_commands.py
    ├── database
    │   ├── database_setup.py
    │   ├── database_models.py
    │   └── database_functions.py
    ├── utils
    │   ├── api_helpers.py
    │   ├── image_utils.py
    │   ├── nlp_utils.py
    │   ├── logging_utils.py
    │   └── error_handling.py
    └── main.py
└── requirements.txt

```

## 💻 Installation

### 🔧 Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- PostgreSQL or MySQL (depending on chosen database)
- Discord Bot Token (obtain from Discord Developer Portal)

### 🚀 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/spectra-ai-codegen/Discord-Multipurpose-Bot.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd Discord-Multipurpose-Bot
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up the database:**
   - **PostgreSQL:**
     - Create a database using pgAdmin or the command line.
     - Update the database credentials in `bot/database/database_setup.py`.
   - **MySQL:**
     - Create a database using MySQL Workbench or the command line.
     - Update the database credentials in `bot/database/database_setup.py`.
5. **Create an environment file:**
   - Create a `.env` file in the project root directory.
   - Add the following lines:
     ```
     DISCORD_TOKEN=your_discord_bot_token
     DATABASE_URL=postgresql://user:password@host:port/database_name 
     ```
     (Replace the placeholders with your actual Discord bot token and database connection string.)
6. **Run the bot:**
   ```bash
   python bot/main.py
   ```

## 🏗️ Usage

Once the bot is running, you can use the following commands:

**Moderation & Management:**

- `!createrole <role_name>`: Create a new role with specified properties.
- `!assignrole <user_id> <role_name>`: Assign a role to a user.
- `!removerole <user_id> <role_name>`: Remove a role from a user.
- `!serverinfo`: Display server statistics and information.

**Entertainment:**

- `!meme`: Generate and display a random meme.
- `!trivia`: Start a trivia game.
- `!random <type>` (e.g., `!random fact`, `!random joke`): Display random content.
- `!play <song_url>`: Play a song from a music streaming service.
- `!skip`: Skip to the next song in the queue.
- `!pause`: Pause the current song.
- `!resume`: Resume playback.
- `!stop`: Stop playback and clear the music queue.

**Community Tools:**

- `!poll <question> <options>`: Create a poll with a question and options.
- `!event <date> <time> <description>`: Schedule an event.
- `!announce <channel> <message>`: Send an announcement to a specific channel.
- `!help`: Display a list of available commands.

**Integration & Automation:**

- `!weather <location>`: Fetch weather data for a specific location.
- `!news`: Display current news headlines.

## 🌐 Hosting

### 🚀 Deployment Instructions

1. **Set up a hosting platform:** Consider using services like Heroku, AWS, Google Cloud Platform, or a dedicated server.
2. **Create a deployment script or use a CI/CD pipeline:** Automate the deployment process to ensure consistency and ease of updates.
3. **Configure environment variables:** Set the necessary environment variables (Discord token, database connection string) in the hosting platform's environment settings.
4. **Deploy the code:** Follow the specific instructions for your chosen hosting platform to deploy the bot's code.

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors and Acknowledgments

- **Author Name** - [Spectra.codes](https://spectra.codes)
- **Creator Name** - [DRIX10](https://github.com/Drix10)

<p align="center">
    <h1 align="center">🌐 Spectra.Codes</h1>
  </p>
  <p align="center">
    <em>Why only generate Code? When you can generate the whole Repository!</em>
  </p>
  <p align="center">
	<img src="https://img.shields.io/badge/Developer-Drix10-red" alt="">
	<img src="https://img.shields.io/badge/Website-Spectra.codes-blue" alt="">
	<img src="https://img.shields.io/badge/Backed_by-Google_&_Microsoft_for_Startups-red" alt="">
	<img src="https://img.shields.io/badge/Finalist-Backdrop_Build_v4-black" alt="">
  <p>