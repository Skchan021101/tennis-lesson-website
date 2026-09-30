# The website: what you do by hand

This is for Coach Soon Keat. You do not need to write any code. Where a step
says "ask Claude", open this repository in Claude and type what is in the
quotes.

The site is plain files in the `site/` folder. There is nothing to install and
nothing to build.

**Unlike the Telegram bot, the website goes live the moment a change is
merged.** Merging a pull request that touches `site/` publishes it within a
minute or two. Nothing else is involved (no server, no `deploy.sh`). Every pull
request also gets its own preview link from Cloudflare, so you can check a
change on your phone before you merge it.

## A. Put the site online: Cloudflare Pages (free, about 10 minutes, once)

1. Sign up at dash.cloudflare.com and choose the free plan.
2. Click **Workers & Pages**, then **Create**, then **Pages**, then
   **Connect to Git**. Authorise GitHub when asked, then choose the
   `tennis-lesson-website` repository. Cloudflare can read a private
   repository. The repository stays private, and only the `site` folder is
   published.
3. For **Project name** type `kovan-tennis`. **If that name is taken**, pick
   another one, then ask Claude: "Replace kovan-tennis.pages.dev with
   my-new-name.pages.dev everywhere." (The tests fail until every page matches.)
4. Set **Production branch** to `main`. Set **Framework preset** to **None**.
   Leave **Build command** empty. Set **Build output directory** to `site`.
5. Click **Save and Deploy**. The site is live at
   `https://kovan-tennis.pages.dev` within a minute.
6. Open your project, click **Metrics**, then **Web Analytics**, then
   **Enable**. This counts visitors without cookies, so no cookie banner is
   needed.

## B. Tell Google the site exists: Search Console (free, about 10 minutes, once)

1. Go to search.google.com/search-console and click **Add property**. Choose
   **URL prefix** and type `https://kovan-tennis.pages.dev/`.
2. Choose **HTML tag** as the verification method and copy the `<meta ...>`
   tag it shows you. Ask Claude: "Put this Search Console tag in
   `site/index.html` in place of the comment", and paste the tag. Merge the
   pull request, wait a minute, then click **Verify**.
3. Click **Sitemaps** and submit `sitemap.xml`.
4. Click **URL inspection**, paste the home page address, and click **Request
   indexing**. Do the same for `https://kovan-tennis.pages.dev/zh/` and
   `https://kovan-tennis.pages.dev/kids/`.
5. Expect it to take 1 to 4 weeks before the site shows up in searches. That is
   normal.

Be realistic: a new site on a free `pages.dev` address will not reach page one
for a plain "tennis lessons" search against big academies. What it can win, over
weeks, is the local searches such as "tennis lessons Kovan", "kids tennis
lessons Serangoon" and "高文 网球课".

## C. Get on Google Maps: Google Business Profile (free, the biggest win for "near Kovan")

1. Go to business.google.com and click **Add business**. Type the name
   `Coach Soon Keat Tennis Lessons`.
2. For the category choose **Tennis instructor**. If it is not offered, choose
   **Sports school**.
3. When it asks "Do you want to add a location customers can visit?", answer
   **No**, because you go to the student's court. Add the service areas:
   Kovan, Hougang, Serangoon and Bishan.
4. Enter the phone number +65 8884 1034 and the website
   `https://kovan-tennis.pages.dev/`.
5. Verify the business. Google may ask for a short video of you coaching and
   some proof of the business, such as the flyer or a PayNow receipt. Follow
   its prompts.
6. Add your services with the three prices, your hours (weekday evenings
   7pm to 10pm, weekends 7am to 10pm), and at least 5 photos of you coaching.
7. **Ask every happy student for a Google review.** Reviews are the strongest
   signal for local searches, and the site can show real ones later. Send the
   review link on WhatsApp after a good lesson.
8. Never make up a review, and never ask friends who have not trained with you
   to write one. Google removes them and can suspend the listing.

## D. Change a price later

Ask Claude: "Change the 2-person price to $80." Claude edits the numbers in
all four pages, the search-engine data on both home pages, and the price list
in `tests/test_website.py`. The tests fail if any one of them is missed.

**Then also change the bot**, or a client is quoted one price on the website and
another by the bot. The bot stores the *total* for 2 and 4 people, so for the
current website prices send it:

- `/setrate solo 100`
- `/setrate semi 140`
- `/setrate group 200`

Then send `/rates` to check.

## E. Check a change before it goes live

1. Open the pull request on GitHub and look for the Cloudflare comment with a
   **Preview** link.
2. Open that link on your phone. Tap **WhatsApp Coach** and check the message
   is already typed in.
3. Tap **中文** and check it opens the matching Chinese page.
4. If it looks right, merge the pull request. It is live a minute or two later.
