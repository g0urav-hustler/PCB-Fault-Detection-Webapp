import streamlit as st
from ultralytics import YOLO
from PIL import Image

model_path = "model/best.pt"
st.set_page_config(page_title="PCB Fault Detection ", layout="wide",)

#title
st.title("PCB Fault Detection")

#subtitle
st.markdown("This application helps you to detect the faults in printed circuit boards. ")

@st.cache_resource(show_spinner="Loading the app..")
def load_model(model_name):
    model = YOLO(model_name)
    return model

model = load_model(model_path)
image_shape = [640,640]
  
#image uploader
image = st.file_uploader(label = "Upload your image here", type=['png','jpg','jpeg'])

if image is not None:
    img = Image.open(image)
    
    with st.spinner("Detecting the faults"):
        img = img.resize(image_shape)
        result = model.predict(img, conf = 0.5, show_conf = False )
        plot_img = result[0].plot()
        result_img = Image.fromarray(plot_img)

    boxes = result[0].boxes.shape[0]
    
    if boxes:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(img)

        with col2:
            st.subheader("Detected Faults")
            st.image(result_img)
    else:
        st.image(img)
        st.subheader("The PCB has no fault.")
else:
    st.write("Upload an Image first")

st.divider() 

st.caption("Made by Gourav Chouhan ")


  