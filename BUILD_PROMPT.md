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

- Hand-written **HTML5 + one CSS file**. **No JavaScript at all**: FAQs use
  `<details>`, navigation uses anchor links. No framework, no bundler, no
  npm, no `package.json`, no Tailwind, no jQuery.
- Why: the coach cannot maintain a build chain, Cloudflare Pages serves a
  folder of files for free with nothing to build, and a page with no
  JavaScript and two photos loads almost instantly on a phone. Speed is a
  Google ranking factor.
- Fonts: **Montserrat 800** for English headings only, from Google Fonts
  (`display=swap`, with `preconnect`). Everything else uses the system font
  stack. Chinese pages use system Chinese fonts; **never load a web font for
  Chinese** (they are several MB).

  ```css
  --font-body: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial,
               "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans SC", sans-serif;
  --font-head: "Montserrat", var(--font-body);
  ```
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

docs/website.md               for the coach: how to change a price, how it deploys (section 11)
tests/test_website.py         guards (section 9)
.github/workflows/ci.yml      runs ruff + pytest on every push and PR (section 9)
CLAUDE.md                     already in the repo: update it (section 11)
```

Do not use the flyer's racquet-and-balls photo. It is a stock image with an
unknown licence and is not in the repo.

---

## 4. Design

### 4.1 Look and feel

The flyer is **royal blue + bright yellow**, with bold uppercase headings
and a tennis ball. Keep that identity so the flyer and the website clearly
belong to the same coach, but make it cleaner and more premium: plenty of
white space, one strong photo, and short text blocks.

```css
:root {
  --blue:        #1d5fd6;  /* flyer blue, darkened slightly so white text passes contrast */
  --blue-dark:   #0e2f6b;  /* headings on white, footer background */
  --ink:         #13213a;  /* body text */
  --muted:       #4a5873;  /* secondary text (must still be >= 4.5:1 on white) */
  --ball:        #e6f24a;  /* tennis-ball yellow: fills and highlights ONLY, never text on white */
  --ball-strong: #d4e31c;  /* hover state of yellow buttons */
  --paper:       #ffffff;
  --sand:        #f7f4ec;  /* alternating section background, echoes the flyer's cream pages */
  --line:        #dfe4ee;
  --radius:      14px;
}
```

- **Primary button** ("WhatsApp Coach"): `--ball` background, `--blue-dark`
  text, bold, a WhatsApp glyph as inline SVG, minimum 48px tall, full width
  on mobile. Yellow on navy/white stands out far more than WhatsApp green,
  and white-on-WhatsApp-green fails contrast.
- **Secondary button**: white/transparent with a 2px `--blue` border and
  `--blue` text.
- Headings: Montserrat 800. H1 and section eyebrows are uppercase; H2 and
  below are sentence case. On Chinese pages, headings are bold system font
  and not uppercased.
- Body text 17px/1.6 on mobile, 18px on desktop. Max line length 68ch.
- Light theme only; a marketing page does not need a dark mode.
- Every text/background pair must pass **WCAG AA** contrast. Visible focus
  ring (`outline: 3px solid var(--blue); outline-offset: 2px`) on every link
  and button.
- Respect `prefers-reduced-motion`. The only motion is a 150ms hover
  transition on buttons.

### 4.2 Layout: mobile first

Most visitors arrive on a phone from Google. Design at **360–390px wide
first**, then widen.

- Horizontal page padding 16px on mobile, 24px on tablet; content max width
  1120px.
- **No horizontal scrolling at any width from 320px up.**
- **Sticky bottom bar on mobile only (<768px)**: a full-width yellow
  "WhatsApp Coach" button pinned to the bottom of the screen
  (`position: sticky` inside a bottom wrapper, or `position: fixed` with
  `padding-bottom` on `body` so it never covers the footer). Include
  `env(safe-area-inset-bottom)` padding for iPhones. On desktop the header
  holds the button instead.
- Header: coach name as a text wordmark on the left ("Coach Soon Keat" /
  "陈顺杰教练", with a small yellow ball dot), then the language switch
  ("中文" / "EN") on the right, then (desktop only) anchor links to Prices,
  Coach, FAQ, plus the WhatsApp button. On mobile, show only the wordmark and
  the language switch. **No hamburger menu** (it would need JavaScript).

### 4.3 Home page sections, in order

Each section has an `id` for anchor links. Alternate `--paper` / `--sand`
backgrounds.

1. **Hero** (`#top`): on desktop, a two-column layout with the text on the
   left and `coach-forehand.jpg` on the right (rounded corners, a subtle
   yellow offset block behind it as a nod to the flyer's angled shapes). On
   mobile the photo sits above the text and is cropped with `object-fit:
   cover` and `aspect-ratio: 4/3`, `object-position: 60% 30%` so the
   coach's face and racquet stay in frame. Contents: eyebrow, H1, subline,
   a "From $50/hr" price chip, primary WhatsApp button, secondary "See
   prices" button (`#prices`). The hero image is the LCP element: give it
   `fetchpriority="high"`, **no** `loading="lazy"`, and explicit
   `width`/`height`.
2. **Credentials strip**: four short badges in a row (2×2 grid on mobile).
   Plain text with a small icon each; no carousel.
3. **Who it's for** (`#levels`): the flyer's four levels plus kids, as five
   cards. The kids card links to `/kids/`.
4. **Prices** (`#prices`): three cards (1-on-1, 2 people, group of 4). The
   2-person card is visually highlighted as "Popular with friends & couples".
   Under the cards, a list of what is included and what is not (racquets and
   balls provided; the court is booked and paid by the student). Each card has
   its own WhatsApp button with a pre-filled message naming that lesson type
   (section 5).
5. **How it works** (`#how`): three numbered steps.
6. **Meet your coach** (`#coach`): `malaysia-junior-davis-cup.jpg` plus the
   achievements list. Its caption says which photo it is so it is not
   mistaken for a current team photo.
7. **Where & when** (`#where`): the four areas as chips, plus the coaching
   hours. Plain text, no map.
8. **FAQ** (`#faq`): `<details>`/`<summary>` accordion, first item open.
9. **Final call to action**: a blue band with a short heading and the
   WhatsApp button.
10. **Footer**: contact (WhatsApp, `tel:` link, `mailto:` link), service
    areas, language switch, and "© 2026 Chan Soon Keat". The year is typed
    in the HTML, since the page has no JavaScript.

### 4.4 Kids page (`/kids/`, `/zh/kids/`)

A real page with its own content, not a copy of the home page (Google
ignores near-duplicates). Sections: hero (smaller, same photo), "How lessons
work for kids", "What to bring", prices (same three cards and numbers),
parent FAQ, final call to action. Include a breadcrumb link back to the home
page. Copy is in section 6.3 and 6.4.

### 4.5 404 page

Short and bilingual: "Page not found / 找不到此页面", with links to `/` and
`/zh/` and the WhatsApp button. Add `<meta name="robots" content="noindex">`.

---

## 5. Links and contact details (use exactly these)

- WhatsApp base: `https://wa.me/6588841034?text=` + URL-encoded message.
  Always `rel="noopener"`. Open in the same tab: on a phone it hands off to
  the app anyway.
- Pre-filled messages. Encode with `encodeURIComponent` semantics, so spaces
  become `%20`; do not use `+`.

  | Button | EN message | 中文 message |
  |---|---|---|
  | General (hero, sticky bar, final call to action, header) | `Hi Coach Soon Keat, I found your website and I'm interested in tennis lessons near Kovan.` | `陈教练您好，我在网站上看到您的网球课，想了解一下。` |
  | 1-on-1 card | `Hi Coach Soon Keat, I'm interested in a 1-on-1 tennis lesson.` | `陈教练您好，我想了解一对一网球课。` |
  | 2-person card | `Hi Coach Soon Keat, I'm interested in a 2-person tennis lesson.` | `陈教练您好，我想了解一对二网球课。` |
  | Group card | `Hi Coach Soon Keat, I'm interested in a group tennis lesson (4 people).` | `陈教练您好，我想了解4人团体网球课。` |
  | Kids page buttons | `Hi Coach Soon Keat, I'm interested in tennis lessons for my child.` | `陈教练您好，我想为孩子报名网球课。` |

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
- Eyebrow: `Kovan · Hougang · Serangoon · Bishan`
- H1: `Tennis lessons near Kovan`
- Subline: `Private and group coaching for complete beginners through to tournament players, from a former Malaysia junior national player. Adults, teenagers and kids welcome.`
- Price chip: `From $50/hr`
- Buttons: `WhatsApp Coach` · `See prices`

**Credentials strip**
- `Former Malaysia national player (U14 & U16)`
- `Tennis Malaysia Level 1 certified coach`
- `2023 STA Interclub Men's Champion`
- `Coaching since 2021`

**Who it's for**: H2 `Lessons for every level`
- **Newcomers**: `Never held a racquet? Start here. We cover grip, footwork and your first rallies, with no experience needed.`
- **Beginners**: `You've played a little and want your basics to feel solid: cleaner strokes, better consistency, and fixing the habits that hold you back.`
- **Recreational players**: `You've got the fundamentals and want to sharpen them with drills, match play and a hitting partner who pushes you.`
- **Competitive players**: `Tournament players who want high-intensity sparring and match preparation to stay sharp.`
- **Kids & teenagers**: `Patient, fun lessons that build real technique from the start.` Link text: `Tennis lessons for kids →` (to `/kids/`)

**Prices**: H2 `Simple, per-person pricing`
- Card 1, `1-on-1 private`: `$100` `/hour`. Bullets: `All the coach's attention on you`, `Lesson planned around your goals`.
- Card 2, `2 people`: `$70` `/hour per person`. Badge: `Popular with friends & couples`. Bullets: `Train with a friend, partner or family member`, `Plenty of rallying between the two of you`.
- Card 3, `Group of 4`: `$50` `/hour per person`. Bullets: `4 players per class`, `1-hour class`, `Great value for friends learning together`.
- Under the cards, heading `Good to know`:
  - `Racquets and balls are provided, so you don't need to buy anything to start.`
  - `All prices are per person.`
  - `You book and pay for the court. Condo courts and public courts are both fine.`
  - `Lesson times are flexible. Message to arrange.`

**How it works**: H2 `How it works`
1. `Message on WhatsApp`: `Tell the coach your level, how many people, and the days that suit you.`
2. `Pick a court and time`: `Book a court near you (your condo or a public court), and the coach will meet you there.`
3. `Play, then pay`: `Pay by PayNow after the lesson. No deposit, no package to buy.`

**Meet your coach**: H2 `Meet Coach Soon Keat`
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

**Where & when**: H2 `Where and when`
- `Lessons are held at a court you book, anywhere around:` then the chips `Kovan` `Hougang` `Serangoon` `Bishan`.
- `Somewhere else in Singapore? Ask, and it can often be arranged.`
- Hours: `Weekday evenings from 7pm · Weekends and public holidays from 7am · Lessons finish by 10pm`
- Lengths: `Lessons are usually 1 hour; 1.5 and 2 hours are available.`

**FAQ**: H2 `Questions`
1. `Do I need my own racquet?`: `No. Racquets and balls are provided. If you already have a racquet, bring it.`
2. `Who books the court?`: `You do. Book any court near you, such as your condo's court or a public court, and pay the court fee directly. The coach comes to you.`
3. `I've never played before. Is that OK?`: `Absolutely. Complete beginners are very welcome. The first lesson starts from how to hold the racquet.`
4. `How long is a lesson?`: `Usually 1 hour. 1.5-hour and 2-hour lessons are also available. Group classes are 1 hour.`
5. `When are lessons available?`: `Weekday evenings from 7pm, and from 7am on weekends and public holidays. Every lesson finishes by 10pm.`
6. `How do I pay?`: `By PayNow after the lesson. There's no deposit and no package to buy. You pay per lesson.`
7. `What if I need to cancel?`: `Cancel at least 3 days ahead and there's no charge. Closer to the day, just message the reason and the coach will sort it out fairly.`
8. `What happens if it rains?`: `The coach will check in with you before the lesson. A lesson cancelled because of rain is never charged.`
9. `Can I bring friends?`: `Yes. 2 people is $70/hour each, and a group of 4 is $50/hour each.`

**Final call to action**: H2 `Ready to get on court?` / text `Message Coach Soon Keat on WhatsApp. He usually replies the same day.` / button `WhatsApp Coach`

> "Usually replies the same day" is a promise. Keep it only if the coach
> confirms it in the PR; otherwise use `Message Coach Soon Keat on WhatsApp to arrange your first lesson.`
> **Default to the second version.**

### 6.2 中文 home (`/zh/`)

**`<title>`:** `高文网球课 | 一对一及团体网球教学 · 陈顺杰教练`

**Meta description:** `高文、后港、实龙岗、碧山一带网球课。前马来西亚青少年国手陈顺杰亲自执教，一对一、一对二及4人团体班，每小时$50起。WhatsApp 预约。`

**Hero**
- Eyebrow: `高文 · 后港 · 实龙岗 · 碧山`
- H1: `高文网球课`
- Subline: `由前马来西亚青少年国手亲自执教，从零基础到比赛选手都适合。欢迎成人、青少年及儿童报名。`
- Price chip: `每小时 $50 起`
- Buttons: `WhatsApp 联系教练` · `查看收费`

**Credentials strip**
- `前马来西亚国手（U14 & U16）`
- `马来西亚网球总会一级认证教练`
- `2023年新加坡网球协会俱乐部联赛男子组冠军`
- `2021年起执教`

**适合对象**: H2 `各个水平都能学`
- **新手**: `零基础也没问题：从握拍、步法到第一次来回对打，一步步教。`
- **初学者**: `已经学过一段时间，想打好基础：动作更规范、击球更稳定，针对性改进弱点。`
- **业余选手**: `基础扎实，想进一步提升：技术训练、实战对练、陪练，休闲又有进步。`
- **比赛选手**: `高强度对打与陪练，为比赛做准备、保持状态。`
- **儿童及青少年**: `耐心有趣的教学，从一开始就打好正确的技术基础。` Link: `儿童网球课 →` (to `/zh/kids/`)

**收费标准**: H2 `收费标准（按人计算）`
- `一对一私教`: `$100` `/小时`. Bullets: `教练全程专注于你`, `根据你的目标安排课程`.
- `一对二`: `$70` `/小时/人`. Badge: `适合朋友、情侣一起学`. Bullets: `和朋友或家人一起上课`, `两人之间有大量对打练习`.
- `4人团体班`: `$50` `/小时/人`. Bullets: `每班4人`, `每堂1小时`, `和朋友一起学，最划算`.
- `须知`:
  - `提供网球拍和网球，开始学不需要购买任何装备。`
  - `以上均为每人价格。`
  - `场地由学生自行预订及付费，公寓球场或公共球场都可以。`
  - `上课时间可商量，欢迎联系安排。`

**上课流程**: H2 `如何报名`
1. `WhatsApp 联系`: `告诉教练你的水平、人数和方便的时间。`
2. `订场地、定时间`: `在你附近预订球场（公寓或公共球场），教练到场上课。`
3. `上课后付款`: `课后用 PayNow 付款，无需订金，也不用买配套。`

**教练介绍**: H2 `认识陈顺杰教练`
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

**地点与时间**: H2 `上课地点与时间`
- `在你预订的球场上课，服务范围：` chips `高文` `后港` `实龙岗` `碧山`
- `其他地区？欢迎询问，通常都可以安排。`
- `平日晚上7点起 · 周末及公共假期早上7点起 · 晚上10点前结束`
- `一般每堂1小时，也可以上1.5小时或2小时。`

**FAQ**: H2 `常见问题`
1. `需要自己带球拍吗？`: `不需要，教练提供网球拍和网球。如果你有自己的球拍，也欢迎带来。`
2. `场地由谁预订？`: `由学生预订并支付场地费，公寓球场或公共球场都可以，教练会到场上课。`
3. `完全没打过网球可以吗？`: `当然可以！非常欢迎零基础的新手，第一堂课从握拍开始教。`
4. `每堂课多长时间？`: `一般1小时，也可以上1.5小时或2小时。团体班每堂1小时。`
5. `什么时候可以上课？`: `平日晚上7点起，周末及公共假期早上7点起，每堂课在晚上10点前结束。`
6. `怎么付款？`: `课后用 PayNow 付款。无需订金，也不用购买配套，每堂课单独付费。`
7. `如果需要取消怎么办？`: `提前3天或以上取消不收费。如果离上课时间较近，请告诉教练原因，教练会合理处理。`
8. `下雨怎么办？`: `教练会在上课前和你确认。因下雨取消的课程一律不收费。`
9. `可以和朋友一起上吗？`: `可以！一对二每人每小时$70，4人团体班每人每小时$50。`

**Final call to action**: H2 `准备好上场了吗？` / `WhatsApp 联系陈教练，安排你的第一堂课。` / button `WhatsApp 联系教练`

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
- Final call to action: H2 `Book your child's first lesson` / button `WhatsApp Coach`
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
- Final call to action: H2 `为孩子预约第一堂课` / button `WhatsApp 联系教练`

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
  `<meta name="theme-color" content="#1d5fd6">`.
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
   `application/ld+json`, and no `on*=` event-handler attributes. That keeps
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
6. **Same-day reply promise.** The final call to action uses the neutral
   version. If the coach does reply the same day, switch to the "usually
   replies the same day" line in 6.1.

---

## 13. Definition of done

- [ ] All four pages plus the 404 page are built exactly to sections 4–6,
      using only the copy given.
- [ ] Checked by eye at **360px, 390px, 768px and 1280px** wide: no
      horizontal scroll, the sticky WhatsApp bar shows on mobile only and
      never covers content, the hero photo keeps the coach's face in frame.
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
