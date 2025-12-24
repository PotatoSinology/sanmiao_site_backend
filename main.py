from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
import sanmiao
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sanmiao API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://norbert.huma-num.fr",
        "https://route-unnecessary-crocodile-sanmiao-backend.apps.math.cnrs.fr",
    ],
    allow_methods=["POST","GET"],
    allow_headers=["*"],
)

class ConvertIn(BaseModel):
    lang: Literal["en","fr"] = "en"
    proleptic: bool = Field(..., description="pg")
    gregorian_begins: Optional[str] = Field(None, description="YYYY-MM-DD or null")
    year_span_start: int = Field(..., description="tpq")
    year_span_end: int   = Field(..., description="taq")
    output_jdn: bool = Field(False, description="jd_out")
    text: str = Field("", description="user_input string (one or many, separated)")

    @field_validator("gregorian_begins")
    @classmethod
    def check_date_fmt(cls, v):
        if v is None or v == "":
            return None
        parts = v.split("-")
        if len(parts) != 3:
            raise ValueError("gregorian_begins must be YYYY-MM-DD")
        y, m, d = parts
        try:
            int(y), int(m), int(d)
        except ValueError:
            raise ValueError("gregorian_begins must be YYYY-MM-DD (integers)")
        return v

class ConvertOut(BaseModel):
    result: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/convert", response_model=ConvertOut)
def convert_endpoint(payload: ConvertIn):
    """
    Maps incoming JSON to sanmiao.cjk_date_interpreter arguments:
      user_input = payload.text
      lang       = payload.lang
      jd_out     = payload.output_jdn
      pg         = payload.proleptic
      gs         = [YYYY,MM,DD] if provided, else None
      tpq        = payload.year_span_start
      taq        = payload.year_span_end
    """
    # Parse gs
    gs_list = None
    if payload.gregorian_begins:
        y, m, d = payload.gregorian_begins.split("-")
        gs_list = [int(y), int(m), int(d)]

    try:
        # Call your package exactly as specified
        result_text = sanmiao.cjk_date_interpreter(
            payload.text,
            lang=payload.lang,
            jd_out=payload.output_jdn,
            pg=payload.proleptic,
            gs=gs_list,
            tpq=payload.year_span_start,
            taq=payload.year_span_end,
        )
    except Exception as e:
        # Return a clear error to the frontend
        raise HTTPException(status_code=400, detail=f"Conversion failed: {e}")

    # The function returns a text string to display
    return ConvertOut(result=str(result_text))

