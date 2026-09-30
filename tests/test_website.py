"""Guards for the public website in site/.

Everything in site/ is published to the internet on every merge to main, so
these tests are the only thing standing between a typo and the live site. They
use the standard library only, so CI needs nothing beyond pytest.
"""
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

SITE = "https://kovan-tennis.pages.dev"
WHATSAPP = "6588841034"
PAGES = {  # path on the site -> file in site/
    "/": "index.html", "/kids/": "kids/index.html",
    "/zh/": "zh/index.html", "/zh/kids/": "zh/kids/index.html",
}
PAIRS = [("/", "/zh/"), ("/kids/", "/zh/kids/")]
PRICES = {"solo": 100, "pair_pp": 70, "group_pp": 50}   # the flyer prices, per person per hour

ROOT = Path(__file__).resolve().parent.parent / "site"


class Page(HTMLParser):
    """Collects the parts of a page the tests care about."""

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tags = []          # (tag, attrs dict)
        self.text = []          # visible text
        self.title = ""
        self.jsonld = []
        self._stack = []
        self._skip = 0
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        self._stack.append(tag)
        if tag in ("script", "style"):
            self._skip += 1
            self._script_type = attrs.get("type")
            self._buf = []

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
            if tag == "script" and self._script_type == "application/ld+json":
                self.jsonld.append("".join(self._buf))
        if self._stack and self._stack[-1] == tag:
            self._stack.pop()

    def handle_data(self, data):
        if self._skip:
            self._buf.append(data)
        elif self._stack and self._stack[-1] == "title":
            self.title += data
        else:
            self.text.append(data)

    def find(self, tag):
        return [a for t, a in self.tags if t == tag]

    def meta(self, key, value="name"):
        for a in self.find("meta"):
            if a.get(value) == key:
                return a.get("content", "")
        return None

    def links(self, rel):
        return [a for a in self.find("link") if a.get("rel") == rel]

    @property
    def visible_text(self):
        return " ".join(" ".join(self.text).split())


def load(path):
    return Page((ROOT / PAGES[path]).read_text(encoding="utf-8"))


def all_pages():
    return {p: load(p) for p in PAGES}


def all_files():
    return [PAGES[p] for p in PAGES] + ["404.html"]


def resolve(url_path):
    """Map an internal URL path to the file Cloudflare would serve."""
    path = urlparse(url_path).path
    target = ROOT / path.lstrip("/")
    if path.endswith("/"):
        target = target / "index.html"
    return target


class TestPagesExist:
    """A page that goes missing is a broken link on the live site, so every file the spec names must exist."""

    def test_content_pages_and_support_files(self):
        expected = list(PAGES.values()) + [
            "404.html", "css/site.css", "robots.txt", "sitemap.xml", "_headers", "img/favicon.svg",
        ]
        missing = [f for f in expected if not (ROOT / f).is_file()]
        assert not missing, missing


class TestHeadTags:
    """Search engines read these tags first; a duplicate h1 or a missing canonical quietly costs ranking."""

    def test_exactly_one_h1(self):
        for path, page in all_pages().items():
            assert len(page.find("h1")) == 1, path

    def test_title_present_and_short(self):
        for path, page in all_pages().items():
            title = page.title.strip()
            assert title, path
            assert len(title) <= 65, (path, len(title))

    def test_meta_description_length(self):
        # English is capped where the spec's own copy ends. Chinese carries more per
        # character and Google truncates by width, so it gets a shorter window.
        for path, page in all_pages().items():
            n = len(page.meta("description") or "")
            low, high = (45, 120) if path.startswith("/zh/") else (70, 185)
            assert low <= n <= high, (path, n)

    def test_lang_attribute(self):
        for path, page in all_pages().items():
            want = "zh-Hans" if path.startswith("/zh/") else "en"
            assert page.find("html")[0].get("lang") == want, path

    def test_viewport(self):
        for path, page in all_pages().items():
            assert "width=device-width" in (page.meta("viewport") or ""), path

    def test_canonical(self):
        for path, page in all_pages().items():
            canon = page.links("canonical")
            assert len(canon) == 1, path
            assert canon[0]["href"] == SITE + path, path

    def test_404_is_noindex(self):
        page = Page((ROOT / "404.html").read_text(encoding="utf-8"))
        assert "noindex" in (page.meta("robots") or "")


class TestHreflang:
    """Without reciprocal hreflang links Google may treat the Chinese pages as duplicates of the English ones."""

    def test_pairs_link_to_each_other_and_themselves(self):
        pages = all_pages()
        for en, zh in PAIRS:
            for path in (en, zh):
                alts = {a["hreflang"]: a["href"] for a in pages[path].links("alternate") if "hreflang" in a}
                assert alts.get("en") == SITE + en, path
                assert alts.get("zh-Hans") == SITE + zh, path
                assert alts.get("x-default") == SITE + en, path
                assert all(h.startswith(SITE) for h in alts.values()), path

    def test_language_switch_goes_to_the_counterpart(self):
        pages = all_pages()
        for en, zh in PAIRS:
            for here, there in ((en, zh), (zh, en)):
                hrefs = [a["href"] for a in pages[here].find("a") if a.get("hreflang")]
                assert hrefs and set(hrefs) == {there}, here


class TestLinks:
    """A dead internal link or a malformed WhatsApp link means a lost customer, so both are checked on every page."""

    def test_internal_links_resolve(self):
        for name in all_files():
            page = Page((ROOT / name).read_text(encoding="utf-8"))
            for tag, attr in (("a", "href"), ("link", "href"), ("img", "src")):
                for a in page.find(tag):
                    url = a.get(attr, "")
                    if url.startswith("/"):
                        assert resolve(url).is_file(), (name, url)

    def test_no_insecure_links(self):
        for name in all_files():
            assert "http://" not in (ROOT / name).read_text(encoding="utf-8").replace(
                "http://www.w3.org/", ""), name

    def test_whatsapp_links(self):
        prefix = f"https://wa.me/{WHATSAPP}?text="
        for path, page in all_pages().items():
            wa = [a["href"] for a in page.find("a") if "wa.me" in a.get("href", "")]
            assert len(wa) >= 2, path
            for href in wa:
                assert href.startswith(prefix), (path, href)
                assert "+" not in href, (path, href)
                text = unquote(href[len(prefix):])
                assert text.strip(), (path, href)
                assert parse_qs(urlparse(href).query)["text"] == [text], (path, href)

    def test_whatsapp_links_open_safely(self):
        for path, page in all_pages().items():
            for a in page.find("a"):
                if "wa.me" in a.get("href", ""):
                    assert "noopener" in a.get("rel", ""), path

    def test_whatsapp_message_matches_page_language(self):
        for path, page in all_pages().items():
            for a in page.find("a"):
                if "wa.me" in a.get("href", ""):
                    text = unquote(urlparse(a["href"]).query[5:])
                    has_han = bool(re.search(r"[一-鿿]", text))
                    assert has_han == path.startswith("/zh/"), (path, text)

    def test_kids_pages_only_send_the_kids_message(self):
        for path in ("/kids/", "/zh/kids/"):
            page = load(path)
            texts = {unquote(urlparse(a["href"]).query[5:]) for a in page.find("a") if "wa.me" in a.get("href", "")}
            assert len(texts) == 1, (path, texts)


class TestImages:
    """Images without alt text or dimensions hurt accessibility, SEO and layout stability."""

    def test_alt_width_height_and_file(self):
        for name in all_files():
            page = Page((ROOT / name).read_text(encoding="utf-8"))
            for img in page.find("img"):
                for key in ("alt", "width", "height"):
                    assert img.get(key, "").strip(), (name, key)
                assert resolve(img["src"]).is_file(), (name, img["src"])

    def test_only_the_hero_loads_eagerly(self):
        for path, page in all_pages().items():
            for img in page.find("img"):
                if "coach-forehand" in img["src"]:
                    assert img.get("fetchpriority") == "high", path
                    assert "loading" not in img, path
                else:
                    assert img.get("loading") == "lazy", path
                    assert img.get("decoding") == "async", path


class TestStructuredData:
    """Broken or invented structured data can get the site penalised, so it must parse and stay honest."""

    def test_blocks_parse(self):
        for path, page in all_pages().items():
            assert page.jsonld, path
            for block in page.jsonld:
                json.loads(block)

    def test_local_business(self):
        for path in ("/", "/zh/"):
            data = json.loads(load(path).jsonld[0])
            assert data["@type"] == "LocalBusiness"
            assert data["telephone"] == "+6588841034"
            offers = [int(o["price"]) for o in data["hasOfferCatalog"]["itemListElement"]]
            assert offers == [PRICES["solo"], PRICES["pair_pp"], PRICES["group_pp"]], path
            for banned in ("address", "aggregateRating", "review", "@graph"):
                assert banned not in data, (path, banned)

    def test_kids_pages_only_have_breadcrumbs(self):
        for path in ("/kids/", "/zh/kids/"):
            blocks = [json.loads(b) for b in load(path).jsonld]
            assert [b["@type"] for b in blocks] == ["BreadcrumbList"], path


class TestPricesAgree:
    """Prices are typed by hand on four pages; this stops one page being updated and the others forgotten."""

    def test_all_prices_on_every_page(self):
        for path, page in all_pages().items():
            text = page.visible_text
            for amount in PRICES.values():
                assert f"${amount}" in text, (path, amount)

    def test_no_other_dollar_amounts(self):
        allowed = {f"${v}" for v in PRICES.values()}
        for path, page in all_pages().items():
            found = set(re.findall(r"\$\s?\d[\d,.]*", page.visible_text))
            assert found <= allowed, (path, found - allowed)
            desc = set(re.findall(r"\$\s?\d[\d,.]*", page.meta("description") or ""))
            assert desc <= allowed, (path, desc - allowed)


class TestNoScripts:
    """The site promises no JavaScript and no inline styles, and the CSP in _headers depends on that."""

    def test_no_scripts_except_json_ld(self):
        for name in all_files():
            page = Page((ROOT / name).read_text(encoding="utf-8"))
            for s in page.find("script"):
                assert s.get("type") == "application/ld+json", name

    def test_no_event_handlers_or_inline_styles(self):
        for name in all_files():
            page = Page((ROOT / name).read_text(encoding="utf-8"))
            assert not page.find("style"), name
            for tag, attrs in page.tags:
                bad = [k for k in attrs if k.startswith("on") or k == "style"]
                assert not bad, (name, tag, bad)

    def test_csp_still_blocks_scripts(self):
        headers = (ROOT / "_headers").read_text(encoding="utf-8")
        assert "script-src 'none'" in headers
        assert "unsafe-inline" not in headers


class TestSitemap:
    """The sitemap is how Google finds the Chinese pages, so it must list every page and only those."""

    def test_lists_every_page(self):
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        locs = sorted(e.text for e in root.findall("s:url/s:loc", ns))
        assert locs == sorted(SITE + p for p in PAGES)

    def test_robots_names_the_sitemap(self):
        assert f"Sitemap: {SITE}/sitemap.xml" in (ROOT / "robots.txt").read_text(encoding="utf-8")


class TestNoStaleOrWrongCopy:
    """Typos from the flyer and anything that counts years go out of date by itself, so they are banned outright."""

    BANNED = ["SUNNIG", "newsport", "years of experience", "years of coaching", "5 years", "五年",
              "TODO", "lorem", "S$"]

    def test_banned_strings(self):
        for name in all_files():
            text = (ROOT / name).read_text(encoding="utf-8")
            lowered = text.lower()
            for word in self.BANNED:
                assert word.lower() not in lowered, (name, word)

    def test_no_minimum_age_and_no_invented_proof(self):
        for name in all_files():
            text = (ROOT / name).read_text(encoding="utf-8").lower()
            for word in ("aggregaterating", "★", "reviews", "google-site-verification\" content"):
                assert word not in text, (name, word)
            assert not re.search(r"\b(from|aged?)\s+(age\s+)?\d+\b", text), name


class TestOnlyPublicFilesInWebsite:
    """Everything in site/ becomes a public URL, so nothing but web files may live there."""

    ALLOWED = {".html", ".css", ".jpg", ".svg", ".txt", ".xml"}

    def test_only_web_files(self):
        for f in ROOT.rglob("*"):
            if f.is_file() and f.name != "_headers":
                assert f.suffix in self.ALLOWED, f.relative_to(ROOT)
