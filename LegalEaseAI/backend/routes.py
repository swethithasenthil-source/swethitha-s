from backend.services.exporters import build_docx, build_pdf, build_txt
from backend.services.gemini_generator import GeminiDocumentGenerator
from fastapi import APIRouter, HTTPException, Response

from backend.config import get_settings
from backend.schemas import DocumentRequest, ExportRequest, GenerateResponse
from backend.services.exporters import build_docx, build_pdf, build_txt
from backend.services.gemini_generator import GeminiDocumentGenerator


router = APIRouter()

settings = get_settings()
generator = GeminiDocumentGenerator(settings)


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "gemini_configured": bool(settings.gemini_api_key),
        "demo_mode": settings.demo_mode,
        "model": settings.gemini_model,
    }


@router.post("/generate", response_model=GenerateResponse)
def generate_document(request: DocumentRequest):
    try:
        result = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
        )

        return GenerateResponse(
            document_type=request.document_type,
            text=result["text"],
            terms=result["terms"],
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {exc}",
        ) from exc


@router.post("/export")
def export_document(request: ExportRequest):
    try:
        if request.format == "txt":
            data, filename = build_txt(request.text)
            media_type = "text/plain"

        elif request.format == "docx":
            data, filename = build_docx(
                text=request.text,
                document_type=request.document_type,
                terms=request.terms,
                logo_base64=request.logo_base64,
            )
            media_type = (
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )

        elif request.format == "pdf":
            data, filename = build_pdf(
                text=request.text,
                document_type=request.document_type,
                terms=request.terms,
                logo_base64=request.logo_base64,
            )
            media_type = "application/pdf"

        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported export format.",
            )

        return Response(
            content=data,
            media_type=media_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            },
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Export failed: {exc}",
        ) from exc