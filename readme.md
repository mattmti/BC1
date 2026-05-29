# Travel Tour Generator

A command-line app to manage a list of cities and generate optimized travel tours between them.

## What it does

- Create an account and log in
- Add cities to your personal list (uses Google Maps API to get coordinates)
- Generate an optimized travel route through all your cities
- Save tours as public or private
- View your saved tours and other users' public tours

## How it works

The tour generator groups cities that are within 50km of each other, picks the best city in each group to stay at (hotel city), then builds the shortest route between all groups using a nearest neighbor algorithm.

## Installation

```bash
pip install bcrypt python-dotenv requests
```

## Setup

Create a `.env` file with your Google Maps API key: