// Mobile nav toggle with aria-expanded sync
const menuBtn = document.querySelector('.menu-toggle');
const nav = document.getElementById('nav');
if (menuBtn && nav){
  menuBtn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', String(open));
  });
}

// Footer year
document.getElementById('year')?.appendChild(document.createTextNode(String(new Date().getFullYear())));

// Contact form (progressive enhancement)
const form = document.getElementById('contactForm');
if (form){
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    // Simple validation
    const name = document.getElementById('name');
    const email = document.getElementById('email');
    const message = document.getElementById('message');
    const errs = { name: '', email: '', message: '' };

    if (!name.value.trim()) errs.name = 'Please enter your name.';
    if (!email.value.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) errs.email = 'Please enter a valid email.';
    if (!message.value.trim()) errs.message = 'Please enter a message.';

    document.getElementById('name-error').textContent = errs.name;
    document.getElementById('email-error').textContent = errs.email;
    document.getElementById('message-error').textContent = errs.message;

    if (errs.name || errs.email || errs.message) return;

    // Target endpoint: Vercel (/api/contact) default
    let endpoint = form.getAttribute('action') || '/api/contact';

    // If running on Netlify, prefer Netlify function path
    if (location.hostname.endsWith('netlify.app')) {
      endpoint = '/.netlify/functions/contact';
    }

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: name.value.trim(), email: email.value.trim(), message: message.value.trim() })
      });
      const ok = res.ok;
      document.getElementById('form-success').hidden = !ok;
      document.getElementById('form-failure').hidden = ok;
      if (ok) form.reset();
    } catch (err){
      document.getElementById('form-success').hidden = true;
      document.getElementById('form-failure').hidden = false;
    }
  });
}
