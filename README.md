# BCP-collects

A Python helper for posting the Sunday collect from the 2019 ACNA Book of Common
Prayer to a personal Facebook profile.

Facebook's API no longer allows automated posting to a personal profile
(only to Pages/Groups), so this doesn't post anything itself. Instead:

1. `src/bcp_calendar.py` works out which Sunday of the church year a given
   date is (Advent 1, Epiphany 3, Proper 14, Christ the King, ...) from the
   date of Easter.
2. `data/collects.json` holds the collect for each of those Sundays, keyed
   to match. Text is copied verbatim from the 2019 BCP's `Collects of the
   Christian Year` section (pp. 598-622), with a `source` page number on
   every entry. Where the BCP gives two alternative collects for a day, the
   first is used.
3. `scripts/get_collect.py` looks up the upcoming Sunday (or a date you
   pass it) and prints ready-to-paste post text.
4. `.github/workflows/weekly-collect-reminder.yml` runs that script and
   emails you the result — ready to copy and paste into a Facebook post.
   It's scheduled for 1:00 AM US/Central, not the 6:00 AM target delivery
   time, because GitHub has twice delayed this exact schedule by about
   4.7-4.75 hours (observed, not a GitHub guarantee -- their docs only
   say high load *can* delay a scheduled run, with no bound on how much).
   Firing ~5 hours early is a calibrated guess to land close to 6am; if
   GitHub's delay pattern drifts, these cron times are the first thing to
   re-tune. Two cron triggers cover both sides of the DST switch. Rather
   than gating on an exact hour (which can't survive a multi-hour delay),
   the workflow caches a small marker keyed to the ISO week: whichever
   trigger fires first sends the email, and any later run that week (the
   other DST trigger, or a delayed retry) sees the marker and skips.

## About the Book of Common Prayer PDF

The 2019 BCP is a copyrighted book, so the PDF is not included in this
repository. `data/collects.json` already holds the collects with page
references. To check them or re-extract, get your own copy of the book
(5th printing, 2022) and compare against `Collects of the Christian
Year`, pp. 598-622.

## Setting up the email

Uses [dawidd6/action-send-mail](https://github.com/dawidd6/action-send-mail)
over SMTP. Add these as repository secrets (Settings -> Secrets and
variables -> Actions -> New repository secret) — never put real
credentials in the workflow file itself:

| Secret | Example (Gmail) |
| --- | --- |
| `MAIL_SERVER` | `smtp.gmail.com` |
| `MAIL_PORT` | `465` |
| `MAIL_USERNAME` | your Gmail address |
| `MAIL_PASSWORD` | a 16-character [Gmail app password](https://myaccount.google.com/apppasswords) — not your normal password |

The reminder is hardcoded to send to `j.chris.todd@gmail.com` (see the
`to:` line in the workflow) — change it there directly if that ever needs
to be a different address.

Gmail app passwords require 2-Step Verification to be turned on for the
account first. Any SMTP provider works the same way — just swap the
server/port.

Test it any time with the "Run workflow" button on the Actions tab —
manual runs always send regardless of the once-per-week cache, so you can
re-test as often as you like without waiting for next Sunday.

## Stack

Python 3, GitHub Actions (scheduled workflow with a weekly cache marker), SMTP email via `dawidd6/action-send-mail`

## Trying it locally

```
python3 scripts/get_collect.py                # next Sunday
python3 scripts/get_collect.py 2027-03-28      # a specific Sunday
```
