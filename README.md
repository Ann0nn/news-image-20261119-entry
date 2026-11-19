# news-image-20261119-entry

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Ann0nn/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Ann0nn/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A single image that sums up Thursday 19 November 2026, entered in the make.fun news-image-20261119 bounty. It is laid out as a newspaper front page. The lead story is the first-ever three-way summit between Trump, Xi and Putin in Shenzhen; below it, the World Court's genocide ruling against Myanmar, Anthropic's record $81.3bn IPO, Ukraine's third strike on the Crimean Bridge, and tankers burning near the Strait of Hormuz, plus six more briefs from the day. All of it was checked against reporting published on 19 November 2026 (AA, Reuters, Al Jazeera, Japan Times).

How it works: `src/render.py` draws `entry.png` with Python and Pillow, and `main.ts` (Node 22, standard library only, no network) reads that file and writes it to `/output/entry.png`, so every run produces identical bytes.

## Run the entry

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Redraw the image from source

```sh
python3 src/render.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=s27wgn68&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
