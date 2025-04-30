import uvicorn
from app.main import app
from app.mcp_server import mcp_app
import multiprocessing

def run_main_app():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def run_mcp_app():
    uvicorn.run(mcp_app, host="0.0.0.0", port=8001)

if __name__ == "__main__":
    # Run both servers in separate processes
    main_process = multiprocessing.Process(target=run_main_app)
    mcp_process = multiprocessing.Process(target=run_mcp_app)
    
    main_process.start()
    mcp_process.start()
    
    main_process.join()
    mcp_process.join()
