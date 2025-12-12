Given the constraints and the feature design contract, here is a concise, production-ready code for the FastAPI backend endpoint `/api/calc-profit` and its corresponding tests.

Backend Code:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class LemonadeStand(BaseModel):
    cups_planned: int
    price_per_cup: float
    cost_per_cup: float
    fixed_costs: float

class ProfitAnalysis(BaseModel):
    revenue: float
    variable_costs: float
    total_costs: float
    profit: float
    break_even_cups: int

@app.post("/api/calc-profit", response_model=ProfitAnalysis)
async def calc_profit(stand: LemonadeStand):
    try:
        revenue = stand.cups_planned * stand.price_per_cup
        variable_costs = stand.cups_planned * stand.cost_per_cup
        total_costs = variable_costs + stand.fixed_costs
        profit = revenue - total_costs
        break_even_cups = int(stand.fixed_costs / (stand.price_per_cup - stand.cost_per_cup))
        return ProfitAnalysis(revenue=revenue, variable_costs=variable_costs, total_costs=total_costs, profit=profit, break_even_cups=break_even_cups)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

Test Code:

```python
from fastapi.testclient import TestClient
from main import app, LemonadeStand

client = TestClient(app)

def test_calc_profit():
    response = client.post(
        "/api/calc-profit",
        json=LemonadeStand(cups_planned=100, price_per_cup=1.0, cost_per_cup=0.5, fixed_costs=20.0).dict()
    )
    assert response.status_code == 200
    assert response.json() == {
        "revenue": 100.0,
        "variable_costs": 50.0,
        "total_costs": 70.0,
        "profit": 30.0,
        "break_even_cups": 40
    }

def test_calc_profit_error():
    response = client.post(
        "/api/calc-profit",
        json=LemonadeStand(cups_planned=100, price_per_cup=1.0, cost_per_cup=1.5, fixed_costs=20.0).dict()
    )
    assert response.status_code == 500
```

Please note that this is a minimal implementation and does not include input validation, error handling, logging, or monitoring. These features should be added as per the project requirements and best practices.