from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime

app = FastAPI(
    title="Korea Trade & Export API",
    description="Real-time Korea trade, export, and import data powered by World Bank Open Data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WB_BASE_URL = "https://api.worldbank.org/v2/country/KR/indicator"

INDICATORS = {
    "exports":      {"id": "NE.EXP.GNFS.ZS",  "name": "Exports of Goods & Services",       "unit": "% of GDP"},
    "imports":      {"id": "NE.IMP.GNFS.ZS",  "name": "Imports of Goods & Services",       "unit": "% of GDP"},
    "trade_gdp":    {"id": "NE.TRD.GNFS.ZS",  "name": "Trade",                             "unit": "% of GDP"},
    "merch_exports":{"id": "TX.VAL.MRCH.CD.WT","name": "Merchandise Exports",               "unit": "Current USD"},
    "merch_imports":{"id": "TM.VAL.MRCH.CD.WT","name": "Merchandise Imports",               "unit": "Current USD"},
    "tech_exports": {"id": "TX.VAL.TECH.MF.ZS","name": "High-Technology Exports",           "unit": "% of Manufactured Exports"},
    "current_acct": {"id": "BN.CAB.XOKA.CD",  "name": "Current Account Balance",           "unit": "Current USD (BoP)"},
    "fdi_inflows":  {"id": "BX.KLT.DINV.CD.WD","name": "Foreign Direct Investment Inflows", "unit": "Current USD (BoP)"},
}


async def fetch_wb(indicator_id: str, limit: int = 10):
    url = f"{WB_BASE_URL}/{indicator_id}"
    params = {
        "format": "json",
        "mrv": limit,
        "per_page": limit,
    }
    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params, timeout=15)
        data = res.json()

    if not data or len(data) < 2:
        return []

    records = data[1] or []
    return [
        {"year": str(r["date"]), "value": r["value"]}
        for r in records
        if r.get("value") is not None
    ]


@app.get("/")
def root():
    return {
        "api": "Korea Trade & Export API",
        "version": "1.0.0",
        "description": "Korea trade statistics — exports, imports, trade balance, FDI, and more",
        "endpoints": [
            "/summary",
            "/exports",
            "/imports",
            "/balance",
            "/tech-exports",
            "/trade-gdp",
            "/fdi",
        ],
        "source": "World Bank Open Data (data.worldbank.org)",
        "country": "Korea, Republic of (KR)",
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/summary")
async def summary(limit: int = Query(default=1, ge=1, le=30)):
    """Get latest values for all key Korea trade indicators."""
    result = {}
    for key, meta in INDICATORS.items():
        data = await fetch_wb(meta["id"], limit=limit)
        result[key] = {
            "name": meta["name"],
            "unit": meta["unit"],
            "data": data,
        }
    return {
        "country": "Korea, Republic of",
        "source": "World Bank Open Data",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "indicators": result,
    }


@app.get("/exports")
async def exports(limit: int = Query(default=10, ge=1, le=60)):
    """Korea exports of goods and services (% of GDP, annual)."""
    data = await fetch_wb("NE.EXP.GNFS.ZS", limit)
    return {
        "indicator": "Exports of Goods and Services",
        "unit": "% of GDP",
        "frequency": "Annual",
        "country": "Korea, Republic of",
        "source": "World Bank",
        "data": data,
    }


@app.get("/imports")
async def imports(limit: int = Query(default=10, ge=1, le=60)):
    """Korea imports of goods and services (% of GDP, annual)."""
    data = await fetch_wb("NE.IMP.GNFS.ZS", limit)
    return {
        "indicator": "Imports of Goods and Services",
        "unit": "% of GDP",
        "frequency": "Annual",
        "country": "Korea, Republic of",
        "source": "World Bank",
        "data": data,
    }


@app.get("/balance")
async def trade_balance(limit: int = Query(default=10, ge=1, le=60)):
    """Korea current account balance (BoP, current USD)."""
    data = await fetch_wb("BN.CAB.XOKA.CD", limit)
    return {
        "indicator": "Current Account Balance",
        "unit": "Current USD (Balance of Payments)",
        "frequency": "Annual",
        "country": "Korea, Republic of",
        "source": "World Bank",
        "data": data,
    }


@app.get("/tech-exports")
async def tech_exports(limit: int = Query(default=10, ge=1, le=60)):
    """Korea high-technology exports (% of manufactured exports)."""
    data = await fetch_wb("TX.VAL.TECH.MF.ZS", limit)
    return {
        "indicator": "High-Technology Exports",
        "unit": "% of Manufactured Exports",
        "frequency": "Annual",
        "country": "Korea, Republic of",
        "source": "World Bank",
        "note": "Includes semiconductors, electronics, aerospace, and pharma",
        "data": data,
    }


@app.get("/trade-gdp")
async def trade_gdp(limit: int = Query(default=10, ge=1, le=60)):
    """Korea total trade as % of GDP (exports + imports)."""
    data = await fetch_wb("NE.TRD.GNFS.ZS", limit)
    return {
        "indicator": "Trade (Exports + Imports)",
        "unit": "% of GDP",
        "frequency": "Annual",
        "country": "Korea, Republic of",
        "source": "World Bank",
        "data": data,
    }


@app.get("/fdi")
async def fdi(limit: int = Query(default=10, ge=1, le=60)):
    """Korea foreign direct investment inflows (BoP, current USD)."""
    data = await fetch_wb("BX.KLT.DINV.CD.WD", limit)
    return {
        "indicator": "Foreign Direct Investment, Net Inflows",
        "unit": "Current USD (Balance of Payments)",
        "frequency": "Annual",
        "country": "Korea, Republic of",
        "source": "World Bank",
        "data": data,
    }


@app.get("/merchandise")
async def merchandise(limit: int = Query(default=10, ge=1, le=60)):
    """Korea merchandise exports and imports (current USD)."""
    exports_data = await fetch_wb("TX.VAL.MRCH.CD.WT", limit)
    imports_data = await fetch_wb("TM.VAL.MRCH.CD.WT", limit)
    return {
        "country": "Korea, Republic of",
        "source": "World Bank",
        "frequency": "Annual",
        "unit": "Current USD",
        "exports": exports_data,
        "imports": imports_data,
    }
