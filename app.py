import streamlit as st
import requests
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import geocoder
from PIL import Image
import io
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tempfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Function to get Landsat overpass data from NASA Earthdata API
def get_landsat_overpass(lat, lon, date):
    url = f"https://api.nasa.gov/planetary/earth/assets?lon={lon}&lat={lat}&date={date}&dim=0.1&api_key=DEMO_KEY"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

# Function to create placeholder images for animation
def create_placeholder_images(start_date, end_date, lat, lon):
    date_range = pd.date_range(start=start_date, end=end_date, freq='30D')
    images = []
    for date in date_range:
        data = get_landsat_overpass(lat, lon, date.strftime('%Y-%m-%d'))
        if data and 'url' in data:
            image_url = data['url']
            image = Image.open(io.BytesIO(requests.get(image_url).content))
            images.append(image)
    return images, date_range

# Function to get coordinates from location name
def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(location_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# Function to send an email
def send_email(subject, body, to_email, attachment_path=None):
    from_email = 'jaswanthjogi7815@gmail.com'  # Replace with your email
    password = 'uiwzwztkowxcnncu'  # Replace with your email password
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))  # Use HTML for better formatting

    if attachment_path:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={attachment_path.split("/")[-1]}')
            msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use your SMTP server
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        st.write("Email sent successfully!")
    except Exception as e:
        st.write(f"Failed to send email. Error: {e}")

# Function to create Google Calendar reminder (placeholder)
def create_calendar_event(summary, description, start_time, end_time):
    # This function should be implemented to create events in Google Calendar
    st.write(f"Reminder created: {summary} from {start_time} to {end_time}")
    # Integration code with Google Calendar API would go here

# Initialize session state
if 'data' not in st.session_state:
    st.session_state['data'] = None
if 'lat' not in st.session_state:
    st.session_state['lat'] = None
if 'lon' not in st.session_state:
    st.session_state['lon'] = None
if 'image_url' not in st.session_state:
    st.session_state['image_url'] = None
if 'animation_path' not in st.session_state:
    st.session_state['animation_path'] = None

# Getting Started Page
if 'show_getting_started' not in st.session_state:
    st.session_state['show_getting_started'] = True

if st.session_state['show_getting_started']:
    st.title("Getting Started with Landsat Reflectance Data App")
    st.write(
        """
        **Welcome to the Landsat Reflectance Data App!**

        **What is Landsat?**
        Landsat is a series of Earth-observing satellites that provide high-resolution images of our planet's surface. These images are used for various applications, including land use planning, environmental monitoring, and natural disaster assessment.

        **About This Application:**
        - **Input Location**: Choose your location by entering coordinates, typing a location name, clicking on a map, or auto-fetching your current location.
        - **Retrieve Landsat Data**: Access high-resolution satellite images for the specified location.
        - **Visualize Data**: View the location on an interactive map.
        - **Generate Time-Series Animation**: Create an animation of Landsat images over a specified date range.
        - **Download Data**: Save the data in JSON or CSV format.
        - **Send Email Notifications**: Send an email with the Landsat data and optional animation attachment.

        **Click "Get Started" to begin using the app and explore its features.**
        """
    )
    if st.button("Get Started"):
        st.session_state['show_getting_started'] = False
else:
    st.title("Landsat Reflectance Data: On the Fly and at Your Fingertips")
    st.write("Compare ground-based observations with Landsat data.")

    # Input method selection
    st.subheader("Select Input Method")
    input_method = st.radio("Choose how to input the location:", 
                            ("Enter Coordinates", "Type Location Name", "Point on Map", "Auto Fetch User Location"))

    if input_method == "Enter Coordinates":
        coord = st.text_input("Enter Coordinates (latitude,longitude)", "40.7128,-74.0060")
        if st.button("Set Coordinates"):
            try:
                lat, lon = map(float, coord.split(','))
                st.session_state['lat'] = lat
                st.session_state['lon'] = lon
            except ValueError:
                st.write("Please enter valid coordinates in the format latitude,longitude.")
    elif input_method == "Type Location Name":
        location_name = st.text_input("Location Name", "New York")
        if st.button("Get Coordinates"):
            lat, lon = get_coordinates(location_name)
            if lat and lon:
                st.session_state['lat'] = lat
                st.session_state['lon'] = lon
                st.write(f"Coordinates for {location_name}: Latitude = {lat}, Longitude = {lon}")
            else:
                st.write("Location not found. Please enter a valid location name.")
    elif input_method == "Point on Map":
        st.write("Click on the map to select a location.")
        map_center = [20.5937, 78.9629]  # Center of India
        m = folium.Map(location=map_center, zoom_start=5)
        
        # Add a marker that will be updated when the user clicks on the map
        marker = folium.Marker(location=map_center, icon=folium.Icon(color='red', icon='info-sign'))
        marker.add_to(m)
        
        # Update map visualization
        map_data = st_folium(m, width=700, height=500)
        
        # Check if coordinates are provided through the map
        if map_data and map_data.get('last_clicked'):
            lat, lon = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
            st.session_state['lat'] = lat
            st.session_state['lon'] = lon
            marker.location = [lat, lon]
            st.write(f"Selected Coordinates: Latitude = {lat}, Longitude = {lon}")
    elif input_method == "Auto Fetch User Location":
        g = geocoder.ip('me')
        if g.ok:
            lat, lon = g.latlng
            st.session_state['lat'] = lat
            st.session_state['lon'] = lon
            st.write(f"Auto-Fetched Coordinates: Latitude = {lat}, Longitude = {lon}")
        else:
            st.write("Unable to fetch user location. Please try another method.")

    if st.session_state['lat'] and st.session_state['lon']:
        if st.button("Get Landsat Overpass Data"):
            data = get_landsat_overpass(st.session_state['lat'], st.session_state['lon'], datetime.now().strftime('%Y-%m-%d'))
            if data:
                st.session_state['data'] = data
                st.session_state['image_url'] = data.get('url', None)
                st.write("Landsat data retrieved successfully!")
            else:
                st.write("No data available for the given location.")

    if st.session_state['data']:
        st.write("Landsat Overpass Data:")
        st.json(st.session_state['data'])

        if st.session_state['image_url']:
            st.image(st.session_state['image_url'], caption="High-Resolution Landsat Image")

        # Visualization
        st.subheader("Map Visualization")
        map_center = [st.session_state['lat'], st.session_state['lon']]
        m = folium.Map(location=map_center, zoom_start=10)
        folium.Marker(location=map_center, popup="Target Location", icon=folium.Icon(color='blue')).add_to(m)
        st_folium(m, width=700, height=500)

        # Data Download
        st.subheader("Download Data")
        file_format = st.selectbox("Select file format", ["JSON", "CSV"])
        if file_format == "JSON":
            st.download_button("Download Landsat Data (JSON)", data=str(st.session_state['data']), file_name="landsat_data.json")
        elif file_format == "CSV":
            import pandas as pd
            df = pd.DataFrame([st.session_state['data']])
            csv = df.to_csv(index=False)
            st.download_button("Download Landsat Data (CSV)", data=csv, file_name="landsat_data.csv")

    # Time-Series Animation
    st.subheader("Time-Series Animation of Landsat Data")

    start_date = st.date_input("Start Date", datetime(2023, 1, 1))
    end_date = st.date_input("End Date", datetime(2023, 12, 31))

    if st.button("Generate Animation"):
        if st.session_state['lat'] and st.session_state['lon']:
            images, date_range = create_placeholder_images(start_date, end_date, st.session_state['lat'], st.session_state['lon'])
            if images:
                st.write("Displaying time-lapse animation of Landsat images.")
                
                # Create animation
                fig, ax = plt.subplots()
                def update(frame):
                    ax.clear()
                    ax.imshow(images[frame])
                    ax.set_title(f"Date: {date_range[frame].strftime('%Y-%m-%d')}")
                    
                ani = animation.FuncAnimation(fig, update, frames=len(images), repeat=False)
                
                # Save animation to a temporary file
                with tempfile.NamedTemporaryFile(suffix='.gif', delete=False) as tmpfile:
                    animation_path = tmpfile.name
                    ani.save(animation_path, writer='pillow')
                    tmpfile.seek(0)
                    # Display animation
                    st.image(animation_path)
                    st.session_state['animation_path'] = animation_path
            else:
                st.write("No images available for the specified date range.")
        else:
            st.write("Please select a location first.")

    # Email Notification
    st.subheader("Email Notification")
    email_notification_option = st.checkbox("Send Email Notification")

    if email_notification_option:
        with st.form("email_form"):
            recipient_email = st.text_input("Recipient Email")
            submit_button = st.form_submit_button("Send Email")
            if submit_button:
                if recipient_email:
                    subject = "Landsat Data Notification"
                    now = datetime.now()
                    revisit_time = now + timedelta(days=16)  # Example revisit time for demonstration
                    body = (f"<html><body>"
                            f"<h2>Hello,</h2>"
                            f"<p>We are pleased to provide you with the Landsat data for the location you selected.</p>"
                            f"<p><strong>Location:</strong> Latitude: {st.session_state['lat']}, Longitude: {st.session_state['lon']}</p>"
                            f"<p><strong>Data:</strong> {st.session_state['data']}</p>"
                            f"<p><strong>Landsat Revisit Time:</strong> {revisit_time.strftime('%Y-%m-%d %H:%M:%S')}</p>"
                            f"<p><strong>Link to access the data:</strong> <a href='https://api.nasa.gov/planetary/earth/assets?lon={st.session_state['lon']}&lat={st.session_state['lat']}&date={now.strftime('%Y-%m-%d')}&dim=0.1&api_key=DEMO_KEY'>Access Data</a></p>"
                            f"<p><strong>Set a Reminder:</strong> <a href='https://calendar.google.com/calendar/r/eventedit?text=Landsat%20Revisit&dates={now.strftime('%Y%m%dT%H%M%S')}/{revisit_time.strftime('%Y%m%dT%H%M%S')}&details=Reminder%20for%20Landsat%20revisit%20at%20Latitude%20{st.session_state['lat']},%20Longitude%20{st.session_state['lon']}'>Add to Calendar</a></p>"
                            f"<p>Best regards,<br>Your Landsat Data Team</p>"
                            f"</body></html>")

                    # Optionally include animation as attachment
                    attachment_path = st.session_state['animation_path'] if st.session_state['animation_path'] else None

                    send_email(subject, body, recipient_email, attachment_path)
                else:
                    st.write("Please enter a recipient email address.")
