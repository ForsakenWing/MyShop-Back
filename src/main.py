from uvicorn import run
from src.core import Base, engine


def main():
    Base.metadata.create_all(bind=engine)
    run(
        app="v1.api:app",
        host="0.0.0.0",
        port=8088,
        use_colors=True
    )


if __name__ == "__main__":
    main()
