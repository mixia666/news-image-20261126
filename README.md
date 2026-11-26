# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/mixia666/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/mixia666/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A one-page broadsheet that sums up the world news of Thursday 26 November 2026 in a single 1024x1024 image: two more tankers hit mines in the Strait of Hormuz beneath AI-generated woodcut front-page art, new U.S. tariffs on 14 trading partners, a Houthi strike on Saudi Arabia's Ras Tanura refinery, missiles over Kyiv, Kim Jong Un's nuclear vow, and the day's other leading stories. `draw.py` composes `entry.png` from the day's reporting; `main.ts` copies it to the output path.

## Run it

```sh
python3 draw.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`draw.py` is deterministic — the same `hero.png` and story text give the same `entry.png` bytes on every run — and `main.ts` checks the image against the gate's caps (PNG or JPEG, at most 1 MiB, at most 1024x1024) before copying it to the output path.

## Stories covered

All reported on Thursday 26 November 2026: two more tankers hit mines in the Strait of Hormuz (Reuters, Arab News); the Houthis say they hit Saudi Arabia's Ras Tanura refinery (Reuters); Trump's new tariffs on 14 trading partners (The Economic Times, The Japan Times); Israeli strikes kill nine in Gaza (Morning Briefing); Russian missiles hit Kyiv and grain ships near Odesa (Morning Briefing, The Japan Times); Kim Jong Un vows more nuclear weapons (The Japan Times); Brent near $95, gold at 15-month lows (Reuters, IQMIA). The front-page art is an AI-generated woodcut-style illustration of the lead story.

---

<sub>Entered on [make.fun](https://make.fun/?ref=vd2s8rmr&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
