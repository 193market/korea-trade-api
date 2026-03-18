# Korea Trade & Export API

Real-time Korea trade statistics powered by **World Bank Open Data**.

**Live API**: https://korea-trade-api.vercel.app
**RapidAPI**: [Korea Trade & Export API](https://rapidapi.com/193market/api/korea-trade-api)

---

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info & endpoint list |
| `GET /summary` | All indicators (latest snapshot) |
| `GET /exports` | Exports of goods & services (% of GDP) |
| `GET /imports` | Imports of goods & services (% of GDP) |
| `GET /balance` | Current account balance (USD) |
| `GET /tech-exports` | High-technology exports (% of manufactured) |
| `GET /trade-gdp` | Total trade as % of GDP |
| `GET /fdi` | Foreign direct investment inflows (USD) |
| `GET /merchandise` | Merchandise exports & imports (USD) |

All endpoints accept `?limit=N` (default 10, max 60).

---

## Example

```bash
curl https://korea-trade-api.vercel.app/exports?limit=5
```

```json
{
  "indicator": "Exports of Goods and Services",
  "unit": "% of GDP",
  "frequency": "Annual",
  "country": "Korea, Republic of",
  "source": "World Bank",
  "data": [
    {"year": "2022", "value": 44.87},
    {"year": "2021", "value": 40.52},
    {"year": "2020", "value": 36.22},
    {"year": "2019", "value": 39.36},
    {"year": "2018", "value": 42.16}
  ]
}
```

---

## Data Source

- **Provider**: World Bank Open Data (data.worldbank.org)
- **License**: Creative Commons Attribution 4.0 (CC BY 4.0)
- **Update frequency**: Annual
- **No API key required**

---

## Pricing (RapidAPI)

| Plan | Requests/month | Price |
|------|---------------|-------|
| BASIC | 100 | Free |
| PRO | 10,000 | $9/month |
| ULTRA | Unlimited | $29/month |

---

## Deploy (Vercel)

```bash
npm i -g vercel
vercel --prod
```

No environment variables required (World Bank API is public).

---

## By GlobalData Store

- GitHub: [193market](https://github.com/193market)
- Email: 193market@gmail.com
