# At the top of your main.py file, before any other imports
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"detail": exc.detail, "status_code": exc.status_code}

# Health check
@app.get("/healthz")
async def health_check():
    return {"status": "healthy"}

# Root route
@app.get("/")
async def root():
    return {
        "status": "online",
        "version": "1.0",
        "available_endpoints": [
            "/",
            "/healthz",
            "/test (GET)",
            "/test (POST)"
        ]
    }

# Test endpoints
@app.get("/test")
async def test_get():
    return {"message": "GET request successful"}

@app.post("/test")
async def test_post(data: dict):
    return {"message": "POST request successful", "data": data}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)