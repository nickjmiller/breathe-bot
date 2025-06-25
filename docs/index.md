# breathe-bot

Guided breathing assistant for discord. Invite the bot to your channel and configure your breathing, then follow the exercises.

[![Build and test/lint/format](https://github.com/nickjmiller/breathe-bot/actions/workflows/python-app.yml/badge.svg)](https://github.com/nickjmiller/breathe-bot/actions/workflows/python-app.yml)

## Setup

1. [Invite the bot to your server](https://discord.com/oauth2/authorize?client_id=1385297548054495306)
1. Join a voice channel and start with a preset: `/breathe box`
    * You can customize the number of rounds: `/breathe box 3` to do 3 rounds of box breathing

Have your own guided breathing plan? You can completely customize the exercise:
```bash
/breathe custom {rounds} {breathe_in} {hold_in} {breathe_out} {hold_out}
```


### Presets

There are currently two presets for guided breathing:

#### Box Breathing

This is a breathing technique where each inhale, hold, and exhale (and hold) take the same amount of time.

[Cherry-picked study on the potential benefits of this technique](https://pmc.ncbi.nlm.nih.gov/articles/PMC9873947/)

#### 4-7-8 Breathing

This technique involves inhaling, holding the breath, and then exhaling slowly.

[Cherry-picked study on potential benefits of this technique](https://pmc.ncbi.nlm.nih.gov/articles/PMC9277512/).

## Development

[Source code](https://github.com/nickjmiller/breathe-bot)

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

### Updating Docs

All documentation is included in the docs directory and built using [mkdocs](https://www.mkdocs.org/). The documentation site is updated on push to the repository automatically.

```bash
uvx mkdocs serve  # Preview the site locally
```