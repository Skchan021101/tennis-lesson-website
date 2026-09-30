# Build Prompt: Coach Soon Keat's tennis website

> **How to use this file:** open a fresh Sonnet session on this repository and
> say: *"Read `BUILD_PROMPT.md` and build it."* Everything the website
> needs is in this file and in `site/img/`. You do not need the original
> flyer PDF.

---

You are building a small, fast, bilingual (English + 简体中文) marketing
website for a one-person tennis coaching business in Singapore. It has one
job: **when someone searches "tennis lessons near Kovan", "tennis lessons for
kids Kovan", "高文 网球课" or just "tennis lessons", they should find this
site, trust the coach within ten seconds, and tap a button that opens
WhatsApp.**

Read `CLAUDE.md` first. This repository holds **only the website**. The
coach's Telegram booking bot lives in a separate private repository
(`Tennis-telebot`) and shares no code with this one. Do not try to link
the two, and do not copy anything from the bot repository.

Every decision below has already been made with the coach. Do not add
features, pages, frameworks or claims beyond this spec. **Never invent facts
about the coach**: no made-up reviews, student numbers, star ratings,
addresses or qualifications. All copy is written for you in section 6. Use it
word for word unless it breaks the layout, in which case shorten it without
changing any facts.

---

## 1. Decisions already made (do not re-open)

| Topic | Decision |
|---|---|
| Prices | **The flyer prices**: 1-on-1 **$100/hr**; 2 people **$70/hr per person**; group of 4 **$50/hr per person**, 1-hour class. All SGD. |
| Where lessons happen | **Any court the student books** in Kovan, Hougang, Serangoon and Bishan. The coach travels to it. The student books and pays for the court. No NTU on the website. |
| Main call to action | **WhatsApp** `+65 8884 1034`, with a message already typed. Phone and email are secondary. **No Telegram bot link, no contact form.** |
| Domain | **Free address only**: Cloudflare Pages `https://<project>.pages.dev`. Default project name `kovan-tennis`, so the site is `https://kovan-tennis.pages.dev`. |
| Languages | **English + 简体中文**, as two full sets of pages linked with `hreflang`. Switching language is a plain link. **Never redirect automatically by browser language.** |
| Kids | **Yes, children are taught.** The coach has **not** given a minimum age, so the site says "kids and teenagers" and never names an age. |
| Google Business Profile | The coach has none. Section 10 is a step-by-step setup guide for them. It is not code. |
| Extra content | **None for now.** No reviews section, no gallery. Use only the two photos in `site/img/`. Do not add "coming soon" placeholders on the live site. |

---

## 2. Tech stack: plain static files, nothing to build

- Hand-written **HTML5 + one CSS file**. **No JavaScript at all**: FAQs and
  the mobile menu use `<details>`, navigation uses anchor links, and the
  header's scroll effect uses CSS scroll-driven animation (section 4.3). No framework, no bundler, no
  npm, no `package.json`, no Tailwind, no jQuery.
- Why: the coach cannot maintain a build chain, Cloudflare Pages serves a
  folder of files for free with nothing to build, and a page with no
  JavaScript and two photos loads almost instantly on a phone. Speed is a
  Google ranking factor.
- Fonts: **Playfair Display 700** for English headings, from Google Fonts;
  the system font stack for everything else (details in section 4.1).
- **No third-party scripts**: no Google Analytics, no Facebook pixel, no
  embedded Google Map (an iframe map adds about 1 MB and slows the page).
  Visitor numbers come from Cloudflare Web Analytics, which the coach turns
  on in the Cloudflare dashboard with one switch. It needs no code, sets no
  cookies and needs no cookie banner.

---

## 3. File layout

Everything the public sees lives in `site/`, which Cloudflare publishes
as the site root. **Nothing else may go in `site/`**: no README, no notes
and no source files, because everything in it becomes a public URL.

```
site/
  index.html                  EN home          /
  kids/index.html             EN kids page     /kids/
  zh/index.html               中文 home        /zh/
  zh/kids/index.html          中文 kids page   /zh/kids/
  404.html                    bilingual "page not found" (Cloudflare serves it automatically)
  css/site.css                the only stylesheet
  img/coach-forehand.jpg      ALREADY IN REPO: 768x513, coach mid-forehand at night, NTU shirt
  img/malaysia-junior-davis-cup.jpg   ALREADY IN REPO: 437x405, Malaysia Junior Davis Cup team photo
  img/favicon.svg             you create it: a simple tennis ball (yellow-green circle with a white seam curve)
  robots.txt
  sitemap.xml
  _headers                    Cloudflare Pages headers file (section 8)

docs/design-reference/        ALREADY IN REPO: 5 screenshots of the design the coach picked (section 4.0)
docs/website.md               for the coach: how to change a price, how it deploys (section 11)
tests/test_website.py         guards (section 9)
.github/workflows/ci.yml      runs ruff + pytest on every push and PR (section 9)
CLAUDE.md                     already in the repo: update it (section 11)
```

Do not use the flyer's racquet-and-balls photo. It is a stock image with an
unknown licence and is not in the repo.

---

## 4. Design

### 4.0 The reference: look at it first

The coach picked a reference design. Screenshots are in
`docs/design-reference/` (a plumbing company's template, "AquaFlow"). Open
all five before writing any CSS. **Match its look and structure, not its
content.** None of its text, claims ("10,000+ homeowners", "4.9★ rating",
"5-year warranty") or photos come across; the tennis copy is in section 6.

What makes that design work, and must survive into this site:

| Reference element | Screenshot | Becomes, here |
|---|---|---|
| Full-bleed hero photo under a dark navy gradient, text on the left | 1 | `coach-forehand.jpg` under the same gradient. The night-time photo is already dark, so it suits this well. |
| Header over the hero: rounded blue square logo tile, serif wordmark, hamburger on the right | 1 | Tile with a white tennis-ball glyph, wordmark "Coach Soon Keat" / "陈顺杰教练". |
| Glassy pill badge above the headline ("TRUSTED BY…") | 1 | `KOVAN · HOUGANG · SERANGOON · BISHAN`. Never a customer count. |
| Big bold **serif** headline, last words in a bright accent colour | 1 | "Tennis lessons **near Kovan**", with the highlight in tennis-ball yellow instead of their teal. |
| Two pill buttons: solid blue with an arrow and a soft blue glow, plus a glass outline button | 1 | "WhatsApp Coach →" and "See prices". |
| Row of three trust points with outline icons | 1 | Three credentials (section 6). **No rating**, because there are no reviews yet. |
| Wavy bottom edge on the hero | 1 | Same: an inline SVG wave filled with the next section's colour. |
| Section header: small uppercase blue eyebrow, big serif H2, grey subline, centred | 2, 4 | The same pattern on every section. |
| Service card: rounded, image on top with a "Popular" pill and a glass icon tile, serif title, grey text, grey tag chips, a divider, then "From $89" and "Learn More →" | 2, 3 | Lesson card: 1-on-1 / 2 people / Group of 4. Section 4.3 explains what goes in place of the photo. |
| "Why choose us" grid: icon in a soft blue rounded tile, serif title, grey text, centred | 4 | "Why train with Soon Keat": six real facts, no invented guarantees. |
| Contact block: eyebrow and serif H2 on the left, rows of icon tile + small uppercase label + value, then a white card | 5 | The same rows (WhatsApp, Call, Email, Where). **The card has buttons instead of a form** (section 4.3, item 10). |
| Floating round chat button, bottom right | 1–5 | A floating round **WhatsApp** button. No fake notification dot. |

### 4.1 Tokens

```css
:root {
  --navy:        #0b1a33;  /* hero overlay, footer, headings */
  --ink:         #0f1b2d;  /* body text on light backgrounds */
  --muted:       #5b6b82;  /* sublines, card text: must stay >= 4.5:1 on --mist */
  --blue:        #0f6bd7;  /* buttons, eyebrows, prices, links (white text on it passes AA) */
  --blue-hover:  #0b5bb8;
  --blue-tint:   #e4eefb;  /* icon tiles */
  --ball:        #dcf23a;  /* tennis-ball yellow: headline highlight on dark, "Popular" pill with navy text. Never as text on white. */
  --mist:        #f4f7fb;  /* alternating section background (the reference's pale blue-grey) */
  --paper:       #ffffff;
  --line:        #e3e8ef;  /* card borders, dividers */
  --chip:        #eef1f5;  /* tag chips */
  --radius-card: 20px;
  --radius-tile: 16px;
  --shadow-card: 0 1px 2px rgb(15 27 45 / .04), 0 10px 30px -12px rgb(15 27 45 / .18);
  --glow:        0 12px 32px -10px rgb(15 107 215 / .65);
}
```

Fonts:

```css
--font-head: "Playfair Display", Georgia, "Times New Roman", serif;   /* EN headings, 700 only */
--font-body: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial,
             "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans SC", sans-serif;
```

- Load **Playfair Display 700 only**, Latin subset, from Google Fonts with
  `display=swap` and `preconnect`. This is the reference's serif headline
  look. The body text uses the system sans stack, as the reference does.
- **Chinese pages:** headings use the body stack at weight 700 (PingFang /
  YaHei). Chinese serif system fonts vary too much between phones. Never load
  a Chinese web font; they are several MB.
- Sizes: H1 `clamp(2.4rem, 6vw, 4.25rem)`, line-height 1.08. H2
  `clamp(1.9rem, 4vw, 2.75rem)`. Card title 1.35rem. Eyebrow 0.8rem, 700,
  uppercase, `letter-spacing: .14em`, `--blue` (on dark backgrounds use
  `--ball`). Body 1.0625rem/1.65; sublines 1.15rem, `--muted`, max 680px.
- Light theme only. Every text/background pair passes **WCAG AA**. There is
  a visible focus ring on every link, button and `summary`
  (`outline: 3px solid var(--blue); outline-offset: 3px`; on dark
  backgrounds `var(--ball)`).
- Motion: cards lift `translateY(-4px)` and the shadow deepens on hover
  (200ms); buttons darken. Put all of it inside
  `@media (prefers-reduced-motion: no-preference)`.

### 4.2 Components

- **Primary button**: pill (`border-radius: 999px`), `--blue` background,
  white 600-weight text, `--glow` shadow, a right-arrow SVG after the label,
  min-height 48px, padding `0 1.6rem`. It is full width on mobile inside the
  hero and inline from 640px up.
- **Glass button** (on dark backgrounds only): pill,
  `background: rgb(255 255 255 / .08)`, `border: 1px solid rgb(255 255 255 / .35)`,
  white text, `backdrop-filter: blur(6px)`.
- **Glass badge**: pill, `rgb(15 107 215 / .18)` background, a 1px
  `rgb(255 255 255 / .18)` border, white uppercase 0.78rem 700 text with
  `.08em` tracking.
- **Icon tile**: 60px square, `--radius-tile`, `--blue-tint` background,
  28px outline icon in `--blue`, stroke 1.75. Use
  [Lucide](https://lucide.dev) icon paths as inline SVG (ISC licence), with
  `aria-hidden="true"` on each. Put one HTML comment
  `<!-- Icons: Lucide, ISC licence -->` in each page. Icons needed:
  `message-circle`, `phone`, `mail`, `map-pin`, `clock`, `trophy`, `award`,
  `wallet`, `cloud-rain`, `users`, `user`, `baby` (or `smile`),
  `arrow-right`, `menu`, `chevron-down`. Write the WhatsApp glyph by hand
  as a simple speech bubble with a phone inside. **Do not** copy
  WhatsApp's logo file.
- **Tag chip**: `--chip` background, `--muted` text, 0.85rem, pill,
  padding `.35rem .8rem`.
- **Card**: `--paper`, 1px `--line` border, `--radius-card`,
  `--shadow-card`, `overflow: hidden`. The body is padded 28px (22px on
  mobile).
- **Floating WhatsApp button**: 60px circle, `--blue`, white glyph, `--glow`,
  `position: fixed; right: 20px; bottom: calc(20px + env(safe-area-inset-bottom))`,
  `z-index: 50`, `aria-label="WhatsApp Coach Soon Keat"` (`"WhatsApp 联系陈教练"`
  on Chinese pages). It uses the general pre-filled message. Give the footer
  96px of bottom padding so the button never covers footer text.

### 4.3 Home page, section by section

Backgrounds alternate `--paper` / `--mist`, following the reference. Every
section after the hero opens with the **section header pattern**: eyebrow,
serif H2 and grey subline, centred. Only the contact section is
left-aligned, as in screenshot 5. Vertical padding is `clamp(64px, 9vw, 112px)`.

1. **Header** (over the hero). Logo tile (40px, `--blue`, radius 12px, white
   ball glyph) + serif wordmark on the left. On the right: the language link
   ("中文" / "EN") and a **hamburger built from `<details>`/`<summary>`**. No
   JavaScript: opening the `<details>` shows a white dropdown panel with
   links to Lessons, Coach, FAQ and Contact, plus the WhatsApp button. From
   1024px up, hide the hamburger and show those links inline instead.

   The header starts transparent, with white text, positioned absolute over
   the hero. **Progressive enhancement, still without JavaScript:** inside
   `@supports (animation-timeline: scroll())`, make it
   `position: fixed` and run a keyframe animation on
   `animation-timeline: scroll(root)` with `animation-range: 0 140px`. The
   animation takes it from transparent / white text to a white background,
   `--ink` text and a soft shadow, which is the white bar in screenshots 2
   and 4. Browsers without support get a header that scrolls away with the
   hero, which is fine because the floating button is always there. Give the
   icons `currentColor` so they change colour with the text.

2. **Hero** (`#top`), `min-height: min(92vh, 860px)` on desktop; on mobile
   the height follows the content, with 120px top padding to clear the
   header.
   - The photo is a real `<img>` (not a CSS background, so it can be the LCP
     element and carry alt text): `position: absolute; inset: 0;
     object-fit: cover; object-position: 68% 35%` (on mobile `72% 30%`),
     `fetchpriority="high"`, no lazy loading, with `width`/`height` set.
   - Overlay: `linear-gradient(90deg, rgb(11 26 51 / .94) 0%, rgb(11 26 51 / .82) 42%, rgb(11 26 51 / .35) 100%)`.
     On mobile use a vertical version (`180deg`, .55 → .92) so the text at
     the bottom stays readable.
   - Content, left-aligned, max 640px: glass badge, then the H1 with the last
     words in `<span class="hl">` coloured `--ball`, then a subline (white at
     80% opacity), then the primary and glass buttons, then the trust row
     (three items, each a 20px outline icon in `--ball` plus white text at
     80% opacity, wrapping onto separate lines on mobile).
   - Bottom: an inline SVG wave (`preserveAspectRatio="none"`, ~70px tall,
     full width), filled with `--mist`.
   - The photo is only 768px wide, so it will look soft on large screens.
     The dark overlay hides most of that. Section 12 asks the coach for a
     larger one. **Do not** sharpen, upscale or AI-enhance it.

3. **Lessons & prices** (`#prices`, `--mist`): three lesson cards in the
   reference's service-card style, one column on mobile, three from 960px.
   There is only one photo per lesson type to go round (none), so **the card
   image area is an illustration of a tennis court**: a 150px-tall band with
   a `--blue` → `#0a4fa8` gradient and white court lines drawn in inline SVG
   (baseline, service line, centre line, at 35% opacity), different on each
   card. Solo is a half-court with one small yellow ball; 2 people shows
   two balls; group shows four. Put the glass icon tile in the bottom-left
   of the band, as in the reference (`user`, `users`, and `users` with a
   "4"). The 2-person card has the **"Popular" pill** top-left, with a `--ball`
   background and `--navy` text. Card body: serif title, one-sentence
   description, 3 tag chips, a divider, then a footer row with the price
   left (`$100` in `--blue`, bold, 1.5rem, then `/hour` or
   `/hour per person` in `--muted`) and `WhatsApp →` right, as a link with
   that card's pre-filled message. There is **no "From"** before the prices;
   they are exact. Under the cards, the "Good to know" list as four
   inline items with check icons, centred.

4. **Who it's for** (`#levels`, `--paper`): five compact cards, each an icon
   tile on the left and title + text on the right. They sit in 1 column on
   mobile, 2 on tablet and 3 on desktop (the kids card takes the last slot,
   with a `--blue` "Tennis lessons for kids →" link).

5. **Meet your coach** (`#coach`, `--mist`): split layout. On the left, the
   Davis Cup photo in a rounded card with its caption underneath. On the
   right, the section header left-aligned, the intro paragraph, then the
   achievements as a list with a small `trophy`/`award` icon per line. It
   stacks on mobile with the photo first.

6. **Why train with Soon Keat** (`#why`, `--paper`): the reference's
   feature grid (screenshot 4). Six items, 2 columns on mobile and tablet,
   3 on desktop, centred, each with an icon tile, a serif title and grey
   text.

7. **How it works** (`#how`, `--mist`): three numbered cards in a row
   (stacked on mobile). The number sits in a 44px `--blue` circle with white
   serif digits.

8. **Where & when** (`#where`, `--paper`): the four areas as large chips
   with `map-pin` icons, then two info cards side by side: "Hours" with a
   `clock` icon, and "Lesson length".

9. **FAQ** (`#faq`, `--mist`): `<details>` items styled as white cards with
   a 12px radius and 1px border. The `summary` is 600 weight with a
   `chevron-down` that rotates when open. The first item is open. Max width
   760px, centred.

10. **Contact** (`#contact`, `--paper`): the layout of screenshot 5. On the
    left: eyebrow, serif H2 and subline, then four contact rows (icon tile +
    small uppercase label + value, each value a link):
    WhatsApp → `wa.me`, Call → `tel:`, Email → `mailto:`, and Where (plain
    text). On the right, a white card titled **"Send a quick message"**.
    Instead of a form, it holds five full-width buttons that each open
    WhatsApp with a different pre-filled message (section 5): one primary
    ("Ask a question"), then four outlined (1-on-1, 2 people, Group of 4,
    Lessons for my child). There is **no form**: nothing is collected and
    nothing needs a backend or a privacy notice. The two columns stack on
    mobile.

11. **Footer** (`--navy`, white text at 75% opacity): logo and wordmark,
    one line "Tennis lessons near Kovan, Hougang, Serangoon and Bishan.",
    contact links, the language link, and "© 2026 Chan Soon Keat" (the year
    is typed in the HTML).

### 4.4 Kids page (`/kids/`, `/zh/kids/`)

The same components as the home page, with its own content (Google ignores
near-duplicates). The hero is the same, but at `min-height: 64vh` with the
kids H1 and a breadcrumb line above the badge. Then: "How lessons work for
kids" (a feature grid of four), "What to bring" (one card with icon chips),
the same three lesson cards (kids pre-filled messages), the parent FAQ, and
the contact section with the kids message on the primary button. Copy is in
sections 6.3 and 6.4.

### 4.5 404 page

Navy background, the logo, "Page not found / 找不到此页面" as a serif H1, links
to `/` and `/zh/`, and the primary WhatsApp button. Add
`<meta name="robots" content="noindex">`.

### 4.6 Mobile first

Design at **360–390px** first, then widen. Page gutter 16px (24px from
768px). Content max width 1180px. **No horizontal scrolling at any width
from 320px up.** The reference screenshots were taken at about 930px, the
point where cards are single-column and wide. At 1280px the lesson cards
sit three across.

## 5. Links and contact details (use exactly these)

- WhatsApp base: `https://wa.me/6588841034?text=` + URL-encoded message.
  Always `rel="noopener"`. Open in the same tab: on a phone it hands off to
  the app anyway.
- Pre-filled messages. Encode with `encodeURIComponent` semantics, so spaces
  become `%20`; do not use `+`.

  | Button | EN message | 中文 message |
  |---|---|---|
  | General (hero, header menu, floating button, contact card "Ask a question") | `Hi Coach Soon Keat, I found your website and I'm interested in tennis lessons near Kovan.` | `陈教练您好，我在网站上看到您的网球课，想了解一下。` |
  | 1-on-1 card | `Hi Coach Soon Keat, I'm interested in a 1-on-1 tennis lesson.` | `陈教练您好，我想了解一对一网球课。` |
  | 2-person card | `Hi Coach Soon Keat, I'm interested in a 2-person tennis lesson.` | `陈教练您好，我想了解一对二网球课。` |
  | Group card | `Hi Coach Soon Keat, I'm interested in a group tennis lesson (4 people).` | `陈教练您好，我想了解4人团体网球课。` |
  | Contact card: "Lessons for my child", and every kids page button | `Hi Coach Soon Keat, I'm interested in tennis lessons for my child.` | `陈教练您好，我想为孩子报名网球课。` |

- Phone: `<a href="tel:+6588841034">+65 8884 1034</a>`
- Email: `<a href="mailto:chansoonkeat123@gmail.com">chansoonkeat123@gmail.com</a>`

---

## 6. Copy (use as written)

Rules for any copy you must adjust: British/Singapore spelling ("racquet",
"centre"). Prices are always written `$100`, never `SGD100` or `S$100` in
body text (the JSON-LD uses `SGD`). **Never write "5 years of experience"**:
it goes out of date every January. Write "coaching since 2021" instead.

The flyer has typos. Do not copy them: "who wants", "newsport", "SUNNIG".

### 6.1 English home (`/`)

**`<title>`:** `Tennis Lessons near Kovan, Singapore | Coach Soon Keat`

**Meta description:** `Private, 2-person and group tennis lessons near Kovan, Hougang, Serangoon and Bishan with former Malaysia junior national player Chan Soon Keat. From $50/hr. WhatsApp to book.`

**Hero**
- Glass badge: `Kovan · Hougang · Serangoon · Bishan` (rendered uppercase by CSS)
- H1: `Tennis lessons near Kovan`, with `near Kovan` as the highlight
- Subline: `Private and group coaching for complete beginners through to tournament players, from a former Malaysia junior national player. Adults, teenagers and kids welcome.`
- Buttons: `WhatsApp Coach` (with arrow) · `See prices`
- Trust row: `Former Malaysia national player` (trophy) · `Level 1 certified coach` (award) · `Coaching since 2021` (clock)

**Who it's for**: eyebrow `Who it's for`, H2 `Lessons for every level`, subline `From your very first rally to your next tournament.`
- **Newcomers**: `Never held a racquet? Start here. We cover grip, footwork and your first rallies, with no experience needed.`
- **Beginners**: `You've played a little and want your basics to feel solid: cleaner strokes, better consistency, and fixing the habits that hold you back.`
- **Recreational players**: `You've got the fundamentals and want to sharpen them with drills, match play and a hitting partner who pushes you.`
- **Competitive players**: `Tournament players who want high-intensity sparring and match preparation to stay sharp.`
- **Kids & teenagers**: `Patient, fun lessons that build real technique from the start.` Link text: `Tennis lessons for kids →` (to `/kids/`)

**Lessons & prices**: eyebrow `Lessons & prices`, H2 `Choose how you train`, subline `Simple per-person pricing. Racquets and balls are provided.`
- Card 1, `1-on-1 private`: `All the coach's attention on you, with every lesson planned around your goals.` Chips: `1 player` `Your goals` `All levels`. Price `$100` `/hour`.
- Card 2, `2 people`: pill `Popular`. `Train with a friend, partner or family member, with plenty of rallying between the two of you.` Chips: `2 players` `Friends & couples` `All levels`. Price `$70` `/hour per person`.
- Card 3, `Group of 4`: `A 1-hour class for four players. Great value for friends learning together.` Chips: `4 players` `1-hour class` `Best value`. Price `$50` `/hour per person`.
- Footer link on every card: `WhatsApp →`
- Under the cards, heading `Good to know`:
  - `Racquets and balls are provided, so you don't need to buy anything to start.`
  - `All prices are per person.`
  - `You book and pay for the court. Condo courts and public courts are both fine.`
  - `Lesson times are flexible. Message to arrange.`

**Why train with Soon Keat**: eyebrow `Why train with Soon Keat`, H2 `What you get`, subline `No packages, no deposits, no fuss. Just good tennis.`
1. `A former national player` (trophy): `Represented Malaysia at U14 and U16 level, and a Tennis Malaysia Level 1 certified coach.`
2. `Racquets and balls provided` (award): `Turn up in sports shoes. You don't need to buy anything to start.`
3. `Pay after the lesson` (wallet): `PayNow after each lesson. No deposit and no package to buy.`
4. `Flexible times` (clock): `Weekday evenings from 7pm, and from 7am on weekends and public holidays.`
5. `A court near you` (map-pin): `Your condo court or a public court around Kovan. The coach comes to you.`
6. `Never charged for rain` (cloud-rain): `If rain cancels your lesson, there's no charge.`

**How it works**: eyebrow `How it works`, H2 `Three steps to your first lesson`
1. `Message on WhatsApp`: `Tell the coach your level, how many people, and the days that suit you.`
2. `Pick a court and time`: `Book a court near you (your condo or a public court), and the coach will meet you there.`
3. `Play, then pay`: `Pay by PayNow after the lesson. No deposit, no package to buy.`

**Meet your coach**: eyebrow `Your coach`, H2 `Meet Coach Soon Keat`
- Intro: `Chan Soon Keat (陈顺杰) represented Malaysia as a junior and has been coaching in Singapore since 2021. He teaches everyone from first-timers to tournament players, and adapts every lesson to the person in front of him.`
- Achievements (list, most impressive first):
  - `Represented Malaysia at U14 and U16 international tournaments`
  - `Ranked No. 1 U16 player in Malaysia (2018)`
  - `Bronze medal, ASEAN Schools Games 2019`
  - `2023 STA Interclub Men's Champion`
  - `SUniG 2023/24 Champion`
  - `Tennis Malaysia Level 1 certified coach`
- Photo alt: `Chan Soon Keat (second from left) with the Malaysia Junior Davis Cup team`. Visible caption: `With the Malaysia Junior Davis Cup team`.
  (The coach should confirm which person he is in the photo; see section 12.
  If you cannot confirm it, use the alt text `Chan Soon Keat with the Malaysia Junior Davis Cup team`, which does not name a position.)
  **Use the version without the position unless the coach has confirmed it.**
- Hero photo alt (both pages): `Coach Chan Soon Keat hitting a forehand on a floodlit court`

**Where & when**: eyebrow `Where & when`, H2 `Lessons at a court near you`
- `Lessons are held at a court you book, anywhere around:` then the chips `Kovan` `Hougang` `Serangoon` `Bishan`.
- `Somewhere else in Singapore? Ask, and it can often be arranged.`
- Hours: `Weekday evenings from 7pm · Weekends and public holidays from 7am · Lessons finish by 10pm`
- Lengths: `Lessons are usually 1 hour; 1.5 and 2 hours are available.`

**FAQ**: eyebrow `FAQ`, H2 `Questions, answered`
1. `Do I need my own racquet?`: `No. Racquets and balls are provided. If you already have a racquet, bring it.`
2. `Who books the court?`: `You do. Book any court near you, such as your condo's court or a public court, and pay the court fee directly. The coach comes to you.`
3. `I've never played before. Is that OK?`: `Absolutely. Complete beginners are very welcome. The first lesson starts from how to hold the racquet.`
4. `How long is a lesson?`: `Usually 1 hour. 1.5-hour and 2-hour lessons are also available. Group classes are 1 hour.`
5. `When are lessons available?`: `Weekday evenings from 7pm, and from 7am on weekends and public holidays. Every lesson finishes by 10pm.`
6. `How do I pay?`: `By PayNow after the lesson. There's no deposit and no package to buy. You pay per lesson.`
7. `What if I need to cancel?`: `Cancel at least 3 days ahead and there's no charge. Closer to the day, just message the reason and the coach will sort it out fairly.`
8. `What happens if it rains?`: `The coach will check in with you before the lesson. A lesson cancelled because of rain is never charged.`
9. `Can I bring friends?`: `Yes. 2 people is $70/hour each, and a group of 4 is $50/hour each.`

**Contact**: eyebrow `Get in touch`, H2 `Ready to get on court?`, subline `Message Coach Soon Keat on WhatsApp to arrange your first lesson.`
- Rows: `WhatsApp` → `+65 8884 1034` · `Call` → `+65 8884 1034` · `Email` → `chansoonkeat123@gmail.com` · `Where` → `Your court, around Kovan, Hougang, Serangoon and Bishan`
- Card title `Send a quick message`, text `Tap what you're interested in. WhatsApp opens with the message already typed.`
- Buttons: `Ask a question` (primary) · `1-on-1 lesson` · `2-person lesson` · `Group of 4` · `Lessons for my child`

> Do not promise a reply time ("usually replies the same day") unless the
> coach confirms it in the PR.

### 6.2 中文 home (`/zh/`)

**`<title>`:** `高文网球课 | 一对一及团体网球教学 · 陈顺杰教练`

**Meta description:** `高文、后港、实龙岗、碧山一带网球课。前马来西亚青少年国手陈顺杰亲自执教，一对一、一对二及4人团体班，每小时$50起。WhatsApp 预约。`

**Hero**
- Glass badge: `高文 · 后港 · 实龙岗 · 碧山`
- H1: `高文网球课`, with `高文` as the highlight
- Subline: `由前马来西亚青少年国手亲自执教，从零基础到比赛选手都适合。欢迎成人、青少年及儿童报名。`
- Buttons: `WhatsApp 联系教练`（带箭头） · `查看收费`
- Trust row: `前马来西亚国手` · `一级认证教练` · `2021年起执教`

**适合对象**: eyebrow `适合对象`, H2 `各个水平都能学`, subline `从第一次对打，到下一场比赛。`
- **新手**: `零基础也没问题：从握拍、步法到第一次来回对打，一步步教。`
- **初学者**: `已经学过一段时间，想打好基础：动作更规范、击球更稳定，针对性改进弱点。`
- **业余选手**: `基础扎实，想进一步提升：技术训练、实战对练、陪练，休闲又有进步。`
- **比赛选手**: `高强度对打与陪练，为比赛做准备、保持状态。`
- **儿童及青少年**: `耐心有趣的教学，从一开始就打好正确的技术基础。` Link: `儿童网球课 →` (to `/zh/kids/`)

**课程与收费**: eyebrow `课程与收费`, H2 `选择适合你的上课方式`, subline `按人计费，简单透明。提供网球拍和网球。`
- `一对一私教`: `教练全程专注于你，每堂课根据你的目标安排。` Chips: `1人` `针对目标` `各水平`. Price `$100` `/小时`.
- `一对二`: pill `热门`. `和朋友、伴侣或家人一起上课，两人之间有大量对打练习。` Chips: `2人` `朋友情侣` `各水平`. Price `$70` `/小时/人`.
- `4人团体班`: `每班4人，每堂1小时。和朋友一起学，最划算。` Chips: `4人` `1小时` `最划算`. Price `$50` `/小时/人`.
- Footer link on every card: `WhatsApp →`
- `须知`:
  - `提供网球拍和网球，开始学不需要购买任何装备。`
  - `以上均为每人价格。`
  - `场地由学生自行预订及付费，公寓球场或公共球场都可以。`
  - `上课时间可商量，欢迎联系安排。`

**为什么选择陈教练**: eyebrow `为什么选择陈教练`, H2 `你能得到什么`, subline `没有配套，没有订金，简单上课。`
1. `前国手亲自执教`: `曾代表马来西亚参加U14及U16赛事，马来西亚网球总会一级认证教练。`
2. `提供球拍和网球`: `穿运动鞋来就可以，开始学不需要买任何装备。`
3. `上课后付款`: `每堂课后用 PayNow 付款，无需订金，也不用买配套。`
4. `时间灵活`: `平日晚上7点起，周末及公共假期早上7点起。`
5. `就近上课`: `在高文一带的公寓球场或公共球场，教练到场。`
6. `下雨不收费`: `如果因下雨取消，一律不收费。`

**上课流程**: eyebrow `上课流程`, H2 `三步开始第一堂课`
1. `WhatsApp 联系`: `告诉教练你的水平、人数和方便的时间。`
2. `订场地、定时间`: `在你附近预订球场（公寓或公共球场），教练到场上课。`
3. `上课后付款`: `课后用 PayNow 付款，无需订金，也不用买配套。`

**教练介绍**: eyebrow `你的教练`, H2 `认识陈顺杰教练`
- Intro: `陈顺杰（Chan Soon Keat）曾代表马来西亚参加青少年国际赛事，2021年起在新加坡执教。从初学者到比赛选手都有教学经验，每堂课都会根据学生的情况调整。`
- 生涯纪录:
  - `代表马来西亚参加U14及U16国际赛事`
  - `2018年马来西亚U16排名第一`
  - `2019年东盟学校运动会铜牌`
  - `2023年新加坡网球协会（STA）俱乐部联赛男子组冠军`
  - `SUniG 2023/24 冠军`
  - `马来西亚网球总会一级认证教练`
- Photo alt: `陈顺杰与马来西亚青少年戴维斯杯代表队合影`. Caption: `与马来西亚青少年戴维斯杯代表队合影`
- Hero photo alt: `陈顺杰教练在灯光球场正手击球`

**地点与时间**: eyebrow `地点与时间`, H2 `在你附近的球场上课`
- `在你预订的球场上课，服务范围：` chips `高文` `后港` `实龙岗` `碧山`
- `其他地区？欢迎询问，通常都可以安排。`
- `平日晚上7点起 · 周末及公共假期早上7点起 · 晚上10点前结束`
- `一般每堂1小时，也可以上1.5小时或2小时。`

**FAQ**: eyebrow `FAQ`, H2 `常见问题`
1. `需要自己带球拍吗？`: `不需要，教练提供网球拍和网球。如果你有自己的球拍，也欢迎带来。`
2. `场地由谁预订？`: `由学生预订并支付场地费，公寓球场或公共球场都可以，教练会到场上课。`
3. `完全没打过网球可以吗？`: `当然可以！非常欢迎零基础的新手，第一堂课从握拍开始教。`
4. `每堂课多长时间？`: `一般1小时，也可以上1.5小时或2小时。团体班每堂1小时。`
5. `什么时候可以上课？`: `平日晚上7点起，周末及公共假期早上7点起，每堂课在晚上10点前结束。`
6. `怎么付款？`: `课后用 PayNow 付款。无需订金，也不用购买配套，每堂课单独付费。`
7. `如果需要取消怎么办？`: `提前3天或以上取消不收费。如果离上课时间较近，请告诉教练原因，教练会合理处理。`
8. `下雨怎么办？`: `教练会在上课前和你确认。因下雨取消的课程一律不收费。`
9. `可以和朋友一起上吗？`: `可以！一对二每人每小时$70，4人团体班每人每小时$50。`

**Contact**: eyebrow `联系我们`, H2 `准备好上场了吗？`, subline `WhatsApp 联系陈教练，安排你的第一堂课。`
- Rows: `WhatsApp` → `+65 8884 1034` · `电话` → `+65 8884 1034` · `电邮` → `chansoonkeat123@gmail.com` · `地点` → `你预订的球场：高文、后港、实龙岗、碧山一带`
- Card title `快速留言`, text `点选你想了解的课程，WhatsApp 会自动填好信息。`
- Buttons: `咨询问题`（primary） · `一对一私教` · `一对二` · `4人团体班` · `儿童网球课`

### 6.3 English kids page (`/kids/`)

**`<title>`:** `Kids Tennis Lessons near Kovan | Coach Soon Keat`

**Meta description:** `Tennis lessons for kids and teenagers near Kovan, Hougang, Serangoon and Bishan. Patient coaching from a former Malaysia junior national player. Racquets provided. WhatsApp to book.`

- Breadcrumb: `Home › Kids tennis lessons`
- H1: `Tennis lessons for kids near Kovan`
- Subline: `Patient, fun coaching for children and teenagers from a coach who came up through junior tennis himself, as a former Malaysia U14 and U16 national player.`
- H2 `How lessons work for kids`:
  - `Private or with a sibling or friend: 1-on-1, 2 kids together, or a group of 4.`
  - `Proper technique from day one, taught through games and rallies so it stays fun.`
  - `Held at a court you book near home, such as your condo's court or a public court.`
  - `Parents are welcome to watch.`
- H2 `What to bring`: `Sports shoes (non-marking soles), comfortable clothes, a water bottle and a cap. Racquets and balls are provided.`
- H2 `Prices`: the same three cards and numbers as the home page, with the kids pre-filled WhatsApp message on each button.
- H2 `Questions from parents`:
  1. `My child has never played. Is that OK?`: `Yes. Most kids start from zero, and lessons begin with the basics.`
  2. `Can siblings or friends share a lesson?`: `Yes. 2 kids is $70/hour each, and a group of 4 is $50/hour each.`
  3. `Do we need to buy a racquet?`: `Not to start. Racquets and balls are provided. The coach can advise on the right racquet size later if your child keeps going.`
  4. `When are lessons?`: `Weekday evenings from 7pm, and from 7am on weekends and public holidays.`
  5. `Who books the court?`: `You do, at any court near you. The coach comes to you.`
- Contact section: H2 `Book your child's first lesson`, same rows and card as the home page, with `Lessons for my child` as the primary button.
- **Do not state a minimum age anywhere.** (See section 12.)

### 6.4 中文 kids page (`/zh/kids/`)

**`<title>`:** `高文儿童网球课 | 陈顺杰教练`

**Meta description:** `高文、后港、实龙岗、碧山一带儿童及青少年网球课。前马来西亚青少年国手耐心教学，提供球拍。WhatsApp 预约。`

- Breadcrumb: `首页 › 儿童网球课`
- H1: `高文儿童网球课`
- Subline: `教练本身是前马来西亚U14及U16国手，从青少年网球一路打上来，教孩子耐心又有趣。`
- H2 `孩子怎么上课`:
  - `可以一对一，也可以和兄弟姐妹或朋友一起：一对二或4人小组。`
  - `从第一堂课就学正确的技术，通过游戏和对打让孩子保持兴趣。`
  - `在你家附近预订的球场上课，公寓球场或公共球场都可以。`
  - `欢迎家长在场观看。`
- H2 `需要准备什么`: `运动鞋（不留痕鞋底）、舒适的运动服、水壶和帽子。教练提供网球拍和网球。`
- H2 `收费标准`: the same three cards, with the 中文 kids WhatsApp message.
- H2 `家长常见问题`:
  1. `孩子完全没打过网球可以吗？`: `可以，大部分孩子都是从零开始，课程从基础教起。`
  2. `兄弟姐妹或朋友可以一起上吗？`: `可以！两个孩子每人每小时$70，4人小组每人每小时$50。`
  3. `需要买球拍吗？`: `刚开始不需要，教练提供球拍和网球。之后如果孩子继续学，教练可以建议合适的球拍尺寸。`
  4. `什么时候上课？`: `平日晚上7点起，周末及公共假期早上7点起。`
  5. `场地由谁预订？`: `由家长在附近预订任何球场，教练到场上课。`
- Contact section: H2 `为孩子预约第一堂课`, same rows and card as the 中文 home page, with `儿童网球课` as the primary button.

---

## 7. Search engine setup (the point of the whole site)

Be realistic about what this gets: a new site on a free `pages.dev` address
**will not reach page one for a bare "tennis lessons" search** against
established academies. What it **can** win, over weeks rather than days, is
the local and long-tail searches: "tennis lessons Kovan", "tennis coach
Hougang", "kids tennis lessons Serangoon", "高文 网球课". Google also shows
local results to people physically nearby, which is where the **Google
Business Profile** (section 10) does more than the website itself. Build for
that.

### 7.1 On every page

- `<html lang="en">` on English pages, `<html lang="zh-Hans">` on Chinese
  pages.
- `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- Unique `<title>` and `<meta name="description">` from section 6.
- `<link rel="canonical" href="https://kovan-tennis.pages.dev/...">`: an
  absolute URL, with a trailing slash on directory pages.
- **hreflang, reciprocal**, on all four content pages. For example, on `/`
  and on `/zh/`:
  ```html
  <link rel="alternate" hreflang="en" href="https://kovan-tennis.pages.dev/">
  <link rel="alternate" hreflang="zh-Hans" href="https://kovan-tennis.pages.dev/zh/">
  <link rel="alternate" hreflang="x-default" href="https://kovan-tennis.pages.dev/">
  ```
  `/kids/` ⇄ `/zh/kids/` follows the same pattern.
- Open Graph tags, so a link shared on WhatsApp or Telegram shows a nice
  preview card: `og:type=website`, `og:title`, `og:description`, `og:url`,
  `og:image=https://kovan-tennis.pages.dev/img/coach-forehand.jpg`,
  `og:image:width=768`, `og:image:height=513`, `og:locale` (`en_SG` /
  `zh_SG`), `og:site_name=Coach Soon Keat Tennis`. Also add
  `<meta name="twitter:card" content="summary_large_image">`.
- `<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">`, and
  `<meta name="theme-color" content="#0b1a33">`.
- Exactly **one `<h1>`** per page, and headings in order (no skipping from
  h2 to h4).
- Every `<img>` has `alt`, `width` and `height`. Every image except the hero
  gets `loading="lazy"` and `decoding="async"`.
- Place names appear naturally in headings and body text (Kovan, Hougang,
  Serangoon, Bishan / 高文, 后港, 实龙岗, 碧山). **Do not keyword-stuff**, add
  hidden text, or add one page per neighbourhood. Google treats thin
  "doorway" pages as spam and demotes the whole site.

### 7.2 Structured data (JSON-LD)

Put one `<script type="application/ld+json">` in the `<head>` of **both home
pages** (with `inLanguage` and `description` in the page's language). It is
the only `<script>` tag allowed on the site, and it is data, not code. On the
kids pages, include only a `BreadcrumbList`.

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://kovan-tennis.pages.dev/#business",
  "name": "Coach Soon Keat Tennis Lessons",
  "alternateName": "陈顺杰网球教练",
  "description": "Private, 2-person and group tennis lessons near Kovan, Singapore, for adults and kids.",
  "url": "https://kovan-tennis.pages.dev/",
  "image": "https://kovan-tennis.pages.dev/img/coach-forehand.jpg",
  "telephone": "+6588841034",
  "email": "chansoonkeat123@gmail.com",
  "priceRange": "$50–$100",
  "currenciesAccepted": "SGD",
  "paymentAccepted": "PayNow",
  "areaServed": [
    {"@type": "Place", "name": "Kovan, Singapore"},
    {"@type": "Place", "name": "Hougang, Singapore"},
    {"@type": "Place", "name": "Serangoon, Singapore"},
    {"@type": "Place", "name": "Bishan, Singapore"},
    {"@type": "GeoCircle",
     "geoMidpoint": {"@type": "GeoCoordinates", "latitude": 1.3603, "longitude": 103.8851},
     "geoRadius": 5000}
  ],
  "founder": {
    "@type": "Person",
    "name": "Chan Soon Keat",
    "alternateName": "陈顺杰",
    "jobTitle": "Tennis Coach",
    "hasCredential": "Tennis Malaysia Level 1 Coach"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Tennis lessons",
    "itemListElement": [
      {"@type": "Offer", "name": "1-on-1 private tennis lesson", "price": "100", "priceCurrency": "SGD",
       "unitText": "per hour"},
      {"@type": "Offer", "name": "2-person tennis lesson", "price": "70", "priceCurrency": "SGD",
       "unitText": "per person per hour"},
      {"@type": "Offer", "name": "Group tennis lesson (4 people)", "price": "50", "priceCurrency": "SGD",
       "unitText": "per person per hour"}
    ]
  },
  "openingHoursSpecification": [
    {"@type": "OpeningHoursSpecification",
     "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "19:00", "closes": "22:00"},
    {"@type": "OpeningHoursSpecification",
     "dayOfWeek": ["Saturday","Sunday"], "opens": "07:00", "closes": "22:00"}
  ],
  "knowsLanguage": ["en", "zh", "ms"]
}
```

The midpoint coordinates are Kovan MRT. **Do not add** `address` (there is no
premises, and a fake address is a policy violation), `aggregateRating` or
`review` (there are no real reviews on the site), or `FAQPage` (Google shows
FAQ rich results only for government and health sites, so it adds nothing).
The JSON must parse; the tests check it.

### 7.3 `robots.txt`

```
User-agent: *
Allow: /

Sitemap: https://kovan-tennis.pages.dev/sitemap.xml
```

### 7.4 `sitemap.xml`

List the four content pages (not `404.html`). Each `<url>` carries the
`xhtml:link` hreflang alternates (declare
`xmlns:xhtml="http://www.w3.org/1999/xhtml"`) and a `<lastmod>` of the build
date.

### 7.5 Search Console verification

Leave room for the coach's verification tag: in `index.html` only, add the
comment `<!-- google-site-verification: paste the meta tag from Search Console here -->`.
The coach replaces it later (section 10, step B). A comment is harmless;
**never** ship a fake `<meta name="google-site-verification" content="...">`.

---

## 8. Performance and hosting headers

Targets on a mobile Lighthouse run: **Performance ≥ 95, Accessibility 100,
Best Practices 100, SEO 100.** The full home page (HTML + CSS + images +
fonts) weighs **under 450 KB**.

- CSS in one file, under 20 KB, no unused framework rules. Link it in the
  `<head>` normally. It is small enough that render blocking does not matter.
- The images are already web-sized JPEGs (~100–130 KB). Do not upscale them.
  If Pillow is available on your machine, you **may** add a 480px-wide
  version of the hero for small screens via `srcset`/`sizes`; otherwise use
  the originals as they are. Do not add Pillow to `pyproject.toml`.
- `site/_headers`:
  ```
  /*
    X-Content-Type-Options: nosniff
    Referrer-Policy: strict-origin-when-cross-origin
    Permissions-Policy: camera=(), microphone=(), geolocation=()
    X-Frame-Options: DENY
    Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; script-src 'none'; base-uri 'self'; form-action 'none'; frame-ancestors 'none'

  /css/*
    Cache-Control: public, max-age=86400

  /img/*
    Cache-Control: public, max-age=604800
  ```
  The CSP has no `'unsafe-inline'` for styles, so **no `style="..."`
  attributes and no `<style>` blocks**. Everything goes in `css/site.css`,
  and the per-card court illustrations use classes. SVG presentation
  attributes (`fill`, `stroke`, `opacity`) are fine.
  `script-src 'none'` still allows the JSON-LD block, because browsers never
  execute `application/ld+json`. If you add Cloudflare Web Analytics by
  snippet instead of the dashboard switch, this policy would block it, so
  use the dashboard switch (section 10).

---

## 9. Tests: `tests/test_website.py`

Create `.github/workflows/ci.yml`: on `push` to `main` and on every
`pull_request`, check out the repo, set up Python 3.12, run
`pip install pytest ruff`, then `ruff check .` and `pytest -q`. There is no
`pyproject.toml` and none is needed. The test file must pass ruff. Use **only the standard library**
(`html.parser`, `json`, `xml.etree`, `pathlib`, `urllib.parse`). Do not add
dependencies.

Put these at the top of the file as the single source of truth:

```python
SITE = "https://kovan-tennis.pages.dev"
WHATSAPP = "6588841034"
PAGES = {  # path on the site -> file in site/
    "/": "index.html", "/kids/": "kids/index.html",
    "/zh/": "zh/index.html", "/zh/kids/": "zh/kids/index.html",
}
PAIRS = [("/", "/zh/"), ("/kids/", "/zh/kids/")]
PRICES = {"solo": 100, "pair_pp": 70, "group_pp": 50}   # the flyer prices, per person per hour
```

Test classes, each with a docstring explaining **why** it exists (match the
style of the other tests in `tests/`):

1. **`TestPagesExist`**: every file in `PAGES`, plus `404.html`,
   `css/site.css`, `robots.txt`, `sitemap.xml`, `_headers` and
   `img/favicon.svg`, exists.
2. **`TestHeadTags`**: for every page: exactly one `<h1>`; a non-empty
   `<title>` that is at most 65 characters; a `meta description` between 70
   and 170 characters; `lang` of `en` or `zh-Hans` as appropriate; a
   `viewport` meta; `canonical == SITE + path`.
3. **`TestHreflang`**: for every pair, each page links to the other *and*
   to itself, with `x-default` pointing at the English one, and all
   `hreflang` hrefs start with `SITE`.
4. **`TestLinks`**: every internal `href`/`src` (starting with `/`)
   resolves to a file in `site/` (`/kids/` → `kids/index.html`); no
   `http://` links anywhere; every `wa.me` link is
   `https://wa.me/6588841034?text=...` with a non-empty, decodable `text`.
   Every page has at least 2 WhatsApp links.
5. **`TestImages`**: every `<img>` has non-empty `alt`, `width` and
   `height`; none reference a file that is missing.
6. **`TestStructuredData`**: every `application/ld+json` block parses; the
   home pages' `LocalBusiness` has `telephone == "+6588841034"`; its offer
   prices equal `PRICES`; it has no `address`, `aggregateRating` or `review`
   key.
7. **`TestPricesAgree`**: the visible text of all four pages contains `$100`,
   `$70` and `$50`, and no other `$` amount appears on any page. This is what
   stops one page being updated and the others forgotten.
8. **`TestNoScripts`**: no `<script>` tag whose type is not
   `application/ld+json`, no `on*=` event-handler attributes, and no
   `style` attribute or `<style>` element. That keeps
   the "no JavaScript" design and the `_headers` CSP true.
9. **`TestSitemap`**: `sitemap.xml` parses and lists exactly
   `SITE + path` for every key of `PAGES`, and `robots.txt` names that
   sitemap.
10. **`TestNoStaleOrWrongCopy`**: across all pages, none of: `SUNNIG`,
    `newsport`, `years of experience`, `years of coaching`, `5 years`,
    `五年`, `TODO`, `lorem`, `S$`. Anything that counts years goes out of
    date by itself.
11. **`TestOnlyPublicFilesInWebsite`**: `site/` contains only `.html`,
    `.css`, `.jpg`, `.svg`, `.txt`, `.xml` files and `_headers`. There is no
    `.md`, `.py`, `.env`, `.db` or `.yaml`, because everything in that folder
    is published to the internet.

Run `pytest tests/test_website.py -q`, then the whole suite with
`pytest -q`, then `ruff check .`. All must be green.

---

## 10. What the coach does by hand (put this in `docs/website.md`)

Write these steps in plain language for someone who has never used these
tools, Number every click.

**A. Put the site online: Cloudflare Pages (free, about 10 minutes, once)**
1. Sign up at dash.cloudflare.com (free plan).
2. Workers & Pages → Create → Pages → **Connect to Git** → authorise GitHub →
   choose the `kovan-tennis-website` repository. Cloudflare can read a private
   repository. The repository stays private, and only the `site` folder is
   published.
3. Project name `kovan-tennis`. **If that name is taken**, pick another, then
   ask Claude to replace `kovan-tennis.pages.dev` everywhere (the `SITE`
   constant in the test will fail until every page matches).
4. Production branch: `main`. Framework preset: **None**. Build command:
   **leave empty**. Build output directory: `site`.
5. Save. The site is live at `https://kovan-tennis.pages.dev` within a minute.
6. Metrics → **Web Analytics → Enable** (visitor counts, no cookies).

**Unlike the bot, the website DOES go live on merge.** Merging a PR that
touches `site/` publishes it within a minute or two. Nothing else is
involved (no `deploy.sh`, no server). Pull requests get their own preview link from Cloudflare, so the
coach can check a change on their phone before merging.

**B. Tell Google the site exists: Search Console (free, about 10 minutes, once)**
1. search.google.com/search-console → Add property → **URL prefix** →
   `https://kovan-tennis.pages.dev/`.
2. Choose **HTML tag** verification, copy the `<meta ...>` tag, ask Claude
   to put it in `site/index.html` in place of the comment, merge, then
   click Verify.
3. Sitemaps → submit `sitemap.xml`.
4. URL inspection → paste the home page URL → **Request indexing**. Do the
   same for `/zh/` and `/kids/`.
5. Expect it to take 1–4 weeks before the site shows up in searches. That is
   normal.

**C. Get on Google Maps: Google Business Profile (free; the biggest win for "near Kovan")**
1. business.google.com → Add business → name: `Coach Soon Keat Tennis Lessons`.
2. Category: **Tennis instructor**. If it is not offered, use **Sports school**.
3. "Do you want to add a location customers can visit?" → **No** (you go to
   the student's court). Service areas: Kovan, Hougang, Serangoon, Bishan.
4. Phone +65 8884 1034; website `https://kovan-tennis.pages.dev/`.
5. Verify. Google may ask for a short video showing you coaching and some
   proof of the business, such as the flyer or a PayNow receipt; follow its
   prompts.
6. Add services with the three prices, hours (weekday evenings 7–10pm,
   weekends 7am–10pm), and at least 5 photos of you coaching.
7. **Ask every happy student for a Google review.** Reviews are the
   strongest ranking signal for local searches, and the site can show real
   ones later. Share the review link on WhatsApp after a good lesson.
8. Never make up a review or ask friends who have not trained with you to
   write one. Google removes them and can suspend the listing.

**D. Change a price later**
- Edit the numbers in the four HTML pages, the JSON-LD on both home pages,
  and `PRICES` in `tests/test_website.py`. The test fails if any one of them
  is missed.
- **Also change the bot**, or it will quote a different price from the
  website (see section 12).

---

## 11. Repo housekeeping in the same PR

- Update `CLAUDE.md` (it already exists; keep what is there). Replace its
  "Still to build" note with a short description of what now exists:
  `site/` is published by Cloudflare Pages on every merge to `main`;
  everything in `site/` is public; prices must agree with the bot's
  `/setrate`; the guard is `tests/test_website.py`; the coach's guide is
  `docs/website.md`.
- `docs/website.md`: section 10, written for the coach.
- `.gitignore`: `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.venv/`.
- End the commit message with a `Try:` line in the coach's words, for example:
  `Try: open the Cloudflare preview link on your phone -- tap WhatsApp Coach and check the message is pre-typed`.
- Open one PR for the whole site.

## 12. Open items: flag these in the PR description, do not guess

Put these under a heading "Coach to confirm" in the PR body:

1. **The bot quotes different prices from the website.** The bot's built-in
   defaults are $90 / $60pp / $45pp; the website shows the flyer's $100 /
   $70pp / $50pp. Unless the coach has already changed them, the bot will
   quote a new client less than the website did. To match, send the bot:
   `/setrate solo 100`, `/setrate semi 140`, `/setrate group 200`. The semi
   and group amounts are the **total** for 2 and 4 people, as the bot
   stores them. Check with `/rates` afterwards.
2. **Minimum age for kids.** Once known, add one line to both kids pages
   (for example "from age 6") and to the home "Kids & teenagers" card.
3. **SUniG.** The flyer says "SUNNIG 23-24 Champion"; the site writes
   "SUniG 2023/24 Champion" (the Singapore University Games). Confirm it is
   the right event and name, and which event or category it was.
4. **Which person is the coach** in the Junior Davis Cup photo, so the alt
   text can say so.
5. **Bigger photos.** Both photos are small (768px and 437px wide). A few
   high-resolution photos of the coach teaching, especially with a student,
   would improve the page more than any other change. The same photos should
   go on the Google Business Profile.
6. **Reply time.** The contact section promises no reply time. If the coach
   reliably replies the same day, saying so on the site helps.
7. **Reviews.** The reference shows a star rating. Leave it out until there
   are real Google reviews, then show a few (with permission) in a section
   after "Why train with Soon Keat".

---

## 13. Definition of done

- [ ] All four pages plus the 404 page are built exactly to sections 4–6,
      using only the copy given.
- [ ] Checked by eye at **360px, 390px, 768px and 1280px** wide: no
      horizontal scroll, the floating WhatsApp button never covers content,
      the hero photo keeps the coach's face in frame, and the `<details>`
      menu opens and closes.
- [ ] Put side by side with `docs/design-reference/`, the pages read as the
      same design family: dark photo hero with wave, serif headings,
      eyebrow + H2 + subline headers, rounded cards with chips and a price
      row, an icon-tile feature grid, and the contact layout.
      Chromium and Playwright are installed in the cloud environment; take
      screenshots of each page at 390px and 1280px and look at them.
- [ ] Every WhatsApp button opens `wa.me/6588841034` with the right
      pre-typed message, in the right language.
- [ ] The language switch on every page goes to that page's counterpart
      (kids ⇄ kids, not kids → home).
- [ ] `pytest -q` and `ruff check .` are green; no new dependencies.
- [ ] CI (`.github/workflows/ci.yml`) is green on the PR.
- [ ] PR opened with the "Coach to confirm" list (section 12) and the
      Cloudflare setup steps linked.
