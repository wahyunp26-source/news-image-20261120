# News in One Image — Friday 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/wahyunp26-source/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/wahyunp26-source/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Referral: `amzcd6wq`

A single-day newspaper front page for **Friday 20 November 2026**: 38 verified
stories across 6 continents plus space, every feature story with its own
matching illustration, a world map with numbered pins, 24 more one-line
briefs, and a DATE CHECK that lists the big Thursday-first stories left out
on purpose.

## What happened that day

- **Cyclone Akvan** makes landfall near Gopalpur, Odisha — 300,000+ evacuated.
- **Kyiv** hit by an overnight ballistic-missile attack; 3 Dnipro bridges damaged.
- **COP31** in Antalya ends in deadlock as fossil-fuel language is cut.
- **Asia shares plunge** — Nikkei −4.1%, Kospi −4.7%, the worst week since 2020.
- **Japan CPI** 2.3%; **Phillips 118** lifts New Zealand to 368 vs India;
  **Russell fastest** in a wet Las Vegas FP2; Brazil recognises Chief Raoni's
  ancestral land; and Mercury puts on its best evening show before
  BepiColombo's capture begins on Saturday.

## How it is built

- `main.py` — stdlib-only entrypoint: copies `entry.png` to the output dir.
- `build.py` — build-time compositor (Pillow): lays out the page from the
  illustrations in `assets/` using Liberation Sans / Liberation Serif.
- `assets/` — 14 feature illustrations + 1 world map, generated for this entry.
- `entry.png` — the finished 1024×1024 page (JPEG bytes, ≤ 1 MiB).

Run: `python3 main.py` (writes `/output/entry.png`; set
`MAKEFUN_OUTPUT_DIR` to change the destination). Run twice — byte-identical.
