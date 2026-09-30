# How to look at the website on your own computer

Use this to check a change before you publish it. It works on Windows and needs
nothing except Python, which you already have.

**Do not double-click `index.html`.** The pages load their style and photos from
paths like `/css/site.css`, which only work when the site is served properly.
Opened as a plain file, the page shows up as unstyled black text.

## Steps (Windows)

1. Get the latest `site` folder.
   - From Claude: download the zip it sends you and right-click it, then choose
     **Extract All**.
   - From GitHub: open the repository, click **Code**, then **Download ZIP**,
     and extract it. The folder you want is the one called `site`.
2. Open the `site` folder in **File Explorer**. You should see `index.html`,
   and folders called `css`, `img`, `kids` and `zh`.
3. Click the **address bar** at the top of File Explorer, type `cmd` and press
   **Enter**. A black window opens already inside that folder.
4. In the black window, type this and press **Enter**:

   ```
   python -m http.server 8000
   ```

   If it says `python` is not recognised, type `py -m http.server 8000`
   instead. The window then says "Serving HTTP on ...". Leave it open.
5. Open your browser and go to **http://localhost:8000**.
6. When you are finished, click the black window and press **Ctrl+C**, then
   close it.

## Pages to check

| Address | What it is |
|---|---|
| http://localhost:8000/ | English home page |
| http://localhost:8000/zh/ | Chinese home page |
| http://localhost:8000/kids/ | English kids page |
| http://localhost:8000/zh/kids/ | Chinese kids page |
| http://localhost:8000/nope | The "page not found" page |

To see how it looks on a phone, press **F12** in the browser, then click the
small phone-and-tablet icon at the top of the panel that opens.

## If something looks wrong

- **You see a list of file names instead of the website.** The black window is
  in the wrong folder. Press Ctrl+C, close it, and redo steps 3 and 4 from
  inside the `site` folder. You should see `index.html` in that list if you
  are in the right place.
- **The page has no colours or photos.** You opened the file by double-clicking
  it. Use http://localhost:8000 as in step 5.
- **You see an old version.** Press **Ctrl+F5** in the browser to reload it,
  or extract a fresh copy of the folder.
- **The headings look plain.** The fancy heading font loads from Google Fonts,
  so it needs an internet connection. Everything else works offline.
- **Nothing happens at step 4, or "Address already in use".** An earlier
  window is still running. Close all black windows and try again, or use a
  different number, for example `python -m http.server 8080` and then
  http://localhost:8080.

The WhatsApp buttons on your local copy still open the real chat, so only tap
them if you want to.
