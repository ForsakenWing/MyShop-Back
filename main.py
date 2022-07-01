import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="localhost",
        port=8800,
    )
