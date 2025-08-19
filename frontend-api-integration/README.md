# Front-end & API Integration (Complete)

Responsive UI with **semantic HTML**, **modern CSS**, and **vanilla JavaScript**.  
Consumes **REST APIs** for **authentication** and **data rendering**. Includes **form validation**, **serverless contact handler**, **unit tests (Jest)**, **E2E tests (Playwright)**, and **GitHub Actions CI**.

## Features
- Login → JWT stored in localStorage → fetch protected resources
- Items list: load & add items
- Contact form wired to **Node.js serverless function** (reused locally)
- Responsive layout (Grid/Flex), dark-friendly, accessible forms
- Unit tests (Jest) + E2E tests (Playwright)
- Dev server (Express) serves static site and API

## Quick start (local)
```bash
npm i
npm run prepare          # installs Playwright browsers
npm run dev              # http://localhost:3000
```
Demo creds: `demo@user.com` / `password123`

## Tests
```bash
npm test                 # Jest unit tests
npm run test:e2e         # Playwright E2E (starts dev server automatically)
```

## Deploying the serverless function
The contact handler is in `serverless/contact.js` (Netlify/AWS Lambda style).  
On Netlify, it would be accessible at `/.netlify/functions/contact`. For this demo, the dev server exposes it at `/api/contact`.

## Project structure
```
frontend-api-integration-full/
  index.html
  blog.html
  contact.html
  css/styles.css
  js/app.js
  js/validation.js
  serverless/contact.js
  server/dev-server.js
  __tests__/validation.spec.js
  tests/e2e/app.spec.ts
  playwright.config.ts
  .github/workflows/ci.yml
  package.json
  README.md
```
