# Northline Finds — storefront

A mobile-first static storefront. No build tools, no backend — just HTML/CSS/JS
you can host anywhere (GitHub Pages, Netlify, Vercel, any static host).

## Rebuild the catalog

```sh
cd ~/workspace/dropship/store
python3 build.py
```

This reads `../research/products.json` and regenerates:
- `index.html` — hero, category filter, product grid
- `products/<id>.html` — one page per product
- `cart.html` — checkout page
- `assets/js/catalog.js` — product data for the JS cart
- `assets/js/products.js` — store config (Stripe links preserved)

Use `python3 build.py --products path/to/other.json` to build from a different file.

## Add Stripe Payment Links

1. Open `assets/js/products.js`
2. Paste each product's Stripe Payment Link into its `stripeLinks` entry:
   ```js
   stripeLinks: {
     "led-strip-lights": "https://buy.stripe.com/abc123...",
   }
   ```
3. Re-run `python3 build.py`

Until a link is filled in, that product's buy button becomes an
"Email us to order" button (mailto to the contact email) — no dead buttons.

## Product images

Put one photo per product in `assets/img/` named after the product id:
`assets/img/<product-id>.jpg` (also accepts `.jpeg`, `.png`, `.webp`).
Products without a photo get a clean branded placeholder automatically.

## Rename the brand

Change `STORE_NAME` at the top of `build.py`, re-run it, and update the
`storeName` in `assets/js/products.js`.

## Edit page copy

About / FAQ / Shipping / Returns / Contact live in `content/` as plain HTML
fragments — edit them, then re-run `build.py`.

## How checkout works

The cart (localStorage) lives in `assets/js/app.js`. Each item checks out
through its own Stripe Payment Link, opened in a new tab. Stripe handles the
payment; this site never touches card details.
