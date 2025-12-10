Given the feature design contract, we need to implement a FastAPI endpoint `/api/calc-profit` and the corresponding tests. 

Here is a concise, production-ready code for the FastAPI endpoint:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ProfitCalculation(BaseModel):
    cups_planned: int
    price_per_cup: float
    cost_per_cup: float
    fixed_costs: float

class ProfitResult(BaseModel):
    revenue: float
    costs: float
    profit: float
    break_even: int

@app.post("/api/calc-profit", response_model=ProfitResult)
async def calc_profit(profit_calc: ProfitCalculation):
    if profit_calc.cups_planned < 0 or profit_calc.price_per_cup < 0 or profit_calc.cost_per_cup < 0 or profit_calc.fixed_costs < 0:
        raise HTTPException(status_code=400, detail="Input values must be positive.")
    
    revenue = profit_calc.cups_planned * profit_calc.price_per_cup
    costs = profit_calc.cups_planned * profit_calc.cost_per_cup + profit_calc.fixed_costs
    profit = revenue - costs
    break_even = int(profit_calc.fixed_costs / (profit_calc.price_per_cup - profit_calc.cost_per_cup)) if profit_calc.price_per_cup > profit_calc.cost_per_cup else -1

    return ProfitResult(revenue=revenue, costs=costs, profit=profit, break_even=break_even)
```

And here are the corresponding tests:

```python
from fastapi.testclient import TestClient

def test_calc_profit():
    client = TestClient(app)
    response = client.post(
        "/api/calc-profit",
        json={
            "cups_planned": 100,
            "price_per_cup": 1.0,
            "cost_per_cup": 0.5,
            "fixed_costs": 20.0
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "revenue": 100.0,
        "costs": 70.0,
        "profit": 30.0,
        "break_even": 40
    }

def test_calc_profit_negative_input():
    client = TestClient(app)
    response = client.post(
        "/api/calc-profit",
        json={
            "cups_planned": -100,
            "price_per_cup": 1.0,
            "cost_per_cup": 0.5,
            "fixed_costs": 20.0
        },
    )
    assert response.status_code == 400
```

Please note that the Next.js frontend implementation is not included as it's not part of the backend stack.