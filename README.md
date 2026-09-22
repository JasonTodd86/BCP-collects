# BCP-collects

A helper for posting the Sunday collect from the 2019 ACNA Book of Common
Prayer to a personal Facebook profile.

Facebook's API no longer allows automated posting to a personal profile
(only to Pages/Groups), so this doesn't post anything itself. Instead:

1. `src/bcp_calendar.py` works out which Sunday of the church year a given
   date is (Advent 1, Epiphany 3, Proper 14, Christ the King, ...) from the
   date of Easter.
2. `data/collects.json` holds the collect text for each of those Sundays,
   keyed to match. **Text starts out `null` for every entry** — it must be
   filled in from an authoritative copy of the 2019 BCP before it's useful.
3. `scripts/get_collect.py` looks up the upcoming Sunday (or a date you
   pass it) and prints ready-to-paste post text, or fails loudly if that
   Sunday's text hasn't been entered yet.
4. `.github/workflows/weekly-collect-reminder.yml` runs that script every
   Saturday evening and opens a GitHub issue with the result, so a
   notification lands in your inbox in time to use Facebook's own
   "Schedule post" feature for 8:00 AM Sunday.

## Filling in the collects

Edit `data/collects.json` and set `text` (and ideally `source`, e.g. a page
number) for each Sunday. `title` can be adjusted too if the BCP's exact
wording differs from the placeholder.

## Trying it locally

```
python3 scripts/get_collect.py                # next Sunday
python3 scripts/get_collect.py 2027-03-28      # a specific Sunday
```
