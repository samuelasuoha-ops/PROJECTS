import { test, expect } from '@playwright/test';

test.describe('Front-end & API Integration', () => {
  test('login -> load items -> add item', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: /welcome/i })).toBeVisible();

    await page.getByLabel(/email/i).fill('demo@user.com');
    await page.getByLabel(/password/i).fill('password123');
    await page.getByRole('button', { name: /sign in/i }).click();

    await expect(page.getByText(/Signed in as/i)).toBeVisible();

    await page.getByRole('button', { name: /load items/i }).click();
    const list = page.getByRole('list', { name: /items/i });
    await expect(list).toBeVisible();
    const before = await list.getByRole('listitem').count();

    await page.getByLabel(/item name/i).fill('E2E New Item');
    await page.getByRole('button', { name: /add item/i }).click();
    await expect(list.getByText('E2E New Item')).toBeVisible();
    const after = await list.getByRole('listitem').count();
    expect(after).toBeGreaterThanOrEqual(before + 1);
  });

  test('contact form submission', async ({ page }) => {
    await page.goto('/contact.html');
    await page.getByLabel(/^name$/i).fill('Playwright Tester');
    await page.getByLabel(/^email$/i).fill('tester@example.com');
    await page.getByLabel(/message/i).fill('Hello from automated test!');
    await page.getByRole('button', { name: /send/i }).click();
    await expect(page.getByText(/submitted successfully|sent \(dev mode\)/i)).toBeVisible();
  });
});
