# The World in One Day — 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/mixia666/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/mixia666/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![make.fun](https://make.fun/badge.svg)](https://make.fun/bounty/news-image-20261126)
[![owner](https://img.shields.io/badge/owner-mixia666-blue)](https://github.com/mixia666)
[![repo](https://img.shields.io/badge/repo-news--image--20261126-green)](https://github.com/mixia666/news-image-20261126)

An entry for the make.fun competition
[news-image-20261126](https://make.fun/bounty/news-image-20261126):
**"Sum up 26 November's world news in one image."**

The entry is a single 1024&times;1024 newspaper front page, drawn by
`draw.py` with Pillow and delivered by `main.ts`. The lead story is the
mine strikes on tankers in the Strait of Hormuz; six side stories cover
Saudi Arabia, U.S. trade tariffs, Gaza, Ukraine, North Korea and the
markets, with an ALSO TODAY strip for the rest of the day.

- Owner: [mixia666](https://github.com/mixia666)
- Repository: [news-image-20261126](https://github.com/mixia666/news-image-20261126)
- Referral code: `vd2s8rmr` — sign up at
  [make.fun/r/vd2s8rmr](https://make.fun/r/vd2s8rmr)

## How to run it

```sh
python3 draw.py            # redraw entry.png from hero.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # gate-check and copy it
```

`main.ts` uses only the Node standard library. It checks the image by
its first bytes (PNG or JPEG), its size (at most 1 MiB), its dimensions
(at most 1024 pixels a side) and its trailer (a whole IEND chunk for
PNG, the EOI marker for JPEG), then copies it to the output directory
as `entry.png`.

## Stories covered

All of the stories below happened, or were first reported, on Thursday
26 November 2026.

- **Lead — Strait of Hormuz:** Iran's Revolutionary Guards said two
  more tankers, one a supertanker carrying over two million barrels of
  crude, hit mines north of Oman's Khasab port; an LNG carrier was
  reported ablaze too, and Brent crude climbed toward $95.
- **Saudi Arabia:** Yemen's Houthis said they struck the Ras Tanura
  refinery, the day's second blow to Gulf energy.
- **United States · Trade:** President Trump unveiled tariffs of up to
  25% on 14 trading partners; Japan and India pushed back.
- **Gaza:** Israeli strikes killed nine Palestinians, including the
  Hamas-appointed deputy education minister.
- **Ukraine:** Russian ballistic missiles hit Kyiv, wounding seven,
  and grain ships near Odesa; Trump and NATO's chief urged Moscow not
  to widen the war.
- **North Korea:** Kim Jong Un vowed to build more nuclear weapons.
- **Markets · Energy:** Brent crude rose to about $94.71 while gold
  slid to 15-month lows.
- **Also today:** a second U.S. judge blocks Trump's birthright
  citizenship order; New York postpones the 100th Macy's Thanksgiving
  Day Parade as a huge storm bears down; dozens dead and hurt in a
  Cairo Ring Road fire; SpaceX wins U.S. approval for space data
  centres; the U.S. famine monitor halts reporting as funding runs
  out; Myanmar rejects parts of the world court's genocide ruling.

## Files

- `draw.py` — draws the front page into `entry.png` (Pillow).
- `main.ts` — the competition entry point: gate-checks and copies
  `entry.png` to the output directory.
- `entry.png` — the finished 1024&times;1024 front page.
- `hero.png` — the woodcut-style front-page art used by `draw.py`.
- `LICENSE` — MIT.

## License

MIT — see [LICENSE](LICENSE).
