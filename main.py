import duckdb as dd
from fastapi import FastAPI
import pickle

app = FastAPI()


def get_db():
    """
    Instantiate database
    """
    return dd.read_csv("car_price.csv")


@app.get("/")
def root():
    return {"status": "succeed"}


@app.get("/hello")
def say_hello(greeting: str):
    return {"greetings": greeting}


@app.get("/car/{car_id}")
def read_db(car_id: int):
    get_db()
    car_info = (
        dd.sql(f"SELECT * FROM car_price.csv WHERE car_id = {car_id}")
        .fetchdf()
        .to_dict("index")
    )
    return {"car_id": car_id, "info": car_info}


def get_regressor_model():
    model = pickle.load(open("linear_regressor_model.pkl", "wb"))
    return model


@app.get("/predict")
def predict_price():
    model = get_regressor_model()
    prediction = model.predict()
    return {"pred_price": prediction}
