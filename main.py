from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import io
import logging
from typing import Optional, Annotated
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get API key from environment
API_KEY = os.getenv("X_API_KEY")
if not API_KEY:
    logger.warning("X_API_KEY not set in environment variables. API will be accessible without authentication!")

# Get allowed origins from environment
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS if origin.strip()]

app = FastAPI(
    title="Python Remove Background Provider",
    description="Background removal service using Python rembg",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication dependency
async def verify_api_key(x_api_key: Annotated[str | None, Header()] = None):
    """
    Verify API key from X-API-Key header
    """
    if not API_KEY:
        # If no API key is configured, allow access (for development)
        return True
    
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="X-API-Key header is required"
        )
    
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    return True

# Request model for background removal options
class BackgroundRemovalRequest(BaseModel):
    model: Optional[str] = "u2net"  # u2net, u2net_human_seg, silueta, isnet-general-use
    alpha_matting: Optional[bool] = False
    alpha_matting_foreground_threshold: Optional[int] = 240
    alpha_matting_background_threshold: Optional[int] = 10
    alpha_matting_erode_size: Optional[int] = 10

@app.get("/")
async def root():
    return {"message": "Python Remove Background Provider", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "python-remove-bg-provider"}

@app.post("/bg/remove")
async def remove_background(
    file: UploadFile = File(...),
    model: str = "u2net",
    alpha_matting: bool = False,
    alpha_matting_foreground_threshold: int = 240,
    alpha_matting_background_threshold: int = 10,
    alpha_matting_erode_size: int = 10,
    _: bool = Depends(verify_api_key)
):
    """
    Remove background from uploaded image using rembg
    
    Args:
        file: Image file to process
        model: rembg model to use (u2net, u2net_human_seg, silueta, isnet-general-use)
        alpha_matting: Enable alpha matting for better edge quality
        alpha_matting_foreground_threshold: Foreground threshold for alpha matting
        alpha_matting_background_threshold: Background threshold for alpha matting
        alpha_matting_erode_size: Erode size for alpha matting
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read file content
        file_content = await file.read()
        
        # Import rembg here to avoid import errors if not installed
        try:
            from rembg import remove, new_session
        except ImportError:
            raise HTTPException(
                status_code=500, 
                detail="rembg not installed. Please install with: pip install rembg"
            )
        
        # Create session with specified model
        session = new_session(model)
        
        # Remove background
        logger.info(f"Processing image with model: {model}")
        
        # Configure alpha matting if enabled
        if alpha_matting:
            output = remove(
                file_content,
                session=session,
                alpha_matting=alpha_matting,
                alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
                alpha_matting_background_threshold=alpha_matting_background_threshold,
                alpha_matting_erode_size=alpha_matting_erode_size
            )
        else:
            output = remove(file_content, session=session)
        
        # Return processed image
        return Response(
            content=output,
            media_type="image/png",
            headers={
                "Content-Disposition": f"attachment; filename=bg_removed_{file.filename}",
                "X-Original-Filename": file.filename or "image",
                "X-Model-Used": model
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/bg/remove-advanced")
async def remove_background_advanced(
    file: UploadFile = File(...),
    model: str = "u2net",
    alpha_matting: bool = False,
    alpha_matting_foreground_threshold: int = 240,
    alpha_matting_background_threshold: int = 10,
    alpha_matting_erode_size: int = 10,
    _: bool = Depends(verify_api_key)
):
    """
    Advanced background removal with full configuration options
    """
    return await remove_background(
        file=file,
        model=model,
        alpha_matting=alpha_matting,
        alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
        alpha_matting_background_threshold=alpha_matting_background_threshold,
        alpha_matting_erode_size=alpha_matting_erode_size
    )

@app.get("/models")
async def list_available_models(_: bool = Depends(verify_api_key)):
    """
    List available rembg models
    """
    return {
        "models": [
            {
                "name": "u2net",
                "description": "General purpose model, good balance of speed and quality"
            },
            {
                "name": "u2net_human_seg",
                "description": "Optimized for human subjects"
            },
            {
                "name": "silueta",
                "description": "Good for portraits and people"
            },
            {
                "name": "isnet-general-use",
                "description": "High quality general purpose model"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or default to 8001
    port = int(os.getenv("PORT", 8001))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting Python Remove Background Provider on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
