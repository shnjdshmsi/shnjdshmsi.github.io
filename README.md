# shnjdshmsi.github.io — simple, Overleaf-connected personal website

A dependency-free rebuild of the previous Academic Pages (Jekyll) site.

- **No Ruby, no Gemfile, no Jekyll, nothing to install.** The site is plain
  HTML + one CSS file. Open `index.html` in a browser to preview locally.
- **The CV is driven by LaTeX.** `cv/cv.tex` is the single source of truth.
  On every push, GitHub Actions compiles it to PDF (`files/cv_shnjdshmsi.pdf`),
  converts it to HTML (`cv.html`), and redeploys the site.
- **Overleaf connection.** Link this repo to Overleaf (GitHub Sync) so that
  pushing from Overleaf updates the website automatically.

## Repository layout

```
index.html            About page (edit directly)
publications.html     Publications (edit directly)
experience.html       Experience (edit directly)
awards.html           Awards (edit directly)
teaching.html         Teaching (edit directly)
cv.html               AUTO-GENERATED from cv/cv.tex — do not edit by hand
assets/style.css      All styling
images/               Profile photo etc.
cv/cv.tex             THE CV SOURCE — edit in Overleaf (or anywhere)
scripts/build_cv.py   tex -> HTML converter used by the workflow
.github/workflows/    Build & deploy pipeline
```

## One-time setup

1. **Create the repo.** On GitHub, create a repository named
   `shnjdshmsi.github.io` (delete or rename the old one first, or push this
   over it). Upload all files from this folder, including the hidden
   `.github` directory.

2. **Enable GitHub Pages via Actions.** Repo → *Settings* → *Pages* →
   *Build and deployment* → **Source: GitHub Actions**.

3. **Trigger the first build.** Any push triggers it, or go to
   *Actions* → *Build & Deploy Website* → *Run workflow*. After ~2 minutes
   the site is live at `https://shnjdshmsi.github.io`.

## Connecting Overleaf

Overleaf GitHub Sync is a **premium** feature (included in Overleaf Standard/
Professional, group subscriptions, and Overleaf Commons via many universities
— check if McGill/Mila gives you premium access).

Overleaf cannot link an *existing* Overleaf project to an *existing* GitHub
repo, so create the Overleaf project **from this repo**:

1. In Overleaf: *Account Settings* → link your GitHub account.
2. *New Project* → *Import from GitHub* → choose `shnjdshmsi/shnjdshmsi.github.io`.
3. In the project, open `cv/cv.tex` and set it as the main document
   (Menu → Main document → `cv/cv.tex`).
4. Paste in your real CV content (replace the starter file entirely if you
   like — any class that compiles on Overleaf will compile in the Action;
   if it needs XeLaTeX, uncomment `latexmk_use_xelatex: true` in
   `.github/workflows/build-deploy.yml`). If your CV uses extra files
   (a `.cls`, `.bib`, photo), put them in the `cv/` folder too.
5. Whenever you finish editing: **Menu → GitHub → Push Overleaf changes to
   GitHub**. That push triggers the workflow, and within ~2 minutes the
   website's CV page and PDF are updated.

**No Overleaf premium?** The pipeline works identically — just update
`cv/cv.tex` another way: edit it directly on github.com (pencil icon), or in
Overleaf choose *Menu → Source (download .zip)*, then drag the updated
`cv.tex` onto the `cv/` folder on GitHub. Every commit rebuilds the site.

## Editing everything else

The other pages are plain HTML — edit them on github.com or locally and
commit. The sidebar and nav are repeated at the top of each page; if you
change them (new link, new photo), update each file (a 30-second
find-and-replace).

## How the CV page is rendered

`scripts/build_cv.py` first tries `pandoc` to convert your `.tex` to HTML so
the CV appears as a normal web page. Highly customized CV classes
(moderncv, awesome-cv) often can't be converted meaningfully; in that case
the script automatically falls back to embedding the freshly compiled PDF on
the page. Either way, the site always shows exactly what's in `cv/cv.tex`.
