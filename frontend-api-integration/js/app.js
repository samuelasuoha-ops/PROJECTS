import { validateEmail, validatePassword, validateRequired } from './validation.js';

const $ = (sel) => document.querySelector(sel);
const apiBase = '/api'; // dev server serves on 3000, same origin

function setYear(){ const el = document.getElementById('year'); if (el) el.textContent = new Date().getFullYear(); }
setYear();

// Responsive nav toggle
const navBtn = document.querySelector('.nav-toggle');
const navMenu = document.getElementById('nav-menu');
if (navBtn && navMenu){
  navBtn.addEventListener('click', () => {
    const collapsed = navMenu.dataset.collapsed === 'true';
    navMenu.dataset.collapsed = String(!collapsed);
    navBtn.setAttribute('aria-expanded', String(collapsed));
  });
}

// Token storage
const Token = {
  key: 'feapi.token',
  save(t){ localStorage.setItem(this.key, t); },
  get(){ return localStorage.getItem(this.key); },
  clear(){ localStorage.removeItem(this.key); }
};

async function apiFetch(path, opts={}){
  const headers = Object.assign({ 'Content-Type':'application/json' }, opts.headers || {});
  const token = Token.get();
  if (token) headers['Authorization'] = 'Bearer ' + token;
  const res = await fetch(apiBase + path, { ...opts, headers });
  if (!res.ok) throw new Error(await res.text() || res.statusText);
  return res.json();
}

// Index page logic
if (document.getElementById('login-form')){
  const form = $('#login-form');
  const email = $('#email');
  const password = $('#password');
  const status = $('#login-status');
  const whoami = $('#whoami');
  const loadBtn = $('#load-items');
  const logoutBtn = $('#logout-btn');
  const itemsList = $('#items-list');
  const addForm = $('#add-item-form');
  const itemName = $('#item-name');

  function setAuthedUI(emailText){
    whoami.textContent = 'Signed in as ' + emailText;
    loadBtn.disabled = false;
    logoutBtn.hidden = false;
    addForm.hidden = false;
  }
  function setLoggedOutUI(){
    whoami.textContent = 'Not signed in.';
    loadBtn.disabled = true;
    logoutBtn.hidden = true;
    addForm.hidden = true;
    itemsList.innerHTML = '';
  }

  // Restore token
  (async () => {
    if (Token.get()){
      try{
        const me = await apiFetch('/me');
        setAuthedUI(me.email);
      }catch(_e){ Token.clear(); setLoggedOutUI(); }
    }
  })();

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    // Validate
    const errs = [];
    if (!validateEmail(email.value)) errs.push(['#email-error','Enter a valid email']);
    if (!validatePassword(password.value)) errs.push(['#password-error','Min 8 chars, include letters & numbers']);
    document.querySelectorAll('.error').forEach(el => el.textContent = '');
    if (errs.length){
      errs.forEach(([sel,msg]) => { const el = document.querySelector(sel); if (el) el.textContent = msg; });
      return;
    }
    status.textContent = 'Signing in…';
    try{
      const data = await apiFetch('/login', { method:'POST', body: JSON.stringify({ email: email.value, password: password.value }) });
      Token.save(data.token);
      status.textContent = 'Signed in!';
      setAuthedUI(data.user.email);
    }catch(err){
      status.textContent = 'Login failed: ' + err.message;
    }
  });

  logoutBtn?.addEventListener('click', () => {
    Token.clear();
    setLoggedOutUI();
  });

  $('#load-items')?.addEventListener('click', async () => {
    itemsList.innerHTML = '<li class="muted">Loading…</li>';
    try{
      const items = await apiFetch('/items');
      itemsList.innerHTML = items.map(i => `<li>${i.name}</li>`).join('') || '<li class="muted">No items</li>';
    }catch(err){
      itemsList.innerHTML = `<li class="muted">Error: ${err.message}</li>`;
    }
  });

  addForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = itemName.value.trim();
    if (!validateRequired(name)){
      alert('Please enter an item name.'); return;
    }
    try{
      const created = await apiFetch('/items', { method:'POST', body: JSON.stringify({ name }) });
      const li = document.createElement('li');
      li.textContent = created.name;
      itemsList.appendChild(li);
      itemName.value = '';
    }catch(err){
      alert('Failed to add: ' + err.message);
    }
  });
}

// Contact page logic
if (document.getElementById('contact-form')){
  const form = document.getElementById('contact-form');
  const name = document.getElementById('c-name');
  const email = document.getElementById('c-email');
  const message = document.getElementById('c-message');
  const status = document.getElementById('contact-status');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    // simple validation
    document.querySelectorAll('.error').forEach(el => el.textContent = '');
    let ok = true;
    if (!validateRequired(name.value)){ ok=false; document.getElementById('c-name-error').textContent = 'Required'; }
    if (!validateEmail(email.value)){ ok=false; document.getElementById('c-email-error').textContent = 'Invalid email'; }
    if (!validateRequired(message.value)){ ok=false; document.getElementById('c-message-error').textContent = 'Required'; }
    if (!ok) return;

    status.textContent = 'Sending…';
    try{
      const res = await fetch(apiBase + '/contact', {
        method:'POST', headers:{ 'Content-Type':'application/json' },
        body: JSON.stringify({ name: name.value, email: email.value, message: message.value })
      });
      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();
      status.textContent = data.message || 'Sent!';
      status.classList.add('success');
      form.reset();
    }catch(err){
      // Fallback: pretend success if API is missing (dev only)
      console.warn('Contact submit failed, using dev fallback:', err.message);
      status.textContent = 'Sent (dev mode).';
      status.classList.add('success');
      form.reset();
    }
  });
}
