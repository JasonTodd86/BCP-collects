"""Liturgical calendar math for the 2019 ACNA Book of Common Prayer.

Given any Sunday date, works out which Sunday of the church year it is
(Advent 1, Epiphany 3, Proper 14, etc.) so the right collect can be looked
up. Movable feasts are derived from the date of Easter; the "Season after
Pentecost" uses the Proper-number-to-week table printed in the BCP itself
("Collects of the Christian Year", pp. 613-622), which assigns each Proper
to the Sunday falling in a specific 7-day window (e.g. Proper 1 = the
Sunday from May 8-14). That window is, by construction, always the Sunday
nearest to the window's middle day, which is how proper_anchor_date below
computes it without hardcoding 29 date ranges.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

_ORDINALS = {
    1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth",
    6: "Sixth", 7: "Seventh", 8: "Eighth", 9: "Ninth", 10: "Tenth",
}


def ordinal(n: int) -> str:
    return _ORDINALS.get(n, f"{n}th")


def nearest_sunday(d: date) -> date:
    """The Sunday nearest to d (ties broken toward the following Sunday)."""
    days_after = (6 - d.weekday()) % 7  # Python: Monday=0 ... Sunday=6
    next_sunday = d + timedelta(days=days_after)
    prev_sunday = next_sunday - timedelta(days=7)
    if (next_sunday - d) <= (d - prev_sunday):
        return next_sunday
    return prev_sunday


def easter_date(year: int) -> date:
    """Anonymous Gregorian algorithm (Meeus/Jones/Butcher) for Easter Sunday."""
    a = year % 19
    b = year // 100
    c = year % 100
    d_ = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d_ - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def advent_sunday(year: int) -> date:
    """The Sunday nearest November 30 of `year` (Nov 27 - Dec 3)."""
    return nearest_sunday(date(year, 11, 30))


def church_year_start(d: date) -> date:
    """The Advent Sunday that opens the church year containing d."""
    adv_this = advent_sunday(d.year)
    if d >= adv_this:
        return adv_this
    return advent_sunday(d.year - 1)


# Proper N is kept on the Sunday nearest this anchor date, one week later
# for each successive Proper (BCP 2019, pp. 613-622: "Proper 1 - Week of
# the Sunday from May 8 to May 14", "Proper 2 - ... May 15 to May 21", etc.)
_PROPER_1_ANCHOR = (5, 11)  # May 11, the middle day of the May 8-14 window


def proper_anchor_date(n: int, year: int) -> date:
    base = date(year, *_PROPER_1_ANCHOR) + timedelta(days=7 * (n - 1))
    return nearest_sunday(base)


@dataclass
class SundayInfo:
    key: str
    title: str


def describe_sunday(d: date) -> SundayInfo:
    """Classify a Sunday date into a named Sunday of the 2019 BCP calendar."""
    if d.weekday() != 6:
        raise ValueError(f"{d} is not a Sunday")

    cy_start = church_year_start(d)
    cy_year = cy_start.year          # calendar year Advent falls in
    easter_year = cy_year + 1        # Easter following that Advent
    easter = easter_date(easter_year)
    ash_wednesday = easter - timedelta(days=46)
    palm_sunday = easter - timedelta(days=7)
    pentecost = easter + timedelta(days=49)
    trinity = easter + timedelta(days=56)
    next_advent = advent_sunday(easter_year)
    last_epiphany_sunday = ash_wednesday - timedelta(days=3)
    second_to_last_epiphany_sunday = last_epiphany_sunday - timedelta(days=7)
    epiphany_day = date(easter_year, 1, 6)
    christmas_day = date(cy_year, 12, 25)

    # Advent (weeks 0-3 after cy_start)
    if cy_start <= d < cy_start + timedelta(days=28):
        n = (d - cy_start).days // 7 + 1
        return SundayInfo(f"advent-{n}", f"The {ordinal(n)} Sunday in Advent")

    # Christmas season (Sundays strictly between Christmas Day and Epiphany)
    if christmas_day < d < epiphany_day:
        first = christmas_day + timedelta(days=(6 - christmas_day.weekday()) % 7)
        if first == christmas_day:
            first += timedelta(days=7)
        n = (d - first).days // 7 + 1
        return SundayInfo(f"christmas-{n}", f"The {ordinal(n)} Sunday of Christmas")

    if d == epiphany_day:
        return SundayInfo("epiphany-day", "The Epiphany")

    # First Sunday of Epiphany: the Sunday following Jan 6 (the Sunday
    # *after* Jan 6 even when Jan 6 itself is a Sunday -- the BCP treats
    # that day as "The Epiphany", not as the First Sunday of Epiphany).
    epiphany_first = epiphany_day + timedelta(days=(6 - epiphany_day.weekday()) % 7)
    if epiphany_first == epiphany_day:
        epiphany_first += timedelta(days=7)

    if d == last_epiphany_sunday:
        return SundayInfo("epiphany-last", "The Last Sunday of Epiphany")

    if d == second_to_last_epiphany_sunday and second_to_last_epiphany_sunday > epiphany_first:
        return SundayInfo("epiphany-second-to-last", "The Second to Last Sunday of Epiphany")

    if epiphany_first <= d < second_to_last_epiphany_sunday:
        n = (d - epiphany_first).days // 7 + 1
        return SundayInfo(f"epiphany-{n}", f"The {ordinal(n)} Sunday of Epiphany")

    # Lent
    lent_1 = ash_wednesday + timedelta(days=4)
    if lent_1 <= d < palm_sunday:
        n = (d - lent_1).days // 7 + 1
        return SundayInfo(f"lent-{n}", f"The {ordinal(n)} Sunday in Lent")

    if d == palm_sunday:
        return SundayInfo("palm-sunday", "Palm Sunday")

    if d == easter:
        return SundayInfo("easter-day", "Easter Day")

    # Easter 2-6; the Sunday between Ascension Day and Pentecost has its
    # own title rather than being "Easter 7".
    if easter < d < pentecost:
        n = (d - easter).days // 7 + 1
        if n == 7:
            return SundayInfo("sunday-after-ascension", "The Sunday after Ascension Day")
        return SundayInfo(f"easter-{n}", f"The {ordinal(n)} Sunday of Easter")

    if d == pentecost:
        return SundayInfo("pentecost", "The Day of Pentecost")

    if d == trinity:
        return SundayInfo("trinity", "Trinity Sunday")

    # Season after Pentecost: Propers (Proper 29 is always Christ the King,
    # the Sunday immediately before Advent Sunday).
    if trinity < d < next_advent:
        for n in range(1, 30):
            if proper_anchor_date(n, easter_year) == d:
                title = f"Proper {n}"
                if n == 29:
                    title += ": Christ the King"
                return SundayInfo(f"proper-{n}", title)
        raise ValueError(f"Could not match {d} to a Proper")

    raise ValueError(f"Could not classify {d} in the church calendar")


if __name__ == "__main__":
    assert easter_date(2026) == date(2026, 4, 5), easter_date(2026)
    assert easter_date(2027) == date(2027, 3, 28), easter_date(2027)
    assert advent_sunday(2026) == date(2026, 11, 29), advent_sunday(2026)
    print("2026-11-29:", describe_sunday(date(2026, 11, 29)))
    print("2027-01-03:", describe_sunday(date(2027, 1, 3)))
    print("2027-03-28 (Easter 2027):", describe_sunday(date(2027, 3, 28)))
    print("2026-09-20 (this week):", describe_sunday(date(2026, 9, 20)))
    print("2026-09-27:", describe_sunday(date(2026, 9, 27)))
    print("2027-05-16 (Pentecost 2027):", describe_sunday(date(2027, 5, 16)))
    print("2027-05-23 (Trinity 2027):", describe_sunday(date(2027, 5, 23)))
    print("2027-05-09 (Sunday after Ascension 2027):", describe_sunday(date(2027, 5, 9)))
    print("2027-11-21 (last before Advent 2027):", describe_sunday(date(2027, 11, 21)))
    print("All sanity checks passed.")
