# Harbourline Radar — setup guide

Competitor activity monitor for DP World's markets: **port operations · logistics & supply chain · free & economic zones · drydocking · feedering · marine services**, recorded historically, worldwide, country by country.

Same model as Harbourline Atlas: public GitHub Pages site + Supabase database, access-request form, admin approval, sign-in by 6-digit e-mail code.

## What is in this package

| File | Purpose |
|---|---|
| `index.html` | The Radar (built from `src/index.template.html`) |
| `admin.html` | Admin: approve access requests, manage users, add/edit activities and competitors, import JSON |
| `demo.html` | Same interface with 6 fake records and no database — for preview only, do not upload |
| `sql/01_schema.sql` | Tables, access model, RLS, bootstrap admin — **run first** |
| `sql/02_email_notification.sql` | Optional: e-mail on each access request via Resend (same as Atlas) |
| `data/competitors.json` | 33 competitors in 4 groups — import first |
| `data/records_*.json` | Research-seeded activities 2024–2026 — import after competitors |
| `data/countries.json` | Worldwide ISO list used by the pages |
| `build.py` + `config.json` | Injects your Supabase URL/key into the pages |
| `.github/workflows/keepalive.yml` | Pings Supabase twice a week so the free project is not paused |
| `research/SCHEMA.md`, `research/AGENT_PROMPT.md` | Record format and the prompt used by research agents — reuse them for future waves |

## Step-by-step

### A. Supabase (10 min)
1. supabase.com → **New project** → name `harbourline-radar`, region Frankfurt (or same as Atlas). Save the database password.
2. **Authentication → Providers → Email**: keep Email enabled; **Confirm email ON**; set **OTP length = 6** and **OTP expiry = 3600**.
   Authentication → Email Templates → *Magic Link*: replace the body with `<p>Your Harbourline Radar code: <b>{{ .Token }}</b></p>` (same as the Atlas).
3. **Authentication → URL Configuration**: Site URL = `https://telfarouki.github.io/harbourline-radar` (change later when you have a domain).
4. **Project Settings → Authentication → SMTP**: copy the Gmail SMTP settings you used for the Atlas (the Supabase default sender has a low hourly limit).
5. **SQL Editor → New query** → paste `sql/01_schema.sql` → Run. Expect `Success. No rows returned`.
   Your e-mail is bootstrapped as **admin**.
6. (Optional) **Project Settings → Vault** → secret `resend_api_key` = your Resend key, then run `sql/02_email_notification.sql`.
7. **Project Settings → API**: copy *Project URL* and *anon public* key.

### B. Build the pages (2 min)
1. Copy `config.example.json` to `config.json`, paste the URL and anon key.
2. Run `python3 build.py` → regenerates `index.html` and `admin.html`.
   (No Python? Open the two HTML files in a text editor and replace `__SUPABASE_URL__` and `__SUPABASE_ANON_KEY__` by hand — once in each file.)

### C. GitHub Pages (5 min)
1. github.com → **New repository** `harbourline-radar`, Public.
2. Upload (Add file → Upload files): `index.html`, `admin.html`, `README.md`, the `.github/workflows/keepalive.yml` (create the folder path when uploading), and the `data/` folder.
3. Settings → Pages → Source: *Deploy from a branch* → `main` / root → Save. The site appears at `https://telfarouki.github.io/harbourline-radar/`.
4. Settings → Secrets and variables → Actions → add `SUPABASE_URL` and `SUPABASE_ANON_KEY`; then Actions → *Supabase keepalive* → Run workflow.

### D. Load the data (5 min)
1. Open `…/admin.html`, sign in with your e-mail + code.
2. Tab **Import JSON** → choose `data/competitors.json` → *Validate & import*.
3. Same tab → select **all** `data/records_*.json` files at once → *Validate & import*. Duplicates are skipped automatically, so re-importing is safe.
4. Open `index.html` — pick a country, tick activities, filter by competitor.

### E. Custom domain (when wanted)
Same as the Atlas: buy e.g. `harbourlineradar.com` at Namecheap, add it in repo Settings → Pages → Custom domain, enforce HTTPS, then update the Supabase Site URL and the admin link in `02_email_notification.sql`.

## Daily use
- **Viewers** read everything; **editors** can add/edit activities (admin → Users → role); **admins** also approve requests.
- Add a single activity in admin → *Activities*; the form has every field of the schema.
- Bulk update: run a new research wave with `research/AGENT_PROMPT.md` (one agent per competitor group, output `records_<tag>.json`), then import. Dates and titles identical to an existing record are skipped.
- Share a view: filter, then *Copy link* — the URL carries country, activities, competitor and period.
- Export: *Export CSV* (current filter) or *Print / PDF*.

## Data model (short)
`competitors(id slug, name, group, hq, website)` ← `activities(competitor_id, country ISO2, category, event_date, date_precision, event_type, title, summary, location, value_usd_m, capacity, partners[], source_name, source_url, source_date, confidence, tags[])`.
Categories: `port_operations`, `logistics_supply_chain`, `free_economic_zones`, `drydocking`, `feedering`, `marine_services`. Country `XX` = global / multi-country.

## Coverage of the seed data (2 Nov 2026)
377 records · 29 competitors · 80 countries. By activity: port operations 200, logistics 50, marine services 50, drydocking 40, feedering 19, free/economic zones 18.
Thin or missing (search budget ran out — to top up in a follow-up wave with `research/AGENT_PROMPT.md`): **AGL/Bolloré, Arise IIP, Kuehne+Nagel, CEVA** (0 records), China Merchants Ports (6), RSGT (4), IMI (4), N-KOM/QSTS (3), Sohar (2), Zamil Offshore (1). 27 records are marked `low` confidence (single secondary source) — worth a second look in admin before relying on them.
