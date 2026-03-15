from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.route import RouteCreate, RouteUpdate, RouteResponse
from app.services import route_service

router = APIRouter(
    prefix="/routes",
    tags=["Trasy"]
)


@router.get("/", response_model=list[RouteResponse])
def get_routes(db: Session = Depends(get_db)):
    return route_service.get_all_routes(db)


@router.get("/{route_id}", response_model=RouteResponse)
def get_route(route_id: int, db: Session = Depends(get_db)):
    return route_service.get_route_by_id(route_id, db)


@router.post("/", response_model=RouteResponse, status_code=201)
def create_route(data: RouteCreate, db: Session = Depends(get_db)):
    return route_service.create_route(data, db)


@router.put("/{route_id}", response_model=RouteResponse)
def update_route(route_id: int, data: RouteUpdate, db: Session = Depends(get_db)):
    return route_service.update_route(route_id, data, db)


@router.delete("/{route_id}")
def delete_route(route_id: int, db: Session = Depends(get_db)):
    return route_service.delete_route(route_id, db)