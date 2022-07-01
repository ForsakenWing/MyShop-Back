import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="localhost",
        port=9800,
        log_level="debug",
        reload=True,
        reload_dirs=["./"],
    )
