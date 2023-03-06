from flask_app.app import main as run_flask

app = {
    1: run_flask,
}



if __name__ == "__main__":
    APP_ID = 1
    main(APP_ID)
