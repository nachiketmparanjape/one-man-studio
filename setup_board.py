#!/usr/bin/env python3
"""One-time setup: create the public 'One-Man Studio' GitHub Project board,
add Status/Product/Sprint fields, and add every studio-mirror issue as an
item with its field values. Run once; mirror.py keeps issues fresh after."""

import json
import urllib.request

TOKEN = open('/home/hatch/.config/github-pat').read().strip()
REPO = 'nachiketmparanjape/one-man-studio'
GQL = 'https://api.github.com/graphql'


def gql(query, variables=None):
    req = urllib.request.Request(
        GQL,
        data=json.dumps({'query': query, 'variables': variables or {}}).encode(),
        method='POST',
    )
    req.add_header('Authorization', f'Bearer {TOKEN}')
    req.add_header('Content-Type', 'application/json')
    resp = json.load(urllib.request.urlopen(req))
    if 'errors' in resp:
        raise RuntimeError(json.dumps(resp['errors'], indent=1)[:2000])
    return resp['data']


def rest(url, data=None, method='GET'):
    req = urllib.request.Request(
        f'https://api.github.com{url}',
        data=json.dumps(data).encode() if data is not None else None,
        method=method,
    )
    req.add_header('Authorization', f'Bearer {TOKEN}')
    req.add_header('Accept', 'application/vnd.github+json')
    return json.load(urllib.request.urlopen(req))


# 1. create the project
viewer = gql('query { viewer { id } }')['viewer']['id']
proj = gql('''mutation($owner: ID!) {
  createProjectV2(input: {ownerId: $owner, title: "One-Man Studio — paper cuts"}) {
    projectV2 { id number url }
  }
}''', {'owner': viewer})['createProjectV2']['projectV2']
pid = proj['id']
print('project:', proj['url'])

# 2. public
gql('mutation($p: ID!) { updateProjectV2(input: {projectId: $p, public: true}) '
    '{ projectV2 { id } } }', {'p': pid})
print('made public')

# 3. fields
status_field = gql('''mutation($p: ID!) {
  createProjectV2Field(input: {projectId: $p, dataType: SINGLE_SELECT,
    name: "Status",
    singleSelectOptions: [
      {name: "Planned", color: GRAY, description: "Committed or backlog"},
      {name: "In Progress", color: YELLOW, description: "In the active sprint"},
      {name: "Shipped", color: GREEN, description: "Live"},
      {name: "Parked", color: PURPLE, description: "Deliberately on hold"}
    ]}) { projectV2Field { id } }
}''', {'p': pid})['createProjectV2Field']['projectV2Field']['id']

product_field = gql('''mutation($p: ID!) {
  createProjectV2Field(input: {projectId: $p, dataType: TEXT, name: "Product"})
  { projectV2Field { id } }
}''', {'p': pid})['createProjectV2Field']['projectV2Field']['id']

sprint_field = gql('''mutation($p: ID!) {
  createProjectV2Field(input: {projectId: $p, dataType: TEXT, name: "Sprint"})
  { projectV2Field { id } }
}''', {'p': pid})['createProjectV2Field']['projectV2Field']['id']

# option ids for the Status field
fields = gql('''query($p: ID!) {
  node(id: $p) { ... on ProjectV2 {
    fields(first: 20) { nodes {
      ... on ProjectV2SingleSelectField {
        id name options { id name } } } } } } }''', {'p': pid})
opt_ids = {}
for f in fields['node']['fields']['nodes']:
    if f.get('name') == 'Status':
        for o in f['options']:
            opt_ids[o['name']] = o['id']
print('status options:', opt_ids)

# 4. issues -> (board status, product, sprint)
import re
issues = []
page = 1
while True:
    batch = rest(f'/repos/{REPO}/issues?labels=studio-mirror&state=all'
                 f'&per_page=100&page={page}')
    if not batch:
        break
    issues.extend(batch)
    page += 1
print(f'{len(issues)} mirror issues')

# derive board status the same way mirror.py does (single source would be
# nicer; keep in sync manually — both read the same markdown)
import sys
sys.path.insert(0, '/home/hatch/workspace/studio')
import mirror as M

cards = {}
for slug in sorted(__import__('os').listdir('/home/hatch/workspace/studio/products')):
    pdir = f'/home/hatch/workspace/studio/products/{slug}'
    bl = f'{pdir}/BACKLOG.md'
    if not __import__('os').path.exists(bl):
        continue
    pname = M.product_name(bl)
    sprints_dir = f'{pdir}/sprints'
    slabels = sorted(__import__('os').listdir(sprints_dir)) if __import__('os').path.isdir(sprints_dir) else []
    per = {}
    for s in slabels:
        plan = f'{sprints_dir}/{s}/PLAN.md'
        if __import__('os').path.exists(plan):
            sl = 'Sprint ' + s.split('-', 1)[1].lstrip('0')
            for c in M.parse_plan_cards(plan, sl):
                per[c['key']] = c
    latest = ('Sprint ' + slabels[-1].split('-', 1)[1].lstrip('0')) if slabels else ''
    for c in M.parse_backlog_cards(bl, set(per)):
        per[c['key']] = c
    shipped = M.shipped_ids(pdir)
    for key, c in per.items():
        blob = (c['header'] + '\n' + c['status'] + '\n' + '\n'.join(c['body']))
        if key in shipped or re.search(r'\b(shipped|SHIPPED|DONE|CLOSED)\b', blob):
            board = 'Shipped'
        elif 'parked' in blob.lower():
            board = 'Parked'
        elif c['sprint'] == latest and latest:
            board = 'In Progress'
        else:
            board = 'Planned'
        cards[(key, pname.lower())] = (board, pname, c['sprint'])

for i in issues:
    m = re.match(r'^((?:PC|BUG)-\d+).*?\(([^),]+)', i['title'])
    key = (m.group(1), m.group(2).strip().lower()) if m else None
    info = cards.get(key)
    if not info:
        print('no card for issue:', i['title'])
        continue
    board, product, sprint = info
    item = gql('''mutation($p: ID!, $c: ID!) {
      addProjectV2ItemById(input: {projectId: $p, contentId: $c}) {
        item { id } } }''',
               {'p': pid, 'c': i['node_id']})['addProjectV2ItemById']['item']['id']
    gql('''mutation($p: ID!, $it: ID!, $f: ID!, $o: String!) {
      updateProjectV2ItemFieldValue(input: {projectId: $p, itemId: $it,
        fieldId: $f, value: {singleSelectOptionId: $o}}) {
        projectV2Item { id } } }''',
        {'p': pid, 'it': item, 'f': status_field, 'o': opt_ids[board]})
    for f, val in ((product_field, product), (sprint_field, sprint)):
        gql('''mutation($p: ID!, $it: ID!, $f: ID!, $v: String!) {
          updateProjectV2ItemFieldValue(input: {projectId: $p, itemId: $it,
            fieldId: $f, value: {text: $v}}) { projectV2Item { id } } }''',
            {'p': pid, 'it': item, 'f': f, 'v': val})
    print(f"added #{i['number']} [{board}] {i['title'][:45]}")

print('\nboard ready:', proj['url'])
