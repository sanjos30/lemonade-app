Given the project's stack and conventions, we will be using FastAPI for the backend. Since the project does not require a database, we will be focusing on the API endpoint and the business logic for calculating the profit.

Here is a minimal, clean code that compiles:

```python
# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ProfitInput(BaseModel):
    cups_planned: int
    price_per_cup: float
    cost_per_cup: float
    fixed_costs: float

class ProfitOutput(BaseModel):
    revenue: float
    variable_costs: float
    total_costs: float
    profit: float
    break_even_cups: int

@app.post("/api/calc-profit", response_model=ProfitOutput)
async def calc_profit(input: ProfitInput):
    if input.cups_planned < 0 or input.price_per_cup < 0 or input.cost_per_cup < 0 or input.fixed_costs < 0:
        raise HTTPException(status_code=400, detail="Invalid input: all inputs must be non-negative.")
    
    revenue = input.cups_planned * input.price_per_cup
    variable_costs = input.cups_planned * input.cost_per_cup
    total_costs = variable_costs + input.fixed_costs
    profit = revenue - total_costs
    break_even_cups = int(input.fixed_costs / (input.price_per_cup - input.cost_per_cup)) if input.price_per_cup > input.cost_per_cup else 0

    return ProfitOutput(
        revenue=revenue,
        variable_costs=variable_costs,
        total_costs=total_costs,
        profit=profit,
        break_even_cups=break_even_cups
    )
```

And here are the unit tests for the generated code:

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_calc_profit():
    response = client.post(
        "/api/calc-profit",
        json={"cups_planned": 100, "price_per_cup": 1.0, "cost_per_cup": 0.5, "fixed_costs": 20.0},
    )
    assert response.status_code == 200
    assert response.json() == {
        "revenue": 100.0,
        "variable_costs": 50.0,
        "total_costs": 70.0,
        "profit": 30.0,
        "break_even_cups": 40
    }

def test_calc_profit_negative_input():
    response = client.post(
        "/api/calc-profit",
        json={"cups_planned": -100, "price_per_cup": 1.0, "cost_per_cup": 0.5, "fixed_costs": 20.0},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid input: all inputs must be non-negative."}
```

To run the tests, use the command `pytest test_main.py`.