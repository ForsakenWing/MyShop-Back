from uvicorn import run
from core import Postgres


def main():
    Postgres.create_tables()
    run(
        app="v1.api:app",
        host="localhost",
        port=8088,
        reload=True,
        debug=True,
        use_colors=True
    )


if __name__ == "__main__":
    main()
