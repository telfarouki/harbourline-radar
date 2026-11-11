# Harbourline Radar — weekly update procedure (for the scheduled tasks)

Goal: find the past 10 days of competitor activity and add it to the Radar database via the repo.

The update is split in TWO scheduled runs so that each gets its own web-search budget (200 WebSearch calls per run, shared by every agent in the run):
- **Run A — Wednesday 00:00 Dubai**: groups g1–g4 (14 competitors), 4 agents, ≤45 searches each → `weekly/YYYY-Www-a.json`, commit "Weekly update YYYY-Www A".
- **Run B — Saturday 00:00 Dubai**: groups g5–g7 (21 competitors), 3 agents, ≤60 searches each → `weekly/YYYY-Www-b.json`, commit "Weekly update YYYY-Www B".

1. Clone github.com/telfarouki/harbourline-radar (add_repo with push access if available, then git clone; `git pull` if already cloned). Read research/SCHEMA.md and competitors.json.
2. Run the run's research agents in parallel. Groups: (g1) apm-terminals, psa, hutchison-ports · (g2) cosco-shipping-ports, china-merchants-ports, cma-cgm · (g3) msc-til, ictsi, eurogate · (g4) ad-ports, agl-bollore, arise-iip · (g5) adani-ports, yilport, gulftainer, rsgt, tanger-med, sohar, port-antwerp-bruges-intl · (g6) svitzer, boluda, boskalis-smit, damen, asry, n-kom, cochin-shipyard, zamil-offshore, imi-saudi · (g7) maersk-logistics, dhl, agility, kuehne-nagel, ceva-logistics.
   Each agent: WebSearch "<competitor> news <month year>" plus 1–2 topical queries per competitor, restricted to the last 10 days (use the current Dubai date), across the 6 categories; stay within its search cap and use WebFetch of company newsrooms/trade press freely (fetches do not count against the search budget); only events dated within the window (an older event reported this week does not count); every record with a real source_url; output records exactly per SCHEMA.md to a temp file. Target: every real event, no padding — 0 records for a quiet competitor is fine. One record per event: when two competitors share one event (e.g. a Maersk/APM Terminals rail link), record it once under the main actor.
   Known trap: indiaseatradenews.com and similar sites show the crawl date in search snippets, not the article date — verify dates on the page.
3. Merge, validate (slugs, ISO2, categories, event types, dates inside the window, URLs), remove duplicates within the file, and write the run's file (ISO week of today's Dubai date). If the file already exists, overwrite it.
4. git add weekly/<file>; commit with the run's message; git push origin main. The repo's Action then inserts the records into Supabase automatically (duplicates skipped). Wait ~60 s and check `gh run list --repo telfarouki/harbourline-radar --limit 1`.
5. Final report (2–4 lines): number of records, top 5 most significant events, any competitor the search could not cover. Send a push notification with the count.
If push is refused: send the JSON file to the user and say they can upload it to the weekly/ folder of the repo.
