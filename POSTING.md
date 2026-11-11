# How to post a journal entry

**Easiest:** paste your notes to Claude in the "business" project and say "post this". Claude formats it and publishes it.

**Yourself (phone or computer):** on GitHub, open this repo → `_posts` folder → **Add file → Create new file**.

1. Name the file `YYYY-MM-DD-short-title.md`, for example `2026-11-12-sat-out-the-chop.md`.
2. Paste this, fill it in, and click **Commit changes**:

```
---
title: Sat out the chop
market: ES Futures
status: traded
setup: H2
grade: A
takeaway: No trend, no trade.
---
### Plan
What I expected and which side I wanted to be on.

### What happened
The session in a few lines.

### Review
Did I follow my rules? What I'll do tomorrow.
```

- `status` is `traded` or `sat out`. It sets the calendar mark (filled dot or ring).
- `setup`, `grade` and `takeaway` are optional; delete any line you don't need.
- Grade the process (did I follow my rules?), not P&L. Keep account balances and P&L off the site.
- Chart screenshot: upload it to `assets/journal/`, then add `[![Chart]({{ site.baseurl }}/assets/journal/your-file.png)]({{ site.baseurl }}/assets/journal/your-file.png)` in the post (click opens it full size).
- Two entries on the same day are fine; both show when you click that day.
- The site updates about a minute after you commit.
