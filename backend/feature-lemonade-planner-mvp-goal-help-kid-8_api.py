Sure, here is a basic implementation of the backend using FastAPI in Python. 

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class ProfitCalculationInput(BaseModel):
    cups_planned: int = Field(..., gt=0)
    price_per_cup: float = Field(..., gt=0)
    cost_per_cup: float = Field(..., gt=0)
    fixed_costs: float = Field(..., gt=0)

class ProfitCalculationOutput(BaseModel):
    revenue: float
    variable_costs: float
    total_costs: float
    profit: float
    break_even_cups: int

@app.post("/api/calc-profit", response_model=ProfitCalculationOutput)
async def calculate_profit(input: ProfitCalculationInput):
    revenue = input.cups_planned * input.price_per_cup
    variable_costs = input.cups_planned * input.cost_per_cup
    total_costs = variable_costs + input.fixed_costs
    profit = revenue - total_costs
    break_even_cups = int(input.fixed_costs / (input.price_per_cup - input.cost_per_cup)) if input.price_per_cup > input.cost_per_cup else 0

    return ProfitCalculationOutput(
        revenue=revenue,
        variable_costs=variable_costs,
        total_costs=total_costs,
        profit=profit,
        break_even_cups=break_even_cups
    )
```

And here are some basic tests for the API:

```python
from fastapi.testclient import TestClient

def test_calculate_profit():
    client = TestClient(app)
    response = client.post(
        "/api/calc-profit",
        json={
            "cups_planned": 100,
            "price_per_cup": 1.0,
            "cost_per_cup": 0.5,
            "fixed_costs": 10.0
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "revenue": 100.0,
        "variable_costs": 50.0,
        "total_costs": 60.0,
        "profit": 40.0,
        "break_even_cups": 20
    }

def test_calculate_profit_invalid_input():
    client = TestClient(app)
    response = client.post(
        "/api/calc-profit",
        json={
            "cups_planned": -100,
            "price_per_cup": 1.0,
            "cost_per_cup": 0.5,
            "fixed_costs": 10.0
        },
    )
    assert response.status_code == 422
```

This code and tests should be placed in the backend directory of your project. The tests can be run using the command `pytest`.