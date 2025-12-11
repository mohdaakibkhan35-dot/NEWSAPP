from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Annotated
import pickle

# Load model bundle (vectorizer + model)
with open("all_model.pkl", "rb") as f:
    model_bundle = pickle.load(f)

vectorizer = model_bundle["vectorizer"]
log_model = model_bundle["log_model"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # change "*" to your actual frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsItem(BaseModel):
    text: Annotated[str, Field(..., description="Enter the news text")]

@app.post("/predict")
def predict_premium(data: NewsItem):

    # Convert input text → TF-IDF
    vectorized_input = vectorizer.transform([data.text])

    # Predict (0 = Fake, 1 = Real)
    prediction = log_model.predict(vectorized_input)[0]
    result = "Perfectly News is Right" if prediction == 1 else "Sorry, News is not Right that is Rumor"

    # return JSONResponse(status_code=200, content={"Predict_category": int(prediction)})
    return JSONResponse(status_code=200, content={"Result": result})
