# DyllanBot
Discord bot for personal server.

## Docker Compose
```
version: "3"
services:
  dyllan-bot:
    build:
        context: 'https://github.com/AnthonyOGorman/DyllanBot.git'
        dockerfile: Dockerfile
    restart: unless-stopped
    environment:
        - TOKEN=CHANGEME
```
