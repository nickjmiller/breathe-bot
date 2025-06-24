# breathe-bot

Guided breathing assistant for discord. Invite the bot to your channel and configure your breathing, then follow the exercises.

[![Build and test/lint/format](https://github.com/nickjmiller/breathe-bot/actions/workflows/python-app.yml/badge.svg)](https://github.com/nickjmiller/breathe-bot/actions/workflows/python-app.yml)

![Logo](assets/logo_256.png?raw=true "Logo")

## Setup

1. Invite the bot: https://discord.com/oauth2/authorize?client_id=1385297548054495306
1. [Optional] Configure your breathing exercise: `/breatheconf`
    * By default there will be 5 rounds of four second intervals for each step: Breathing in, holding, breathing out, holding.
1. Join a voice channel and start: `/breathe`
    * There are also preset exercises, such as box breathing. Try `/breathe_preset box` (or `/breathe_preset_box 3` to do 3 rounds of box breathing)

## Development

### Prerequisites
1. Install uv: https://docs.astral.sh/uv/getting-started/installation/
1. Install ffmpeg: https://github.com/oop7/ffmpeg-install-guide?tab=readme-ov-file

> Optional - Install docker: https://docs.docker.com/engine/install/

### Running the app

Add a `.env` file with your BOT_SECRET: https://discord.com/developers/docs/quick-start/getting-started#fetching-your-credentials

```bash
uv run main.py        # Run the bot
uv run pytest         # Run tests
uvx ruff format       # Run the formatter
uvx ruff check --fix  # Run the linter
```

#### Docker

A simple compose file is included in this repo. Running `docker compose up` should build and run the dockerfile included here.