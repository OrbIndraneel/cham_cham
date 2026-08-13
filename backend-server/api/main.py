from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import predict_routes, evacuation_routes, shelter_routes, sos_routes

app = FastAPI(
    title="Disaster Management AI Platform API",
    description="Backend API powering GNN Cascade Predictions and Dynamic Evacuation Routing",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict_routes.router, prefix="/api", tags=["Cascade Prediction"])
app.include_router(evacuation_routes.router, prefix="/api", tags=["Route Optimization"])
app.include_router(shelter_routes.router, prefix="/api", tags=["Safe Shelters"])
app.include_router(sos_routes.router, prefix="/api", tags=["Emergency SOS Alerts"])

@app.get("/")
def root():
    return {"message": "Disaster Management AI Backend Running", "status": "online"}
