Given the stack and the feature design contract, we can implement the backend API using FastAPI. The API will have a single endpoint `/api/calc-profit` that accepts a POST request with the required parameters and returns the calculated values.

Here is the implementation:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class ProfitInput(BaseModel):
    cups_planned: int = Field(..., gt=0)
    price_per_cup: float = Field(..., gt=0)
    cost_per_cup: float = Field(..., gt=0)
    fixed_costs: float = Field(..., ge=0)

class ProfitOutput(BaseModel):
    revenue: float
    variable_costs: float
    total_costs: float
    profit: float
    break_even_cups: int

@app.post("/api/calc-profit", response_model=ProfitOutput)
async def calc_profit(input: ProfitInput):
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

For testing, we can write unit tests to validate the calculation logic and integration tests to validate the API endpoint. Here are some example tests:

```python
from fastapi.testclient import TestClient

def test_calc_profit():
    client = TestClient(app)
    response = client.post("/api/calc-profit", json={
        "cups_planned": 100,
        "price_per_cup": 1.0,
        "cost_per_cup": 0.5,
        "fixed_costs": 10.0
    })
    assert response.status_code == 200
    assert response.json() == {
        "revenue": 100.0,
        "variable_costs": 50.0,
        "total_costs": 60.0,
        "profit": 40.0,
        "break_even_cups": 20
    }

def test_calc_profit_invalid_input():
    client = TestClient(app)
    response = client.post("/api/calc-profit", json={
        "cups_planned": -100,
        "price_per_cup": 1.0,
        "cost_per_cup": 0.5,
        "fixed_costs": 10.0
    })
    assert response.status_code == 422
```

This code and tests should be placed in the appropriate directories according to the project's structure.