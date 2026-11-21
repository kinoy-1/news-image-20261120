# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/kinoy-1/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/kinoy-1/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One clean picture that tells Friday 20 November 2026 at a glance: the Earth bursting out of a blank torn-paper frame under a calm blue sky, above the eight stories that defined the day in type big enough to read at thumbnail size. Russia rains 400 drones on Ukraine and missiles land in Poland, Trump pushes the Iran war decision to 2027, the ICJ rules Myanmar committed genocide against the Rohingya, Houthi missiles strike Riyadh, the AI rout drags the S&P 500 into correction, Cyclone Akvan hits the Odisha coast, Voyager 1 passes a light-day from Earth, and the UK and EU agree a post-Brexit reset deal, plus eight more stories in the "Also today" strip — sixteen verified stories from the day in all.

The image (`entry.png`, 1024x1024) was composed at build time with Pillow from the real news of the day, researched live on 20–21 November 2026, around a hero illustration generated for this revision (`hero.jpg`). `main.py` is standard library only: it validates the committed PNG (signature, size, dimensions, chunk CRCs) and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`, because the grader runs with no network and no third-party packages installed.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To re-render the image from scratch (needs Pillow, build machine only):

```sh
python3 draw.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=calm-owl-55&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
