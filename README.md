# Vehicle Movement and Parking Management System using Edge AI

This project aims to manage vehicle movement and parking within a college campus using Edge AI. The system analyzes vehicle movement patterns, monitors parking occupancy, and matches vehicles to an approved database using real-time image data from cameras.

## Features

- **Image Preprocessing:** Resize and convert images to grayscale for better processing.
- **Sample Image Display:** Display original and preprocessed images with timestamps.
- **Vehicle Entry/Exit Time Plot:** Visualize the frequency of vehicle movements throughout the day.
- **License Plate Recognition:** Recognize license plates using Tesseract OCR.
- **Vehicle Matching:** Match recognized license plates to an approved database.
- **Insights Generation:** Generate visual insights on vehicle movement patterns and parking occupancy.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/vehicle-movement-parking-management.git
   cd vehicle-movement-parking-management
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download YOLOv3 files:**
   - [YOLOv3 Weights](https://drive.google.com/file/d/1Gx-2tRsxWQ6nf6i1TcB5HytRk1-QERf_/view?usp=drive_link)
   - Place the `lapi.weights`, `darknet-yolov3.cfg`, and `classes.names` files in the project root directory.

## Usage

1. **Load and display sample images:**
   ```python
   python main.py 
   ```

## File Structure

- `cars_data/`: Directory containing the images and `timestamps.txt`.
- `main.py`: Main script to run different functionalities.
- `requirements.txt`: List of Python dependencies.

## Acknowledgements

- YOLOv3 for object detection.
- Tesseract OCR for license plate recognition.
- OpenCV and Matplotlib for image processing and visualization.
- Flask for web application framework.

---

Feel free to modify the content as per your project specifics and add any additional details you deem necessary.
