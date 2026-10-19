from app import create_app


def start():
    return create_app()


if __name__ == "__main__":
    start().run(debug=True)
