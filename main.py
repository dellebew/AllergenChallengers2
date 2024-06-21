import easyocr # package to read data
import cv2 # package to load img object for overlaying
import matplotlib.pyplot as plt # package to plot data back to menu
from callgpt import process_in_gpt
from menufunctions import ReadObj, read_menu, draw_on_menu, process_msg, opt_process_msg
# Connect to streamlit
import streamlit as st
import numpy as np

# to create one with real time updated footage: https://thiagoalves.ai/building-webcam-streaming-applications-with-streamlit-and-opencv/


# imagename = 'image_13.png'
img_file_buffer = st.camera_input("Take a picture")
if img_file_buffer is not None:

    bytes_data = img_file_buffer.getvalue()
    image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    img_file_buffer = None

    menudata = read_menu(image)
    gptmsg = process_in_gpt(menudata)
    menudata = opt_process_msg(gptmsg, menudata)

    # draw on img and print
    for key in menudata:
        image = draw_on_menu(image, menudata[key])
    
    # Check the shape of cv2_img:
    # Should output shape: (height, width, channels)
    st.image(image)
