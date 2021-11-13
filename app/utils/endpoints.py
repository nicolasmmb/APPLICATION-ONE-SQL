from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/utils",
    tags=["UTILITIES"]
)


@router.get('/endpoints/')
def list_endpoints(request: Request):
    url_list = [
        {'path': route.path, 'name': route.name}
        for route in request.app.routes
    ]
    return url_list
