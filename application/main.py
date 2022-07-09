import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        port=8101,
        use_colors=True,
        host='0.0.0.0',
        reload=True,
        debug=True
    )
