from fastapi import FastAPI
from presentation.routes.auth import router as auth_router
from presentation.routes.payment import router as payment_router
# from settings.config import get_settings

app = FastAPI()
app.include_router(auth_router)
app.include_router(payment_router)

# login routes
@app.get("/")
async def root():
    return {"message": "Clean Architecture API is running!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "my-clean-api"}

# payment routes




if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)