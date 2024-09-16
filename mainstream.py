import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
from maingemini import analyze_image

# Title
st.title("AI Canvas Maths Calculator ")

# Sidebar settings
st.sidebar.header("Canvas Configuration")

# Configuration options
stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ", "#000000")
bg_color = st.sidebar.color_picker("Background color hex: ", "#FFFFFF")
drawing_mode = st.sidebar.selectbox(
    "Drawing mode:", ("freedraw", "line", "rect", "circle", "transform", "eraser")
)
realtime_update = st.sidebar.checkbox("Update in real-time", True)

# Set stroke color to background color when eraser is selected
if drawing_mode == "eraser":
    stroke_color = bg_color  # Eraser uses the background color to "erase"

# Undo functionality (clear canvas)

# Session state to manage the canvas clearing
if "canvas_key" not in st.session_state:
    st.session_state.canvas_key = 0  # Initialize canvas key to track resets

# Button to clear the canvas
if st.button("Clear Canvas"):
    st.session_state.canvas_key += 1  # Increment the key to clear canvas
# Excalidraw-like canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fill color for shapes
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=500,
    width=800,
    drawing_mode=drawing_mode if drawing_mode != "eraser" else "freedraw",
    update_streamlit=realtime_update,
    key=f"canvas_{st.session_state.canvas_key}",
)

# Function to delete a LaTeX expression from the list
def delete_latex(latex_item):
    st.session_state.latex_list.remove(latex_item)


if st.button("Run"):
     if canvas_result.image_data is not None:
# Convert canvas image data to a PIL image
        image_data = canvas_result. image_data.astype(np.uint8) #
        img = Image.fromarray (image_data) # Create an image from
        
        latex_input=analyze_image(img)
        """latex_input=r'''
            a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
            \sum_{k=0}^{n-1} ar^k =
            a \left(\frac{1-r^{n}}{1-r}\right)
            ''' """
        # Initialize list in session_state if not already initialized
        if "latex_list" not in st.session_state:
            st.session_state.latex_list = []
        # Display the LaTeX list
        st.write("Your LaTeX List:")
        if latex_input not in st.session_state.latex_list:
           st.session_state.latex_list.append(latex_input)
        for latex_item in st.session_state.latex_list:
            # Render the LaTeX expression
            st.latex(latex_item)
            
            # Button to delete the corresponding LaTeX item
            st.button(f"Delete", key=f"delete_{latex_item}", on_click=delete_latex, args=(latex_item,)) 

# Option to clear the entire list
if st.button("Clear All LaTeX Expressions"):
    st.session_state.latex_list = []

# Instructions
st.write("""
### Instructions:
1. Use **Free Draw** to create hand-drawn sketches.
2. Use **Line, Rect, Circle** tools to create more precise shapes.
3. Use **Eraser** mode to remove parts of your drawing.
4. **Clear Canvas** resets everything, and you can start over.
5. Optionally, enable **real-time updates** for smooth interaction.
""")













