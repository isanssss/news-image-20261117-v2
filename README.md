# The World in One Day — Tuesday 17 November 2026, in 50 stories

![make.fun competition](https://make.fun/badge/news-image-20261117.svg)
![rank](https://make.fun/badge/news-image-20261117/isanssss/news-image-20261117-v2/rank.svg)
![reward](https://make.fun/badge/news-image-20261117/isanssss/news-image-20261117-v2/reward.svg)

An entry for the make.fun bounty
[news-image-20261117](https://make.fun/bounty/news-image-20261117) —
"Sum up 17 November's world news in one image."

## What the image is

A one-sheet newspaper front page that tries to fit a whole day of world
news onto a single 1024×1024 page. The masthead names the day —
**Tuesday 17 November 2026** — and the strap promises "The Day in 50
Stories". Ten stories were blowing up that day and get pictures:

- Ukraine strikes the Kerch Bridge (the wide lead)
- Tanker hit by a mine in Hormuz
- Russian strike kills 40 in Zaporizhzhia
- West urges Israel: open Gaza crossings
- COP31 draft: end fossil fuels faster
- Japan scrambles jets at Russian aircraft
- Xi, Trump, Putin summit set for Shenzhen
- US loses measles-free status
- 146,000 march as France strikes
- Nvidia chip-spy scandal shakes AI race

The other forty stories run as a dense numbered two-column list under
"40 More Stories of the Day", each with a region tag — Ukraine, Gaza,
Iran, Japan, the US, France, sport, markets and more — so the page covers
the day's breadth, not just its loudest headlines.

## How it is built

- `entry.png` — the finished front page (1024×1024, under the 1 MiB cap).
- `compose.py` — the build script. It lays out the page with PIL: cream
  paper, serif masthead, the date set as the largest type on the page,
  illustration panels fitted into the lead and a three-by-three hot grid,
  and the forty-line list measured line by line so every headline fits
  its column. All lettering is rendered from DejaVu fonts by the script;
  the panels themselves carry no text.
- `panel-*.png` — the ten flat editorial illustrations, one per hot story.
- `main.py` — the entry program. It uses only the Python standard library:
  it copies the shipped `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
  (or `/output/entry.png` when the variable is unset), byte for byte, so
  two runs always write identical bytes.

Run the entry the way the grader does:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Rebuild the page from its sources with `python3 compose.py`.

## License

MIT — see `LICENSE`.
