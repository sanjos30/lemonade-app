Given the constraints and requirements, here is a concise implementation of the FastAPI backend and the associated tests.

First, let's create the FastAPI application in `main.py`:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ProfitCalculationInput(BaseModel):
    cups_planned: float
    price_per_cup: float
    cost_per_cup: float
    fixed_costs: float

class ProfitCalculationOutput(BaseModel):
    revenue: float
    variable_costs: float
    total_costs: float
    profit: float
    break_even_cups: float

@app.post("/api/calc-profit", response_model=ProfitCalculationOutput)
async def calc_profit(input: ProfitCalculationInput):
    if input.cups_planned < 0 or input.price_per_cup < 0 or input.cost_per_cup < 0 or input.fixed_costs < 0:
        raise HTTPException(status_code=400, detail="Invalid input")

    revenue = input.cups_planned * input.price_per_cup
    variable_costs = input.cups_planned * input.cost_per_cup
    total_costs = variable_costs + input.fixed_costs
    profit = revenue - total_costs
    break_even_cups = input.fixed_costs / (input.price_per_cup - input.cost_per_cup) if input.price_per_cup > input.cost_per_cup else float('inf')

    return ProfitCalculationOutput(
        revenue=revenue,
        variable_costs=variable_costs,
        total_costs=total_costs,
        profit=profit,
        break_even_cups=break_even_cups
    )
```

Next, let's write the tests in `test_main.py`:

```python
from fastapi.testclient import TestClient
from main import app, ProfitCalculationInput

client = TestClient(app)

def test_calc_profit():
    response = client.post(
        "/api/calc-profit",
        json=ProfitCalculationInput(
            cups_planned=100,
            price_per_cup=1.0,
            cost_per_cup=0.5,
            fixed_costs=50.0
        ).dict()
    )
    assert response.status_code == 200
    assert response.json() == {
        "revenue": 100.0,
        "variable_costs": 50.0,
        "total_costs": 100.0,
        "profit": 0.0,
        "break_even_cups": 100.0
    }

def test_calc_profit_bad_request():
    response = client.post(
        "/api/calc-profit",
        json=ProfitCalculationInput(
            cups_planned=-1,
            price_per_cup=1.0,
            cost_per_cup=0.5,
            fixed_costs=50.0
        ).dict()
    )
    assert response.status_code == 400
```

This code includes the FastAPI application with the `/api/calc-profit` endpoint and the associated tests. The endpoint takes an input model `ProfitCalculationInput` and returns an output model `ProfitCalculationOutput`. The tests cover a successful calculation and a bad request scenario.