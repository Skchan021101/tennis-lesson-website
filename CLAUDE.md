# Working on this repo

The public website for Coach Soon Keat (Chan Soon Keat, 陈顺杰), a tennis
coach in Singapore: tennis lessons near Kovan, in English and 中文. Its one
job is to be found on Google and get a visitor to tap WhatsApp.

The coach's Telegram booking bot is a **separate** private repository
(`Tennis-telebot`). Nothing here is shared with it, and nothing from it
belongs here, least of all its `CLAUDE.md`, which holds server details.

## Still to build

The site does not exist yet. `BUILD_PROMPT.md` is the complete spec: copy,
design, SEO, tests and the coach's setup steps. Build from it and nothing
else. When the site is built, replace this section with what exists.

## Rules that do not bend

- **Everything in `site/` is published to the internet** by Cloudflare
  Pages, on every merge to `main`, within a minute or two. Merging here
  *is* deploying, unlike the bot. Nothing private, no notes, no README,
  and no source files belong in `site/`.
- **Never invent facts about the coach**: no made-up reviews, ratings,
  student counts, ages, addresses or titles. If the copy needs a fact nobody
  has given, ask for it in the PR.
- **Prices must match the bot.** The site shows $100 / $70pp / $50pp. If a
  price changes here, the coach must also `/setrate` the bot, or a client is
  quoted two prices.
- Never write "N years of experience"; write "coaching since 2021". A count
  of years goes stale every January.
- No JavaScript, no trackers, no cookie-setting scripts. The CSP in
  `site/_headers` depends on it.
- The coach reads commits: end each one that changes the site with a
  `Try:` line saying what to open and tap, in plain words.
