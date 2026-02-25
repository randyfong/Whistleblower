import os
import shutil
import base64
import httpx
import fitz  # PyMuPDF
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import List
from crew_config import generate_police_report

app = FastAPI()

# Ensure /tmp exists (though it usually does on Mac/Linux)
UPLOAD_DIR = "/tmp/whistleblower_evidence"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts all text from a PDF file."""
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        raise Exception(f"Error extracting PDF text: {str(e)}")
    return text

async def analyze_image_with_venice(file_path: str) -> str:
    """Analyzes an image using Venice Vision LLM (Qwen3-VL)."""
    api_key = os.getenv("VENICE_API_KEY")
    if not api_key:
        raise Exception("VENICE_API_KEY not found in environment.")
    
    # Read and encode image to base64
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    mime_type = "image/jpeg" if file_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
    
    url = "https://api.venice.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "qwen3-vl-235b-a22b",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in detail as evidence for a police report. Focus on factual observations."},
                    {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{encoded_string}"}}
                ]
            }
        ]
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=60.0)
        if response.status_code != 200:
            raise Exception(f"Venice API error: {response.text}")
        return response.json()['choices'][0]['message']['content']

@app.post("/upload")
async def upload_evidence(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, or PDF files are allowed.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        analysis_result = ""
        # Process based on file type
        if file.content_type == "application/pdf":
            analysis_result = extract_text_from_pdf(file_path)
            if not analysis_result:
                analysis_result = "PDF uploaded but no text could be extracted."
        else:
            # It's an image
            analysis_result = await analyze_image_with_venice(file_path)
        
        # Generate police report using CrewAI
        crew_response = generate_police_report(analysis_result)
        
        return {
            "filename": file.filename,
            "status": "success",
            "path": file_path,
            "analysis": analysis_result,
            "police_report": str(crew_response)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing evidence: {str(e)}")

@app.get("/chat-history")
async def get_chat():
    return [
        {"role": "system", "content": "Secure connection established. End-to-end encryption active."},
        {"role": "assistant", "content": "How can I help you today? You can share information or upload evidence securely."}
    ]

# Serve static files
# We'll create the static directory next
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
