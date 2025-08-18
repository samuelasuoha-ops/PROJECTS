import os, sys, datetime, html

def main(p='output'):
    os.makedirs(p, exist_ok=True)
    files = sorted([f for f in os.listdir(p) if f.lower().endswith(('.png','.jpg','.jpeg','.gif'))])
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    out = os.path.join(p, 'index.html')
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write('<!doctype html><meta charset="utf-8">')
        fh.write('<title>Weather Charts</title>')
        fh.write('<style>body{font-family:system-ui,Arial,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem}h1{margin-bottom:.25rem}figure{margin:1.5rem 0}figcaption{color:#555}</style>')
        fh.write(f'<h1>Weather Charts</h1><p>Last updated: {now}</p>')
        if not files:
            fh.write('<p>No charts found.</p>')
        for f in files:
            s = html.escape(f)
            fh.write(f'<figure><img src="{s}" alt="{s}" style="width:100%;max-width:900px"><figcaption>{s}</figcaption></figure>')
    print(f"Generated {out} with {len(files)} images.")

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'output')
