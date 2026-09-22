# BCP-collects

A helper for posting the Sunday collect from the 2019 ACNA Book of Common
Prayer to a personal Facebook profile.

Facebook's API no longer allows automated posting to a personal profile
(only to Pages/Groups), so this doesn't post anything itself. Instead:

1. `src/bcp_calendar.py` works out which Sunday of the church year a given
   date is (Advent 1, Epiphany 3, Proper 14, Christ the King, ...) from the
   date of Easter.
2. `data/collects.json` holds the collect for each of those Sundays, keyed
   to match. Text is copied verbatim from
   `BCP-2019-MASTER-5th-PRINTING-05022022-3.pdf` (`Collects of the
   Christian Year`, pp. 598-622), with a `source` page number on every
   entry. Where the BCP gives two alternative collects for a day, the
   first is used.
3. `scripts/get_collect.py` looks up the upcoming Sunday (or a date you
   pass it) and prints ready-to-paste post text.
4. `.github/workflows/weekly-collect-reminder.yml` runs that script every
   Saturday evening and opens a GitHub issue with the result, so a
   notification lands in your inbox in time to use Facebook's own
   "Schedule post" feature for 8:00 AM Sunday. **The cron schedule is
   currently stubbed for US/Central — confirm or change it before relying
   on it.**

## Trying it locally

```
python3 scripts/get_collect.py                # next Sunday
python3 scripts/get_collect.py 2027-03-28      # a specific Sunday
```
