# What it costs, with the command beside every number

## Measured, on Kate's own library

The one page of her library the console handed me, measured — not estimated:

    manage_file action=list scope=user   -> library_listing.json
    python3 measure_library.py

    files listed         1560
    total               318.2 MB
    largest             41.3 MB  motion-video/videos/2026-08-07_lamoom-in-colour/cuts/v1.mp4
    over 7MB             11
    over 1MB             36
    folders              322
    folders over 10 files 14
    more pages          True

`more pages True` means this is one page, so every count is a floor, not a total.

**What that measurement decides.** The `send_email` limits — 10 files, 7MB — are not
theoretical. 11 files in one page of her library can never be attached, and 14 of her 322
folders hold more than ten files. So an option that only attaches is an option that cannot
deliver a `motion-video` result at all. `{{link:path}}` is not the polite third form: it is the
only form that works for the biggest thing Lamoom makes.

## Per send

| What happens | How many | Unit price (AWS list, not measured here) |
|---|---|---|
| one read per reference, to prove the path and take the bytes | N, and N is 1 to 5 in a normal mail | S3 GET, $0.0004 per 1,000 requests |
| bytes out of S3 into the mail | the attached files only | same region, no egress charge |
| one mail | 1 | SES, $0.10 per 1,000 mails, plus $0.12 per GB of attachment |

**The per-send figure, computed.** A mail with three references, one of them a 200KB picture:

    3 GETs        3 x $0.0004/1000                    = $0.0000012
    1 send        $0.10/1000                          = $0.0001
    200KB out     0.0002 GB x $0.12/GB                = $0.000024
    ----------------------------------------------------------------
    total                                             = $0.000125

So about **one eightieth of a cent**, and the send is 80% of it.

**That ratio does not hold at the cap, and it is wrong to say it does.** The attachment term is
per byte, so at the 7MB cap one mail costs `0.007 GB x $0.12 = $0.00084` in bytes against
$0.0001 in send — **eight times the send**, and the send stops dominating anywhere above about
830KB of attachments. Every price here is an AWS list price, not something measured on Lamoom's
bill; only the file sizes come from a measurement, and even those are a stand-in (see the last
paragraph).

**At 100x, with the byte term carried and not dropped.** A hundred finished runs a day, three
references each, at 210KB apiece:

    100 sends            100 x $0.10/1000              = $0.0100 / day
    300 GETs             300 x $0.0004/1000            = $0.00012 / day
    100 x 3 x 210KB      = 61.2 MB/day = 0.064 GB      x $0.12/GB = $0.0077 / day
    ----------------------------------------------------------------------------
    total                                              ≈ $0.018 / day, ~$0.54 / month

**A correction, because this paragraph was wrong.** It first read "61 GB/mo -> 2.0 GB/day ->
$0.24/day", concluded that bytes were 96% of the bill, and said an all-attach design costs thirty
times a linking one. 100 x 3 x 210KB is 61 **megabytes** a day, not 61 gigabytes a month: the byte
term was inflated 33-fold and the conclusion drawn from it was backwards. Corrected, **sends are
the larger half** — $0.010 a day against $0.0077 — and at typical file sizes attaching everything
costs under twice what linking the big ones does, not thirty times.

**Where attaching does dominate is at the top of the range**, and that is worth having straight:
one mail at the 7MB cap costs $0.00084 in bytes against $0.0001 to send it — eight times — and the
crossover is around 830KB of attachments. So the argument for `{{link:path}}` is the 7MB ceiling
and the 41.3 MB video, not the monthly bill. At about fifty cents a month at a hundred times
today's volume, none of this decides anything; it is written out so nobody has to take "still
cents" on trust, and the arithmetic is shown so the next reader can catch it if it is wrong again.

**What 210KB is, exactly.** The mean file size over one page of Kate's library — 318.2 MB across
1560 files, printed by `python3 measure_library.py` as `average per file 210 KB`. It is not a
measurement of what a mail actually attaches, because no mail has ever attached one of these;
it is the best available stand-in, and every line above that uses it is an estimate wearing a
measured input.

**What the client-side option costs instead, priced.** N extra MCP round trips before every
send: one lambda invocation and one DynamoDB read each. At AWS list prices that is
$0.0000002 per lambda request plus $0.00000025 per eventually-consistent read — under a
millionth of a dollar per reference. **So on money the two options tie, and the comparison table
scores them both 5 on Cost.** Anyone using cost to choose between them is using a rounding error.

The real difference is not money and must not be smuggled in as money: N extra round trips are N
extra places a send can fail before a mail exists, which is an Operability difference and is
scored there.

**What N is.** Assumed to be 1 to 5 in a normal mail — an assumption, not a measurement, and
nothing above depends on its value: at a hundred references the arithmetic is still a fraction of
a cent. Stated so nobody later cites it as a number that was checked.

## The money story

The number that matters is not on this bill. Kate has under two hours a day and is the builder,
the seller and the support. Today a finished run mails her a body that says the result is in
her files, and reviewing it costs her a hunt through the studio. The mail is where she already
is. Every reference that turns into a picture she can see or a link she can tap removes one hunt,
every day, for every run she owns. That is the return, and no AWS line item competes with it.
