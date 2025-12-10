Given the feature design contract, we'll need to implement the backend API endpoint `/api/calc-profit` using FastAPI. As the backend directory is not specified, we'll assume that the code will be placed in the root directory. 

Here is the implementation for the FastAPI application:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, Decimal

app = FastAPI()

class ProfitCalculationInput(BaseModel):
    cups_planned: int = Field(..., ge=0)
    price_per_cup: Decimal = Field(..., ge=0)
    cost_per_cup: Decimal = Field(..., ge=0)
    fixed_costs: Decimal = Field(..., ge=0)

class ProfitCalculationOutput(BaseModel):
    revenue: Decimal
    variable_costs: Decimal
    total_costs: Decimal
    profit: Decimal
    break_even_cups: int

@app.post("/api/calc-profit", response_model=ProfitCalculationOutput)
async def calc_profit(input: ProfitCalculationInput):
    revenue = input.cups_planned * input.price_per_cup
    variable_costs = input.cups_planned * input.cost_per_cup
    total_costs = variable_costs + input.fixed_costs
    profit = revenue - total_costs
    break_even_cups = int(total_costs / input.price_per_cup) if input.price_per_cup > 0 else 0

    return ProfitCalculationOutput(
        revenue=revenue,
        variable_costs=variable_costs,
        total_costs=total_costs,
        profit=profit,
        break_even_cups=break_even_cups
    )
```

For testing, we'll use FastAPI's built-in test client. Here are some basic tests:

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_calc_profit():
    response = client.post("/api/calc-profit", json={
        "cups_planned": 100,
        "price_per_cup": 1.5,
        "cost_per_cup": 0.5,
        "fixed_costs": 20.0
    })
    assert response.status_code == 200
    assert response.json() == {
        "revenue": 150.0,
        "variable_costs": 50.0,
        "total_costs": 70.0,
        "profit": 80.0,
        "break_even_cups": 47
    }

def test_calc_profit_invalid_input():
    response = client.post("/api/calc-profit", json={
        "cups_planned": -100,
        "price_per_cup": 1.5,
        "cost_per_cup": 0.5,
        "fixed_costs": 20.0
    })
    assert response.status_code == 422
```

These tests cover the basic functionality of the API endpoint. More tests should be added to cover edge cases and invalid inputs.