import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Page Config
st.set_page_config(page_title="🖼️ Image Lab", layout="wide", page_icon="🎨")

# Custom CSS for modern look
st.markdown("""
<style>
body {
    background-color: #f5f5f5;
    font-family: 'Segoe UI', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #1f1f1f, #333333);
    color: white;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
}
img {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🖼️ Image Processing Lab")
st.markdown("Upload your image and apply various transformations in real-time.")

# Sidebar Upload
with st.sidebar:
    st.header("📤 Upload")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

# Main Display
if uploaded_file:
    image = np.array(Image.open(uploaded_file))
    st.sidebar.header("⚙️ Transformations")

    # Rotation
    rotate_angle = st.sidebar.slider("Rotate (Degrees)", -180, 180, 0)
    if rotate_angle != 0:
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, rotate_angle, 1.0)
        image = cv2.warpAffine(image, M, (w, h))

    # Flip
    flip_mode = st.sidebar.radio("Flip Image", ["None", "Horizontal", "Vertical"])
    if flip_mode == "Horizontal":
        image = cv2.flip(image, 1)
    elif flip_mode == "Vertical":
        image = cv2.flip(image, 0)

    # Grayscale
    apply_gray = st.sidebar.checkbox("Convert to Grayscale")
    display_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if apply_gray:
        display_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Filters
    st.sidebar.header("🎨 Filters")
    filter_type = st.sidebar.radio("Select Filter", ["None", "Gaussian Blur", "Median Blur", "Unsharp Mask"])
    kernel_size = st.sidebar.slider("Kernel Size", 3, 25, 9, 2)

    if filter_type == "Gaussian Blur":
        sigma = st.sidebar.slider("Sigma", 0.1, 5.0, 1.5)
        display_image = cv2.GaussianBlur(display_image, (kernel_size, kernel_size), sigma)
    elif filter_type == "Median Blur":
        display_image = cv2.medianBlur(display_image, kernel_size)
    elif filter_type == "Unsharp Mask":
        blur = cv2.GaussianBlur(display_image, (0, 0), 3)
        display_image = cv2.addWeighted(display_image, 1.5, blur, -0.5, 0)

    # Layout
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🖼️ Original Image")
        st.image(np.array(Image.open(uploaded_file)), use_column_width=True)
    with col2:
        st.markdown("### 🎯 Processed Image")
        st.image(display_image, use_column_width=True, clamp=True)


else:
    st.markdown("""
    <div style="text-align: center; padding: 100px 20px;">
        <h2 style="color: #777;">📁 Drag & Drop an Image to Begin</h2>
        <p style="color: #555;">Supported formats: JPG, PNG, JPEG</p>
    </div>
    """, unsafe_allow_html=True)
