# AI Based Ornament Recommendation System

## Overview
A simple Flask-based chatbot-like web app that recommends ornament designs based on user inputs (type, metal, style, weight) and generates a price quotation with PDF download.

## Installation (for local development)
1. Clone or unzip the project.
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Open http://127.0.0.1:5000 in your browser.

## Project Structure
- `app.py` - Flask application
- `templates/` - HTML templates
- `static/` - CSS and images
- `data/ornaments.json` - sample ornaments dataset
- `output/` - generated quotation.json and PDFs

## Notes
- The pricing logic uses placeholder base prices. Integrate a real metal rates API for live pricing.
- For production, replace file-based storage with a proper database.
