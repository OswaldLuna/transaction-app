from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import AssistantLog
from app.schemas import SummarizeRequest, SummarizeResponse
from app.services.openai_client import client

router = APIRouter()

@router.post("/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest, db: Session = Depends(get_db)):

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "Resume el siguiente texto de manera breve y clara."},
                {"role": "user", "content": req.text}
            ],
            max_tokens=150
        )

        summary = response.choices[0].message.content

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando OpenAI: {str(e)}")

    log = AssistantLog(
        input_text=req.text,
        output_text=summary
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return {"summary": summary}
