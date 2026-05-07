# 1. Imports
from fastapi import FastAPI, File, HTTPException, UploadFile
from ultralytics import YOLO
from PIL import Image, UnidentifiedImageError
import io

# 2. Create FastAPI app
app = FastAPI()

# 3. Load YOLO model
model = YOLO("model/best.pt")

# 4. Home route
@app.get("/")
def home():
    return {"message": "YOLO API running"}

# 5. Prediction endpoint
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image")

    image_bytes = await file.read()

    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image")

    results = model(image)

    detections = []

    for r in results:
        for box in r.boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = [float(value) for value in box.xyxy[0]]

            label = model.names[cls]

            detections.append({
                "label": label,
                "confidence": round(conf, 2),
                "box": {
                    "x1": round(x1, 2),
                    "y1": round(y1, 2),
                    "x2": round(x2, 2),
                    "y2": round(y2, 2)
                }
            })

    return {
        "detections": detections
    }