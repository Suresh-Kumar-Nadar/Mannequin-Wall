from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from roop.core import start, decode_execution_providers, suggest_max_memory, suggest_execution_threads
from roop.processors.frame.core import get_frame_processors_modules
from roop.utilities import normalize_output_path
import roop.globals
from PIL import Image
import io
import os

app = FastAPI()

# Allow frontend on Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/swap_faces")
async def swap_faces(
    source_image: UploadFile = File(...),
    face_enhancer: bool = Form(False)
):
    source_path = "input.jpg"
    target_path = "target.jpg"
    output_path = "output.jpg"
    final_output = "final.jpg"
    preimage_path = "preimage.jpg"

    if not os.path.exists(target_path):
        return {"error": "Target image (target.jpg) not found on server."}
    if not os.path.exists(preimage_path):
        return {"error": "Preimage (preimage.jpg) not found on server."}

    # Save the uploaded image
    source_data = await source_image.read()
    Image.open(io.BytesIO(source_data)).save(source_path)

    # Setup Roop
    roop.globals.source_path = source_path
    roop.globals.target_path = target_path
    roop.globals.output_path = normalize_output_path(source_path, target_path, output_path)
    roop.globals.frame_processors = ["face_swapper", "face_enhancer"] if face_enhancer else ["face_swapper"]
    roop.globals.headless = True
    roop.globals.keep_fps = True
    roop.globals.keep_audio = True
    roop.globals.keep_frames = False
    roop.globals.many_faces = False
    roop.globals.video_encoder = "libx264"
    roop.globals.video_quality = 18
    roop.globals.max_memory = suggest_max_memory()
    roop.globals.execution_providers = decode_execution_providers(["cuda"])
    roop.globals.execution_threads = suggest_execution_threads()

    for processor in get_frame_processors_modules(roop.globals.frame_processors):
        if not processor.pre_check():
            return {"error": f"{processor.__class__.__name__} failed pre-check."}

    # Run swap
    start()

    # Post-process: composite onto preimage
    try:
        image = Image.open(preimage_path)
        cut = Image.open(output_path)

        x1, y1 = 377, 0
        x2, y2 = 634, 1000

        # White rectangle
        white_box = Image.new("RGB", (x2 - x1, y2 - y1), color=(255, 255, 255))
        image.paste(white_box, (x1, y1))

        # Paste swapped face into preimage
        image.paste(cut, (x1, y1))
        image.save(final_output)

    except Exception as e:
        return {"error": f"Post-processing failed: {str(e)}"}

    return FileResponse(final_output, media_type="image/jpeg")
