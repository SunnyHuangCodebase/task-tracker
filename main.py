from flask_app.app import app as flask_app


def main():
    flask_app.run(debug=True)


if __name__ == "__main__":
    main()
