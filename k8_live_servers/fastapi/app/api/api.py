from fastapi    import APIRouter
from .endpoints import screenshot

router = APIRouter()
router.include_router(screenshot.router)