import tkinter as tk
from tkinter import ttk, messagebox
import random
import geopy.distance
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageTk

class EToilet:
    def __init__(self, location):
        self.location = location
        self.engaged = False

    def check_availability(self):
        if self.engaged:
            return "Engaged"
        else:
            return "Available"

    def scan_qr_code(self, qr_code):
        if qr_code == "1234":
            self.engaged = True
            return "QR code scanned successfully. Toilet engaged."
        else:
            return "Invalid QR code."

    def reserve_toilet(self):
        if self.engaged:
            return "Toilet is already engaged."
        else:
            self.engaged = True
            return "Toilet reserved successfully."

def check_availability_command():
    availability_label.config(text=etoilet.check_availability())

def scan_qr_code_command():
    def scan_qr_code_video():
        capture = cv2.VideoCapture(0)
        qr_code_scanned = False

        while not qr_code_scanned:
            ret, frame = capture.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture video.")
                break

            # Convert frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert frame to ImageTk format
            img = Image.fromarray(rgb_frame)
            img_tk = ImageTk.PhotoImage(image=img)

            # Display image in tkinter window
            video_label.config(image=img_tk)
            video_label.image = img_tk

            # Use OpenCV QR code detector
            qr_code_detector = cv2.QRCodeDetector()
            qr_code_info, points, _ = qr_code_detector.detectAndDecode(frame)

            if qr_code_info:
                qr_code_scanned = True
                result = etoilet.scan_qr_code(qr_code_info)
                messagebox.showinfo("QR Code Scan Result", result)
                availability_label.config(text=etoilet.check_availability())

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()

    scan_qr_code_video()

def reserve_toilet_command():
    # For demonstration purposes, generate random user location within the vicinity of the toilets
    user_location = (
        random.uniform(12.95, 12.97),  # Random latitude within the range
        random.uniform(77.58, 77.61)    # Random longitude within the range
    )

    toilet_location = (locations_data[etoilet.location]['latitude'], locations_data[etoilet.location]['longitude'])
    distance = geopy.distance.geodesic(user_location, toilet_location).kilometers

    # Introduce a probability threshold for allowing reservation
    reservation_probability = 0.7  # Adjust this probability as needed

    if distance <= 1 or random.random() < reservation_probability:
        result = etoilet.reserve_toilet()
        messagebox.showinfo("Reservation Result", result)
    else:
        messagebox.showwarning("Reservation Unavailable", "Toilet reservation is only available when you are within 1km of the toilet, or sometimes based on a probability.")

    availability_label.config(text=etoilet.check_availability())

def show_map():
    # Generate random location
    location = random.choice(locations)
    etoilet.location = location
    availability_label.config(text="Location: {}\nAvailability: {}".format(etoilet.location, etoilet.check_availability()))

    # Plot a simple map with all available locations
    plt.figure(figsize=(8, 6))
    for loc, status in available_locations.items():
        if status == 'Available':
            plt.scatter(locations_data[loc]['longitude'], locations_data[loc]['latitude'], marker='o', color='blue', label='Available')
        else:
            plt.scatter(locations_data[loc]['longitude'], locations_data[loc]['latitude'], marker='x', color='red', label='Engaged')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('E-Toilet Locations')
    plt.legend()
    plt.grid(True)
    plt.show()

def show_available_near_you():
    table_window = tk.Toplevel(root)
    table_window.title("Available Near You")

    table = ttk.Treeview(table_window, columns=('Location', 'Availability'), show='headings')
    table.heading('Location', text='Location')
    table.heading('Availability', text='Availability')
    table.pack()

    for loc, status in available_locations.items():
        table.insert('', 'end', values=(loc, status))

# List of Indian street names
locations = [
    "MG Road",
    "Brigade Road",
    "Jayanagar 4th Block",
    "Indiranagar 100 Feet Road",
    "Koramangala Inner Ring Road",
    "Commercial Street",
    "Lalbagh Main Road",
    "Basavanagudi Bull Temple Road",
    "Cunningham Road",
    "Malleshwaram Margosa Road"
]

# Sample latitude and longitude data for demonstration
locations_data = {
    "MG Road": {"latitude": 12.9716, "longitude": 77.5946},
    "Brigade Road": {"latitude": 12.9707,    "longitude": 77.6070},
    "Jayanagar 4th Block": {"latitude": 12.9294, "longitude": 77.5832},
    "Indiranagar 100 Feet Road": {"latitude": 12.9784, "longitude": 77.6408},
    "Koramangala Inner Ring Road": {"latitude": 12.9279, "longitude": 77.6271},
    "Commercial Street": {"latitude": 12.9822, "longitude": 77.6081},
    "Lalbagh Main Road": {"latitude": 12.9507, "longitude": 77.5848},
    "Basavanagudi Bull Temple Road": {"latitude": 12.9469, "longitude": 77.5743},
    "Cunningham Road": {"latitude": 12.9868, "longitude": 77.5992},
    "Malleshwaram Margosa Road": {"latitude": 13.0028, "longitude": 77.5692}
}

# Randomly set initial availability for locations
available_locations = {location: random.choice(["Available", "Engaged"]) for location in locations}

# Create an instance of EToilet
etoilet = EToilet(random.choice(locations))

def set_background_image(image_path):
    try:
        background_image = tk.PhotoImage(file=image_path)
        background_label = tk.Label(root, image=background_image)
        background_label.place(relwidth=1, relheight=1)
        background_label.image = background_image
    except tk.TclError:
        print("Background image not found or cannot be loaded.")

# Create main window
root = tk.Tk()
root.title("E-Toilet System")
root.geometry("800x600")

# Set background image
set_background_image("image2.png")

# Create a custom style for the buttons
style =ttk.Style()
style.configure('Custom.TButton', foreground="black", background="lightcoral", bordercolor="black", borderwidth=2)

# Create and place widgets
title_label = tk.Label(root, text="E-Toilet System", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

availability_label = tk.Label(root, text="Location: {}\nAvailability: {}".format(etoilet.location, etoilet.check_availability()))
availability_label.pack()

check_availability_button = ttk.Button(root, text="Check Availability", command=check_availability_command, style='Custom.TButton')
check_availability_button.pack(pady=5)

scan_qr_code_button = ttk.Button(root, text="Scan QR Code", command=scan_qr_code_command, style='Custom.TButton')
scan_qr_code_button.pack(pady=5)

reserve_toilet_button = ttk.Button(root, text="Reserve Toilet", command=reserve_toilet_command, style='Custom.TButton')
reserve_toilet_button.pack(pady=5)

show_map_button = ttk.Button(root, text="Show Map", command=show_map, style='Custom.TButton')
show_map_button.pack(pady=5)

show_available_button = ttk.Button(root, text="Available Near You", command=show_available_near_you, style='Custom.TButton')
show_available_button.pack(pady=5)

video_label = tk.Label(root)
video_label.pack()

root.mainloop()

