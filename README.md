# IPA-Discord-notifier

Fetches IPA (Information-technology Promotion Agency, Japan) RSS feeds and posts new items to a Discord channel via Webhook.

## What it does
- Polls official IPA RSS feeds
- Deduplicates by link/id (persisted in `sent.json`)
- Posts to Discord using an Incoming Webhook URL (stored in GitHub Actions Secrets)

## Setup (GitHub Actions)
1. Repository Settings → Secrets and variables → Actions
2. Add a repository secret:
   - Name: `DISCORD_WEBHOOK_URL`
   - Value: your Discord webhook URL

3. Actions tab → enable workflows if prompted.
4. Run manually:
   - Actions → "IPA RSS to Discord" → Run workflow

## Notes
- The workflow runs every 15 minutes (UTC). Edit `.github/workflows/ipa.yml` if you want a different schedule.
- `sent.json` is committed by the workflow to avoid re-posting the same items.
- Do not commit your webhook URL; keep it in GitHub Secrets.
