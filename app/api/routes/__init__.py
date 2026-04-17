from fastapi import APIRouter

from app.api.routes import auth, check, training, algorithm, crawler, system

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(check.router, prefix="/check", tags=["check"])
api_router.include_router(training.router, prefix="/training", tags=["training"])
api_router.include_router(algorithm.router, prefix="/algorithm", tags=["algorithm"])
api_router.include_router(crawler.router, prefix="/crawler", tags=["crawler"])
api_router.include_router(system.router, prefix="/system", tags=["system"])
