# Video Synthesis from Portrait Image and Audio

How to run Gradio App:
- git clone https://github.com/ductt-1167/ai-video-synthesis.git
- cd ai-video-synthesis
- bash api/src/download_model.sh
- pip install -r api/requirements.txt
- pip install -r client/requirements.txt
- python api/utils/save_sd.py
- uvicorn api.model_api:app --reload
- gradio client/app_gradio.py
## Introduction
A demo Gradio application helps user generate video from audio and face image using SadTalker and Stable Diffusion

## Environments Prequisition
To run the application, you need to install Python version>=3.8 in your machine. We recommend using Anaconda or Miniconda to install Python libraries and configure environment.

You also need to install **ffmpeg** on your machine: `sudo apt install ffmpeg` (Linux) or download from https://ffmpeg.org/download.html (Windows)

**Updated**: You need to install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) on your machine **if you want to run the application in Docker**

## Installation
<b>Note: the installation of models is quite slow due to its size, so wait for it to be installed before continuing to the next step.</b>

- Clone the project to your local machine:

```git clone https://github.com/ductt-1167/ai-video-synthesis.git```

```cd ai-video-synthesis```

- Download the necessary libraries (skip this if you run Docker):

```pip install -r api/requirements.txt```

```pip install -r client/requirements.txt```

- Download SadTalker and Stable Diffusion models:

```bash api/src/download_model.sh```

```python api/utils/save_sd.py```

**If you want to run directly on your machine environment:**
- Run the model api endpoint written in FastAPI:
```uvicorn model_api:app --reload```

- Switch to another terminal, run the Gradio application:
    - Reload mode: `gradio app_gradio.py`
    - Normal: `python app_gradio.py`

**If you want to run in Docker mode:**
- Build and run the Docker application:
```docker compose up --build```

## Issues
- If your issues related to **ffmpeg** or **ffprobe**, you can re-install **ffmpeg** in Conda environment: `conda install -c conda-forge ffmpeg`
