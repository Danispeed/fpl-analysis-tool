# FPL Analysis Tool

A simple tool that fetches and processes Fantasy Premier League (FPL) data to help you make better decisions. It calculates and displays player ratings to guide who to keep, sell, or buy. It also shows a "Dream Eleven" lineup based on the highest-rated players across all positions.

## Features
- Fetches real-time data from the official FPL API.
- Calculates positional player ratings (goalkeepers, defenders, midfielders, and forwards).
- Provides a "Dream Eleven" view showcasing top-rated players in each position.
- Displays sorted tables of players and their ratings for easier selection.

## Getting Started

### Set Up a Virtual Environment
```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Run the Backend
python program.py # This starts a Flask server at http://127.0.0.1:5000 serving player ratings through JSON endpoints.

# Run the Frontend
# In the React project directory:
npm install
npm start # This launches the frontend at http://127.0.0.1:3000.

## Additional Dependencies

The frontend uses `react-slick` to implement a carousel/slider component. Before running the frontend, make sure to install:

# In the frontend directory:
npm install react-slick slick-carousel

```

# Usage
- Navigate to http://127.0.0.1:3000 in your browser.
- View the Dream Eleven lineup and inspect sorted tables of goalkeepers, defenders, midfielders, and forwards.
- Use the information to help guide your FPL transfer decisions.

# ChatGPT
This README file was genereated by ChatGPT.