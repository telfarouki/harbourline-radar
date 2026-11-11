# Harbourline Radar — weekly update procedure (for the scheduled task)

Goal: find the past 10 days of competitor activity and add it to the Radar database via the repo.

1. Clone github.com/telfarouki/harbourline-radar (add_repo with push access, then git clone). Read research/SCHEMA.md and competitors.json.
2. Run 7 research agents in parallel (same groups as the seed): (g1) apm-terminals, psa, hutchison-ports · (g2) cosco-shipping-ports, china-merchants-ports, cma-cgm · (g3) msc-til, ictsi, eurogate · (g4) ad-ports, agl-bollore, arise-iip · (g5) adani-ports, yilport, gulftainer, rsgt, tanger-med, sohar, port-antwerp-bruges-intl · (g6) svitzer, boluda, boskalis-smit, damen, asry, n-kom, cochin-shipyard, zamil-offshore, imi-saudi · (g7) maersk-logistics, dhl, agility, kuehne-nagel, ceva-logistics.
   Each agent: WebSearch "<competitor> news" restricted to the last 10 days (use the current date), across the 6 categories; only events dated within the window; every record with a real source_url; output records exactly per SCHEMA.md to a temp file. Target: every real event, no padding — 0 records for a quiet competitor is fine.
3. Merge, validate (slugs, ISO2, categories, dates, URLs), remove duplicates within the file, and write weekly/YYYY-Www.json (ISO week of today). If the file for this week already exists, overwrite it.
4. git add weekly/<file>; commit "Weekly update <week>"; git push origin main. The repo's Action then inserts the records into Supabase automatically.
5. Final report (2–4 lines): number of records, top 5 most significant events, any competitor the search could not cover. Send a push notification with the count.
If push is refused: send the JSON file to the user and say they can upload it to the weekly/ folder of the repo.
