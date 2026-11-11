#!/usr/bin/env python3
"""Insert activity records from JSON files into Supabase (runs in GitHub Actions).
Env: SUPABASE_URL, SUPABASE_SERVICE_KEY.  Args: one or more JSON files (SCHEMA.md format).
Duplicates (same competitor+country+date+title) are skipped by the DB unique index."""
import json, os, sys, urllib.request, urllib.error, re

URL = os.environ['SUPABASE_URL'].rstrip('/')
KEY = os.environ['SUPABASE_SERVICE_KEY']
CATS = {'port_operations','logistics_supply_chain','free_economic_zones','drydocking','feedering','marine_services'}
ET = {'concession_award','acquisition','divestment','investment','expansion','greenfield','partnership_jv','contract','service_launch','operational_milestone','financing','regulatory','exit_or_loss','other'}

def req(method, path, body=None, prefer=None):
    h = {'apikey': KEY, 'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'}
    if prefer: h['Prefer'] = prefer
    r = urllib.request.Request(URL + path, data=json.dumps(body).encode() if body is not None else None, headers=h, method=method)
    with urllib.request.urlopen(r, timeout=60) as resp:
        return resp.status, resp.read().decode()

status, body = req('GET', '/rest/v1/competitors?select=id')
comps = {c['id'] for c in json.loads(body)}

total_in = total_ok = 0
for path in sys.argv[1:]:
    with open(path, encoding='utf-8') as f:
        arr = json.load(f)
    if not isinstance(arr, list):
        print(f'{path}: not a JSON array, skipped'); continue
    rows, bad = [], []
    for i, r in enumerate(arr):
        if r.get('competitor') not in comps or r.get('category') not in CATS or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(r.get('event_date',''))) or not r.get('title') or not re.fullmatch(r'[A-Z]{2}', str(r.get('country',''))):
            bad.append(i+1); continue
        rows.append({
            'competitor_id': r['competitor'], 'country': r['country'], 'category': r['category'],
            'event_type': r.get('event_type') if r.get('event_type') in ET else 'other',
            'event_date': r['event_date'], 'date_precision': r.get('date_precision') if r.get('date_precision') in ('day','month','year') else 'day',
            'title': r['title'].strip(), 'summary': r.get('summary'), 'location': r.get('location'),
            'value_usd_m': r.get('value_usd_m'), 'capacity': r.get('capacity'), 'partners': r.get('partners') or [],
            'source_name': r.get('source_name'), 'source_url': r.get('source_url'),
            'source_date': r.get('source_date') if re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(r.get('source_date',''))) else None,
            'confidence': r.get('confidence') if r.get('confidence') in ('high','medium','low') else 'medium',
            'tags': r.get('tags') or [], 'created_by': 'weekly-import',
        })
    inserted = 0
    for k in range(0, len(rows), 200):
        chunk = rows[k:k+200]
        try:
            status, body = req('POST', '/rest/v1/activities?on_conflict=competitor_id,country,event_date,title', chunk, 'resolution=ignore-duplicates,return=representation')
            inserted += len(json.loads(body))
        except urllib.error.HTTPError as e:
            print(f'{path}: chunk {k//200} failed: {e.code} {e.read().decode()[:300]}'); sys.exit(1)
    print(f'{path}: {len(arr)} records, {len(rows)} valid, {inserted} inserted, {len(rows)-inserted} duplicates skipped' + (f', {len(bad)} invalid (#{bad[:10]})' if bad else ''))
    total_in += len(arr); total_ok += inserted
print(f'TOTAL: {total_ok} new activities inserted from {total_in} records')
