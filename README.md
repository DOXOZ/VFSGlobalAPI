# VFS Global Appointment Scraper

This project automates the process of checking available appointment dates on the [VFS Global](https://visa.vfsglobal.com/arg/en/dnk/book-appointment)
website for visa appointments using Python. The tool navigates the VFS site, performs a login, fills out a booking form, and collects available appointment dates
displayed on the calendar. It then provides the scraped data through a Flask-based API endpoint.

## Features
- **Automated Appointment Search**: Logs in and navigates the VFS site to locate available appointment dates.
- **Calendar Scraping**: Collects available appointment slots over several months and displays the dates.
- **REST API Endpoint**: The Flask app provides an endpoint (`/scrape`) that returns available dates in JSON format.
- **Cloudflare Handling**: Waits for Cloudflare’s challenge if detected.

## Prerequisites
- Python 3.8 or higher
- Required Python packages in `requirements.txt`:
  - `DrissionPage` for browser automation
  - `beautifulsoup4` for HTML parsing
  - `Flask` for serving the API

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/DOXOZ/VFSGlobalAPI.git
   cd VFSGlobalAPI
   ```

2. **Install Dependencies**
   Install the necessary packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up DrissionPage**
   Make sure you have a Chromium-based browser installed for DrissionPage to function properly.

4. **Environment Variables (Optional)**
   For security, it’s recommended to store sensitive data (like email, password) in environment variables or a secure storage instead of hardcoding.

## Usage

1. **Run the Flask App**
   Start the application by running:
   ```bash
   python <script_name>.py
   ```
   Replace `<script_name>.py` with the actual script name.

2. **Access the Endpoint**
   Access the scraping functionality by sending a GET request to the `/scrape` endpoint:
   ```bash
   http://127.0.0.1:5000/scrape
   ```

3. **Response**
   The endpoint returns available appointment dates in JSON format, with each month as a key and available days as values.

   Example response:
   ```json
   {
     "November 2024": ["5", "12", "19"],
     "December 2024": ["3", "10", "17"]
   }
   ```

## Code Walkthrough
1. **`scrape` Function**:
   - Initializes a Chromium browser session, navigates to the VFS site, and logs in.
   - Fills out the booking form, selects appointment category and sub-category, and proceeds to the calendar page.
   - Scrapes available appointment dates over multiple months and returns the results.

2. **`scrape_endpoint`**:
   - Defines a Flask route (`/scrape`) to serve the scrape data as a JSON response.

## Security Notice
This script contains login credentials directly in the code, which is not secure for production use. Consider using environment variables or a secure credential storage mechanism.

