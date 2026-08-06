#!/usr/bin/env python3
"""
Convert cv/cv.tex into cv.html for the website.

Usage:
    python3 scripts/build_cv.py <path/to/cv.tex> <path/to/output/cv.html>

Strategy:
  1. Try `pandoc cv.tex -f latex -t html` to render the CV as HTML.
  2. If pandoc produces meaningful content, publish it (plus a
     "Download PDF" button).
  3. If pandoc can't make sense of the document (heavily customized
     classes such as moderncv / awesome-cv often defeat it), fall back
     to embedding the compiled PDF directly on the page. Either way
     the page always reflects the latest push from Overleaf.

No third-party Python packages required.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

MIN_VISIBLE_CHARS = 300  # below this, pandoc output is considered junk

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CV - Shayan Nejadshamsi</title>
<meta name="description" content="Curriculum Vitae of Shayan Nejadshamsi">
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/jpswalsh/academicons@1/css/academicons.min.css">
</head>
<body>

<header class="masthead">
  <div class="masthead-inner">
    <a class="site-title" href="index.html">Shayan Nejadshamsi</a>
    <nav class="site-nav">
      <a href="index.html">About</a>
      <a href="publications.html">Publications</a>
      <a href="experience.html">Experience</a>
      <a href="awards.html">Awards</a>
      <a href="teaching.html">Teaching</a>
      <a href="cv.html" class="active">CV</a>
    </nav>
  </div>
</header>

<div class="page-wrap">

  <aside class="sidebar">
    <div class="author-avatar">
      <img src="images/shnjdshmsi.jpg" alt="Shayan Nejadshamsi">
    </div>
    <div class="author-info">
      <h3 class="author-name">Shayan Nejadshamsi</h3>
      <p class="author-bio">Machine Learning Researcher<br>x.nejadshamsi@mcgill.ca, x=shayan</p>
      <ul class="author-links">
        <li><i class="fa-solid fa-location-dot"></i> Toronto, ON, Canada</li>
        <li><i class="fa-solid fa-building-columns"></i> Mila (Quebec AI Institute)</li>
        <li><a href="https://scholar.google.com/citations?hl=en&amp;user=3Gj_NTIAAAAJ&amp;view_op=list_works&amp;sortby=pubdate" target="_blank" rel="noopener"><i class="ai ai-google-scholar"></i> Google Scholar</a></li>
        <li><a href="https://orcid.org/0000-0002-7501-8016" target="_blank" rel="noopener"><i class="ai ai-orcid"></i> ORCID</a></li>
        <li><a href="https://github.com/shnjdshmsi" target="_blank" rel="noopener"><i class="fa-brands fa-github"></i> GitHub</a></li>
        <li><a href="https://www.linkedin.com/in/shnjdshmsi" target="_blank" rel="noopener"><i class="fa-brands fa-linkedin"></i> LinkedIn</a></li>
        <li><a href="https://twitter.com/shnjdshmsi" target="_blank" rel="noopener"><i class="fa-brands fa-x-twitter"></i> Twitter</a></li>
        <li><a href="files/cv_shnjdshmsi.pdf" target="_blank" rel="noopener"><i class="fa-solid fa-file-pdf"></i> CV (PDF)</a></li>
      </ul>
    </div>
  </aside>

  <main class="page-content">
<h1 class="page-title">Curriculum Vitae</h1>
<p><a class="btn" href="files/cv_shnjdshmsi.pdf" target="_blank" rel="noopener">
<i class="fa-solid fa-file-pdf"></i>&nbsp; Download CV (PDF)</a></p>
{BODY}
  </main>

</div>

<footer class="site-footer">
  <div class="site-footer-inner">
    &copy; 2026 Shayan Nejadshamsi. Hosted on GitHub Pages. This page is auto-generated from cv/cv.tex.
  </div>
</footer>

</body>
</html>
"""

PDF_FALLBACK = """
<p>The CV below is compiled automatically from the LaTeX source on every update.</p>
<object class="cv-embed" data="files/cv_shnjdshmsi.pdf" type="application/pdf">
  <p>Your browser cannot display embedded PDFs.
  <a href="files/cv_shnjdshmsi.pdf">Download the CV instead</a>.</p>
</object>
"""


def visible_text_len(fragment: str) -> int:
    return len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", fragment)).strip())


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    tex_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])

    body = None
    try:
        result = subprocess.run(
            ["pandoc", str(tex_path), "-f", "latex", "-t", "html", "--wrap=none"],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0 and visible_text_len(result.stdout) >= MIN_VISIBLE_CHARS:
            body = f'<div class="cv-generated">\n{result.stdout}\n</div>'
            print(f"pandoc conversion OK ({visible_text_len(result.stdout)} visible chars)")
        else:
            print("pandoc output too thin or failed; falling back to embedded PDF")
            if result.stderr:
                print(result.stderr[:2000])
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        print(f"pandoc unavailable ({exc}); falling back to embedded PDF")

    if body is None:
        body = PDF_FALLBACK

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(PAGE_TEMPLATE.replace("{BODY}", body), encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
