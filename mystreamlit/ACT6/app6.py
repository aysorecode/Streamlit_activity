import cv2
import streamlit as st
import numpy as np
from PIL import Image
import time

st.title("🎥 OpenCV + Streamlit: Real-Time Video Processing")

# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.header("⚙️ Filter Controls")
selected_filter = st.sidebar.selectbox("Select Filter", ["None", "Grayscale", "Canny Edge", "Face Detection"])

if selected_filter == "Canny Edge":
    threshold1 = st.sidebar.slider("Threshold 1", 0, 255, 100)
    threshold2 = st.sidebar.slider("Threshold 2", 0, 255, 200)

# -------------------------------
# Load Face Detection Model
# -------------------------------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# -------------------------------
# Video Capture
# -------------------------------
capture = cv2.VideoCapture(0)

frame_placeholder = st.empty()
snapshot_btn = st.button("📸 Take Snapshot")

snapshot_img = None

while True:
    ret, frame = capture.read()
    if not ret:
        st.error("Unable to access webcam.")
        break

    frame = cv2.flip(frame, 1)  # Mirror the image

    # Apply selected filter
    if selected_filter == "Grayscale":
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

    elif selected_filter == "Canny Edge":
        frame = cv2.Canny(frame, threshold1, threshold2)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

    elif selected_filter == "Face Detection":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display frame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(frame_rgb, channels="RGB")

    # Snapshot logic
    if snapshot_btn:
        snapshot_img = frame_rgb.copy()
        break

    # Small delay to avoid high CPU usage
    time.sleep(0.03)

capture.release()

# -------------------------------
# Display Snapshot
# -------------------------------
if snapshot_img is not None:
    st.success("✅ Snapshot captured!")
    st.image(snapshot_img, caption="📸 Snapshot", use_column_width=True)