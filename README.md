# The World in One Image — 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/xiami1020/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/xiami1020/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-page newspaper front page that sums up Saturday 21 November 2026
in a single 1024×1024 image. No photographs, no fetched assets — every
line and letter is drawn in code.

## What's on the page

- **Lead — Ukraine and Poland:** Russia's biggest November barrage, 404
  drones and 111 missiles, kills at least eight in Kyiv; two missiles and
  a drone come down in Poland.
- **Justice — The Hague:** the World Court finds Myanmar committed genocide
  against the Rohingya, the first such ruling against a state.
- **Markets — New York:** an AI sell-off drags the S&P 500 into correction,
  days after Anthropic's $2 trillion market debut.
- **Climate — Antalya:** COP31 runs past its deadline as fossil-fuel
  language falls out of the draft deal.
- **Diplomacy — Shenzhen:** Trump, Xi and Putin sign a four-point peace
  declaration that says nothing about Ukraine.
- **Health — London:** a trial pill, daraxonrasib, makes pancreatic tumours
  undetectable in one in 12 patients.

All facts were checked against same-day reporting (AP, NYT, One Turn,
Majik Brief) before drawing.

## How it is made

- `main.py` — entry point. Renders the page and writes the PNG.
- `generate.py` — all drawing: masthead, lead story, stat strip,
  two-column story grid, "in brief" box and source line.
- The only dependency is Pillow. No network, no clock, no randomness,
  so the output is byte-identical on every run.

## Run it

```sh
python3 main.py
```

This writes `entry.png` (1024×1024, under 1 MiB) next to `main.py`,
and also to `output/entry.png` and `/output/entry.png`.

## Licence

MIT — see `LICENSE`.
