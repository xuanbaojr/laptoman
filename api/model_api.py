import io
import os
import time
from contextlib import asynccontextmanager
from typing import Annotated, List

import torch
from diffusers import StableDiffusionPipeline
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from PIL import Image
from pydantic import BaseModel

from src.inference import SadTalker


class Prompt(BaseModel):
    text: str


class FaceAudio(BaseModel):
    audio_path: str
    image_path: str


models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    model_id = "stable-diffusion-v1-4"
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    pipe.enable_attention_slicing()
    pipe.to(device)

    models["pipe"] = pipe

    sad_talker = SadTalker(
        checkpoint_path="checkpoints", config_path="src/config", lazy_load=True
    )

    models["sad_talker"] = sad_talker

    yield
    models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.post("/prediction/")
def predict(prompt: Prompt):
    image = models["pipe"](
        prompt.text, guidance_scale=7.5, num_inference_steps=25, height=512, width=512
    ).images[0]
    img = io.BytesIO()
    image.save(img, format="PNG")
    img_byte_arr = img.getvalue()
    return Response(content=img_byte_arr, media_type="image/png")


@app.post("/video/")
def create_item(files: List[UploadFile] = File(...)):
    audio_path, image_path = files[0].filename, files[1].filename

    for file in files:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
        file.file.close()

    result_path = models["sad_talker"].test(image_path, audio_path)

    with open(result_path, 'rb') as fd:
        contents = fd.read()

    return Response(content=contents, media_type="video/mp4")