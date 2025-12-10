Given the stack and the feature requirements, we can create a FastAPI application with a single endpoint `/api/calc-profit`. This endpoint will receive the inputs and return the calculated values.

First, let's define the data models for the request and response. Create a new file `models.py` in the backend directory:

```python
from pydantic import BaseModel

class ProfitCalculationRequest(BaseModel):
    cups_planned: int
    price_per_cup: float
    cost_per_cup: float
    fixed_costs: float

class ProfitCalculationResponse(BaseModel):
    revenue: float
    variable_costs: float
    total_costs: float
    profit: float
    break_even_cups: int
```

Next, let's create the FastAPI application and define the `/api/calc-profit` endpoint. Create a new file `main.py` in the backend directory:

```python
from fastapi import FastAPI, HTTPException
from models import ProfitCalculationRequest, ProfitCalculationResponse

app = FastAPI()

@app.post("/api/calc-profit", response_model=ProfitCalculationResponse)
async def calculate_profit(request: ProfitCalculationRequest):
    if request.cups_planned < 0 or request.price_per_cup < 0 or request.cost_per_cup < 0 or request.fixed_costs < 0:
        raise HTTPException(status_code=400, detail="All inputs must be non-negative")

    revenue = request.cups_planned * request.price_per_cup
    variable_costs = request.cups_planned * request.cost_per_cup
    total_costs = variable_costs + request.fixed_costs
    profit = revenue - total_costs
    break_even_cups = int(request.fixed_costs / (request.price_per_cup - request.cost_per_cup)) if request.price_per_cup > request.cost_per_cup else 0

    return ProfitCalculationResponse(
        revenue=revenue,
        variable_costs=variable_costs,
        total_costs=total_costs,
        profit=profit,
        break_even_cups=break_even_cups
    )
```

Finally, let's write some tests for our application. Create a new file `test_main.py` in the `tests_dir`:

```python
from fastapi.testclient import TestClient
from main import app
from models import ProfitCalculationRequest

client = TestClient(app)

def test_calculate_profit():
    request = ProfitCalculationRequest(
        cups_planned=100,
        price_per_cup=1.0,
        cost_per_cup=0.5,
        fixed_costs=10.0
    )
    response = client.post("/api/calc-profit", json=request.dict())
    assert response.status_code == 200
    assert response.json() == {
        "revenue": 100.0,
        "variable_costs": 50.0,
        "total_costs": 60.0,
        "profit": 40.0,
        "break_even_cups": 20
    }

def test_calculate_profit_negative_input():
    request = ProfitCalculationRequest(
        cups_planned=-100,
        price_per_cup=1.0,
        cost_per_cup=0.5,
        fixed_costs=10.0
    )
    response = client.post("/api/calc-profit", json=request.dict())
    assert response.status_code == 400
```

This code provides a complete implementation of the backend for the Lemonade Stand Planner MVP feature. It includes input validation, calculation logic, and tests.