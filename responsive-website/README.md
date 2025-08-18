# Responsive Website Starter (with Blog & Serverless Contact)

Accessible, performant and responsive site built with **semantic HTML**, **modern CSS**, and **vanilla JS**.
Now includes:
- **Blog/Article page template** (`blog.html` + sample in `/articles/`)
- **Contact form** wired to a **serverless endpoint**
  - Vercel-style function: `/api/contact.js`
  - Netlify function: `/netlify/functions/contact.js`

## Run locally
```bash
# any static server works:
python -m http.server 5500
# then open http://localhost:5500
```

## Deploy options

### Vercel
- Keep `/api/contact.js` (Node env).
- Deploy with Vercel. The contact form posts to `/api/contact` automatically.

### Netlify
- Keep `/netlify/functions/contact.js`.
- In Netlify dashboard, set **Functions directory** to `netlify/functions`.
- Update `form action` to `/.netlify/functions/contact` (already handled by JS).

## Environment variables (both platforms)
- `CONTACT_TO` — destination email (if you forward via provider) or Slack webhook URL if you adapt the function.
- For demo, the function simply logs and returns a success JSON.

> NOTE: Don’t put secrets in the client. Set them in your hosting platform dashboard.

## Structure
```
.
├── index.html
├── blog.html
├── articles/
│   └── sample-article.html
├── css/
│   └── styles.css
├── js/
│   └── script.js
├── api/
│   └── contact.js            # Vercel
├── netlify/
│   └── functions/
│       └── contact.js        # Netlify
├── manifest.webmanifest
├── favicon.svg
├── robots.txt
└── README.md
```

