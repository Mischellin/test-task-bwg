import uvicorn

from config import settings


def run_uvicorn_server():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    run_uvicorn_server()
