# Harbourline Radar — activity record schema

Each research agent produces ONE JSON file: an array of activity records.

```json
{
  "competitor": "apm-terminals",          // slug from COMPETITORS list below
  "country": "GH",                         // ISO 3166-1 alpha-2, upper case. Use "XX" only for global/multi-country items.
  "category": "port_operations",           // one of the 6 categories below
  "event_date": "2025-03-14",              // YYYY-MM-DD; if only month known, use the 1st; if only year, YYYY-01-01 and set date_precision
  "date_precision": "day",                 // "day" | "month" | "year"
  "event_type": "concession_award",        // see EVENT TYPES
  "title": "APM Terminals wins 30-year concession for Tema Port Terminal 3 expansion",
  "summary": "2–4 sentences: what happened, with whom, size/capacity, financial terms if public, strategic significance vs DP World.",
  "location": "Tema",                      // city/port/zone name, optional
  "value_usd_m": 350,                      // deal/investment value in USD millions, null if unknown
  "capacity": "1.5m TEU/yr",               // optional free text
  "partners": ["Ghana Ports and Harbours Authority"],
  "source_name": "Reuters",
  "source_url": "https://...",
  "source_date": "2025-03-14",
  "confidence": "high"                     // high = primary/major source; medium = trade press; low = single secondary source
}
```

## CATEGORIES (exactly these slugs)
- `port_operations` — container/multipurpose/bulk/RoRo terminal concessions, acquisitions, expansions, volumes, automation
- `logistics_supply_chain` — inland logistics, warehousing, rail/road/ICD, freight forwarding, cold chain, e-commerce logistics
- `free_economic_zones` — free zones, industrial parks, SEZs, logistics parks, port-city developments
- `drydocking` — ship repair, dry docks, shipbuilding, rig repair
- `feedering` — feeder shipping services, short-sea, intra-regional container services (incl. new feeder lines/vessels)
- `marine_services` — towage, pilotage, bunkering, offshore marine, dredging support, marine agency, cruise terminal ops

## EVENT TYPES
`concession_award`, `acquisition`, `divestment`, `investment`, `expansion`, `greenfield`, `partnership_jv`, `contract`, `service_launch`, `operational_milestone`, `financing`, `regulatory`, `exit_or_loss`, `other`

## COMPETITORS
The authoritative slug list is `/home/claude/radar/data/competitors.json` (field `id`). Use only those slugs. Never record DP World's own activities (DP World, Jafza, Economic Zones World, Drydocks World, Unifeeder, P&O Maritime are all DP World — exclude). Record competitor activities worldwide, any country.

## QUALITY RULES
- Period: 1 Jan 2024 → today (Nov 2026). Prefer the most recent 18 months.
- Every record must have a real source_url you actually fetched or saw in search results. No invented URLs.
- One record per event. Do not duplicate the same event under two categories; pick the main one.
- Country = where the activity physically is. A global corporate result (annual throughput) uses "XX".
- Aim for breadth across countries, not 20 records on one port.
