# 1. Imports
from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
from PIL import Image
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
    
    image_bytes = await file.read()

    image = Image.open(io.BytesIO(image_bytes))

    results = model(image)

    detections = []

    for r in results:
        for box in r.boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            label = model.names[cls]

            detections.append({
                "label": label,
                "confidence": round(conf, 2)
            })

    return {
        "detections": detections
    }