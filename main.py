import os
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pytesseract
from flask import Flask, render_template

# Directory paths
dataset_dir = 'data/cars_data'
timestamps_path = os.path.join(dataset_dir, 'timestamps.txt')
yolov3_weights = 'yolo/lapi.weights'
yolov3_cfg = 'yolo/darknet-yolov3.cfg'
coco_names = 'yolo/classes.names'

# Load timestamps
timestamps = pd.read_csv(timestamps_path, header=None, names=['filename', 'timestamp'])

# Preprocess image
def preprocess_image(image, target_size=(416, 416)):
    image_resized = cv2.resize(image, target_size)
    image_gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
    return image_gray

# Display sample images
def load_and_display_samples(dataset_dir, timestamps, num_samples=3):
    for index, row in timestamps.iterrows():
        if index >= num_samples:
            break
        image_path = os.path.join(dataset_dir, row['filename'])
        image = cv2.imread(image_path)
        if image is not None:
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.title(f"Timestamp: {row['timestamp']}")
            plt.axis('off')
            plt.show()
        else:
            print(f"Failed to load image at {image_path}")

# Display preprocessed images
def display_preprocessed_samples(dataset_dir, timestamps, num_samples=3):
    for index, row in timestamps.iterrows():
        if index >= num_samples:
            break
        image_path = os.path.join(dataset_dir, row['filename'])
        image = cv2.imread(image_path)
        if image is not None:
            preprocessed_image = preprocess_image(image)
            plt.imshow(preprocessed_image, cmap='gray')
            plt.title(f"Timestamp: {row['timestamp']}")
            plt.axis('off')
            plt.show()
            plt.savefig('/results')
        else:
            print(f"Failed to load image at {image_path}")

# Plot vehicle entry/exit times
def plot_vehicle_entry_exit_times(timestamps):
    plt.figure(figsize=(12, 6))
    sns.histplot(timestamps['timestamp'], bins=24, kde=True)
    plt.title('Vehicle Entry/Exit Times')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()

# Recognize license plate using Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def recognize_license_plate(image):
    plate_text = pytesseract.image_to_string(image, config='--psm 8')
    plate_text = ''.join(filter(str.isalnum, plate_text)).upper()
    return plate_text

# Match vehicles to approved database
approved_vehicles = {'ABC123', 'XYZ789', 'LMN456'}

def match_vehicles(dataset_dir, timestamps, approved_vehicles):
    matches = []
    for index, row in timestamps.iterrows():
        image_path = os.path.join(dataset_dir, row['filename'])
        image = cv2.imread(image_path)
        if image is not None:
            preprocessed_image = preprocess_image(image)
            plate_text = recognize_license_plate(preprocessed_image)
            if plate_text in approved_vehicles:
                matches.append((row['filename'], row['timestamp'], plate_text))
    return matches

# Generate insights
def generate_insights(timestamps):
    movement_patterns = timestamps['timestamp'].dt.hour.value_counts().sort_index()
    plt.figure(figsize=(12, 6))
    movement_patterns.plot(kind='bar')
    plt.title('Vehicle Movement Patterns by Hour')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Vehicles')
    plt.show()
    
    parking_occupancy = {'Lot A': 50, 'Lot B': 30, 'Lot C': 20}
    plt.figure(figsize=(8, 6))
    plt.bar(parking_occupancy.keys(), parking_occupancy.values())
    plt.title('Parking Occupancy')
    plt.xlabel('Parking Lot')
    plt.ylabel('Number of Vehicles')
    plt.show()

# Flask application
app = Flask(__name__)

@app.route('/')
def home():
    matches = match_vehicles(dataset_dir, timestamps, approved_vehicles)
    return render_template('index.html', insights=matches)

if __name__ == '__main__':
    # Load and display sample images
    load_and_display_samples(dataset_dir, timestamps)
    # Display preprocessed sample images
    display_preprocessed_samples(dataset_dir, timestamps)
    # Plot vehicle entry/exit times
    plot_vehicle_entry_exit_times(timestamps)
    # Generate insights
    generate_insights(timestamps)
    # Run Flask app
    app.run(debug=True)
