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
   Sunday at 6:00 AM US/Central and emails you the result — ready to copy
   and paste into a Facebook post right away. (Two cron triggers cover
   both sides of the DST switch; a guard step checks the actual Central
   time and only lets one of them through each week.)

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

Test it any time with the "Run workflow" button on the Actions tab
(bypasses the 6am check).

## Trying it locally

```
python3 scripts/get_collect.py                # next Sunday
python3 scripts/get_collect.py 2027-03-28      # a specific Sunday
```
