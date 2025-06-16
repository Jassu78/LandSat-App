# Landsat Fly at Your Fingertips

This Streamlit application lets you effortlessly access and visualize **Landsat satellite data**. Compare ground-based observations with high-resolution imagery, track changes over time, and even get notified about Landsat revisits.

---

## Features

* **Flexible Location Input:** Specify your area of interest by:
    * Entering **coordinates** (latitude, longitude).
    * Typing a **location name**.
    * **Clicking directly on a map**.
    * **Auto-fetching your current location**.
* **Landsat Data Retrieval:** Get the latest available Landsat overpass data for your chosen spot.
* **Image Visualization:** View the high-resolution Landsat image.
* **Interactive Map:** See your selected location clearly marked on a dynamic map.
* **Time-Series Animation:** Generate an animation of Landsat images over a specified date range to observe changes.
* **Data Download:** Download the retrieved Landsat data in **JSON** or **CSV** formats.
* **Email Notifications:** Receive email updates with Landsat data and optional animation attachments. You can also easily add a reminder to your Google Calendar for the next Landsat revisit.

---

## How to Use

1.  **Run the App:**
    If you have Python and Streamlit installed, navigate to the directory containing your script (e.g., `app.py`) and run:
    ```bash
    streamlit run app.py
    ```
2.  **Getting Started:** The app will first display a "Getting Started" page explaining its features. Click "Get Started" to proceed.
3.  **Choose Input Method:** Select how you want to specify the location.
4.  **Get Landsat Data:** Once a location is set, click "Get Landsat Overpass Data" to retrieve the latest image and details.
5.  **Explore Visualizations:** View the image and interactive map.
6.  **Generate Animation:** Select a start and end date, then click "Generate Animation" to see a time-lapse.
7.  **Download & Share:** Use the download buttons for data or the email notification option to share information.

---

## Technical Details

This application is built using:

* **Streamlit:** For the interactive web interface.
* **Requests:** To interact with the NASA Earthdata API.
* **Folium & Streamlit-Folium:** For interactive map visualizations.
* **Geopy & Geocoder:** For converting location names to coordinates and auto-fetching user location.
* **PIL (Pillow):** For image processing.
* **Matplotlib & Matplotlib.animation:** For generating time-series animations.
* **smtplib & email:** For sending email notifications.

---

## API Key

The application uses `DEMO_KEY` for the NASA Earthdata API. For production use or higher rate limits, you should obtain your own API key from [NASA Earthdata](https://urs.earthdata.nasa.gov/).

---

## Disclaimer

The "Landsat Revisit Time" in the email notification is an example for demonstration purposes. Actual Landsat revisit times vary based on the specific satellite and location. The Google Calendar reminder link is a client-side link and assumes the user is logged into their Google account.

---
