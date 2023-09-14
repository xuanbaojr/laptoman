import io
import time

import streamlit as st
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image


@st.cache_resource
def load_model(model_id="CompVis/stable-diffusion-v1-4"):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe.enable_attention_slicing()
    return pipe.to(device)


def upload_audio():
    st.header("Input audio")
    uploaded_file = st.file_uploader(
        "Choose audio file", type=[".wav", ".mp3"], accept_multiple_files=False
    )

    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        st.audio(audio_bytes, format="audio/wav")

    return uploaded_file


def upload_image():
    upload_img = st.file_uploader(
        "Choose image file", type=["jpg", "png", "jpeg"], accept_multiple_files=False
    )

    if upload_img:
        st.image(upload_img, caption="Your input image", width=450)

    return upload_img


# @st.cache_data
def input_text():
    text = st.text_input(
        "Text to generate", placeholder="Text to generate image with Stable Diffusion"
    )
    upload_button = st.form_submit_button("Generate image")
    if "upload_button" not in st.session_state:
        st.session_state.upload_button = False
    if upload_button or st.session_state.upload_button:
        st.session_state.upload_button = True
        if len(text) == 0:
            st.error("Please input your text")
        else:
            # image = pipe(text, guidance_scale=7.5, num_inference_steps=2).images[0]
            image = Image.open("img.jpg")
            st.image(image, caption="demo image", width=450)
            output = io.BytesIO()
            image.save(output, format="JPEG")
            img_bin = output.getvalue()
            st.download_button(
                label="Download image",
                data=img_bin,
                file_name="img.jpg",
                mime="image/jpg",
            )
            return image


def radio():
    st.header("Input image")
    choice = st.radio(
        "Choose your image", ("Upload image", "Image generated from Stable Diffusion")
    )
    if choice == "Upload image":
        image = upload_image()
    elif choice == "Image generated from Stable Diffusion":
        image = input_text()
    return image


def generate_video(upload_file, image):
    st.header("Generate video")
    if st.button("Generate video"):
        if upload_file is None:
            st.error("Please upload your audio")
        elif image is None:
            st.error("Please upload or generate image")
        else:
            progress_text = "Operation in progress. Please wait."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.05)
                my_bar.progress(percent_complete + 1, text=progress_text)

                video_file = open("star.mp4", "rb")
                video_bytes = video_file.read()

                st.video(video_bytes)

            st.download_button(
                label="Download video",
                data=video_file,
                file_name="video.mp4",
                mime="video/mp4",
            )


def main():
    st.title("Video Synthesis from Portrait Image and Audio")
    load_model()
    upload_file = upload_audio()
    st.divider()
    image = radio()
    st.divider()
    generate_video(upload_file, image)


main()
