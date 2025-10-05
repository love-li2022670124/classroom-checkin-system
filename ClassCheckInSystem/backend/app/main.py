from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware  # pyright: ignore[reportMissingImports]
from .routers.common import router as common_router
from .routers.student import router as student_router
from .routers.teacher import router as teacher_router
from .routers.admin import router as admin_router

app = FastAPI(title="ClassCheckIn System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(common_router)
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(admin_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
