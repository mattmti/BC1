# Travel Planning Application

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Technology Choices](#technology-choices)
- [Algorithm Description](#algorithm-description)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [File Structure](#file-structure)
- [Tests](#tests)

---

## Project Overview

This application allows users to automatically generate an optimized travel tour visiting a maximum of locations. Users can manage their list of cities, generate optimized tours, and share their results publicly or privately.

---

## Architecture

The application is a Python console application structured around several modules:

```
BC1/
├── connexion/
│   └── login.py          # Authentication (login, account creation, password hashing)
├── gestion/
│   ├── addCity.py         # Add a city to the user's list via Google Maps API
│   ├── deleteCity.py      # Delete a specific city from the user's list
│   ├── deleteAll.py       # Delete all cities from the user's list
│   ├── viewList.py        # Display the user's city list
│   └── changeVisibility.py # Change the visibility of a tour
├── ittineraire/
│   └── generateTour.py    # Tour generation algorithm
├── json/
│   ├── users.json         # User accounts (hashed passwords)
│   ├── listCities.json    # Cities list per user
│   └── listTours.json     # Generated tours per user
├── tests/
│   ├── loginTest.py
│   ├── addCityTest.py
│   ├── deleteCityTest.py
│   ├── deleteAllTest.py
│   ├── generateTourTest.py
│   ├── viewListTest.py
│   └── viewMyTourTest.py
├── viewMyTour.py          # Display the connected user's tours
├── viewTour.py            # Display all public tours
└── menu.py                # Main menu (entry point)
```

### Data Flow

```
menu.py
  ├── login.py         → users.json
  ├── addCity.py       → Google Maps API → listCities.json
  ├── deleteCity.py    → listCities.json
  ├── deleteAll.py     → listCities.json
  ├── viewList.py      → listCities.json
  ├── generateTour.py  → listCities.json → listTours.json
  ├── viewMyTour.py    → listTours.json
  └── viewTour.py      → listTours.json
```

---

## Technology Choices

### Python
Python was chosen for its simplicity, readability and rich ecosystem of libraries. It allows rapid development while maintaining clean, modular code.

### bcrypt
bcrypt is the industry standard for password hashing. It automatically handles salting and produces irreversible hashes, making it secure against brute-force attacks. Alternative considered: `hashlib` (SHA-256), but bcrypt is more resistant to modern attacks.

### JSON
JSON files are used for data storage. This choice avoids the complexity of setting up a database (SQLite, PostgreSQL) while remaining human-readable and easy to maintain. The trade-off is that it is not suitable for large-scale production use.

### Google Maps Geocoding API
Used to retrieve GPS coordinates from a city name. It provides accurate and up-to-date geographic data worldwide. The API key is stored in a `.env` file for security.

### dotenv
Used to manage environment variables (API key) without hardcoding them in the source code.

### pytest
Standard Python testing framework. Allows writing unit tests with mocking capabilities to test functions without depending on real files or network calls.

---

## Algorithm Description

The tour generation algorithm is a two-level optimized **Nearest Neighbor** approach.

### Step 1 — City Grouping (`groupCities`)
Cities within 50km of each other are grouped together. The goal is to avoid unnecessary long-distance travel between nearby cities.

### Step 2 — Hotel City Selection (`findHotelCity`)
For each group, the most central city is selected as the "hotel city" — the one that minimizes the total distance to all other cities in the group. This is where the user will stay overnight.

### Step 3 — Path Between Hotels (`findPath`)
The hotels are connected using a **Nearest Neighbor** greedy algorithm: at each step, we move to the closest unvisited hotel. Within each group, all cities are visited in round trips from the hotel.

### Step 4 — Return to Start
After visiting all hotels and their groups, the algorithm returns to the starting city.

### Distance Formula
The distance between two cities is calculated using the spherical law of cosines:

```
D(Va, Vb) = R × arccos(sin(lat_a) × sin(lat_b) + cos(lat_a) × cos(lat_b) × cos(long_b - long_a))
```

Where:
- R = 6378.197 km (Earth radius)
- Coordinates are expressed in radians

### Why this algorithm is better than a naive solution
A random or naive solution would visit cities in arbitrary order, resulting in unnecessarily long paths. The two-level approach reduces travel distance by:
1. Grouping nearby cities to minimize short-range travel
2. Applying nearest neighbor between hotel cities to minimize long-range travel

---

## Installation

### Prerequisites
- Python 3.x
- pip

### Steps

1. Clone the repository:
```bash
git clone https://github.com/mattmti/BC1.git
cd BC1
```

2. Install dependencies:
```bash
pip install bcrypt requests python-dotenv pytest
```

3. Create a `.env` file at the root of the project:
```
API_Key=your_google_maps_api_key
```

4. Initialize the JSON files (if not already present):
```bash
echo "[]" > json/users.json
echo "[]" > json/listCities.json
echo "[]" > json/listTours.json
```

5. Run the application:
```bash
python menu.py
```

---

## Usage Guide

### Launch the application
```bash
python menu.py
```

### Main Menu (not logged in)
```
1. Login / Create account
2. View public tours
```

### Create an account
- Select option `1`
- Answer `no` to "Do you already have an account?"
- Choose a username and password (password is automatically hashed and stored securely)

### Login
- Select option `1`
- Answer `yes` to "Do you already have an account?"
- Enter your username and password

### Connected Menu
```
1. View my cities
2. Add a city
3. Generate a tour
4. View my tours
5. Delete a city
6. Delete all cities
7. Logout
```

### Add a city
- Select option `2`
- Enter the city name (e.g. "Paris", "Tokyo")
- The coordinates are automatically retrieved via the Google Maps API

### Generate a tour
- Select option `3`
- The algorithm generates an optimized tour from your city list
- The tour is displayed with each city in order and the total distance
- You are asked if you want to save the tour
- If yes, choose `public` or `private`

### View my tours
- Select option `4`
- All your saved tours are displayed with their distance and visibility

### View public tours
- Available from the main menu (option `2`) without being logged in
- Displays all tours shared publicly by all users

### Delete a city
- Select option `5`
- Enter the name of the city to delete

### Delete all cities
- Select option `6`
- Deletes all cities from your list

---

## JSON Data Structure

### users.json
```json
[
    {
        "pseudo": "alice",
        "password": "$2b$12$..."
    }
]
```

### listCities.json
```json
[
    {
        "pseudo": "alice",
        "villes": [
            {"nom": "Paris", "lat": 48.8575, "long": 2.3514},
            {"nom": "Lyon", "lat": 45.7640, "long": 4.8357}
        ]
    }
]
```

### listTours.json
```json
[
    {
        "pseudo": "alice",
        "tours": [
            {
                "id": 1,
                "villes": ["Paris", "Lyon", "Marseille", "Paris"],
                "distance": 1247.53,
                "visibility": "public"
            }
        ]
    }
]
```

---

## Tests

Tests are located in the `tests/` folder and use pytest with mocking.

### Run all tests
```bash
pytest tests/
```

### Run a specific test file
```bash
pytest tests/loginTest.py
```

### Run with details
```bash
pytest tests/ -v
```

Tests cover: login, account creation, add/delete cities, tour generation, and tour display.