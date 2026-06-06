from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.certificates import router as certificates_router
from app.api.analysis import router as analysis_router
from app.api.evidence import router as evidence_router
from app.api.timeline import router as timeline_router
from app.api.skills import router as skills_router
from app.api.twin import router as twin_router
from app.api.fraud_detection import router as fraud_router
from app.api.dashboard import router as dashboard_router

app = FastAPI(
    title="EduProof AI"
)

app.include_router(
    upload_router,
    prefix="/upload",
    tags=["Upload"]
)

app.include_router(
    certificates_router,
    prefix="/certificates",
    tags=["Certificates"]
)

app.include_router(
    analysis_router,
    prefix="/analysis",
    tags=["Analysis"]
)

app.include_router(
    evidence_router,
    prefix="/evidence",
    tags=["Evidence"]
)

app.include_router(
    timeline_router,
    prefix="/timeline",
    tags=["Timeline"]
)

app.include_router(
    skills_router,
    prefix="/skills",
    tags=["Skills"]
)

app.include_router(
    twin_router,
    prefix="/twin",
    tags=["Digital Twin"]
)

app.include_router(
    fraud_router,
    prefix="/fraud",
    tags=["Fraud Detection"]
)

app.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"]
)


@app.get("/")
def root():
    return {
        "message": "EduProof AI Backend Running"
    }