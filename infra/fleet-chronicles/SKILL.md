# Fleet Chronicles Skill

## Purpose
Archive Discord channel history (primarily #gene-pool and #gene-pool-prior) to local files and Google Drive using DiscordChatExporter (DCE). Pip is the designated Fleet Chronicler.

## Fleet Deployment

| Agent | Machine | Arch | Status | Primary scope |
|-------|---------|------|--------|---------------|
| **Pip** 🐣 | Intel MacBook 2017 | osx-x64 | ✅ Installed | Fleet Chronicler — #gene-pool + all Ranch channels |
| **Zevo** 🦓 | Mac Mini M4 Pro | osx-arm64 | ✅ Installed | Backup / nightly cron |
| **Uvy** 🦾 | Mac Mini (Milit) | osx-arm64 | ✅ Installed | UViiVe channels (pre-Zevo history) |
| **Buster** 🐕 | Framework Linux | linux-x64 | ✅ Installed | UViiVe protein design work archiving |

**Token:** Steve's user token stored at `~/.openclaw/workspace/.discord-user-token` (chmod 600) on all machines.
**Binary:** `~/.openclaw/workspace/tools/discordchatexporter/DiscordChatExporter.Cli`
**Version:** 2.47.1

## ⚠️ Token Requirements
DCE requires a **Discord user token** — bot tokens do not work.

### How Steve gets his user token (one-time setup):
1. Open Discord in Chrome/Firefox
2. Open DevTools (F12 / Cmd+Option+I)
3. Go to **Network** tab
4. Send any message or click around in Discord
5. Find any request to `discord.com/api`
6. In **Request Headers**, find `Authorization:` — that value is your token
7. Copy and paste to Steve's agent (Zevo or Pip), who will store it securely

**Store token:** `echo "TOKEN_HERE" > ~/.openclaw/workspace/.discord-user-token && chmod 600 ~/.openclaw/workspace/.discord-user-token`

## Basic Export Commands

```bash
DCE=~/.openclaw/workspace/tools/discordchatexporter/DiscordChatExporter.Cli
TOKEN=$(cat ~/.openclaw/workspace/.discord-user-token)
OUTPUT=~/.openclaw/workspace/projects/fleet-chronicles/

# Export a channel (JSON format, all history)
$DCE export --token "$TOKEN" --channel CHANNEL_ID --format Json --output $OUTPUT

# Export with date range (incremental)
$DCE export --token "$TOKEN" --channel CHANNEL_ID --format Json --output $OUTPUT --after 2026-01-01

# Export plain text
$DCE export --token "$TOKEN" --channel CHANNEL_ID --format PlainText --output $OUTPUT
```

## Key Channel IDs
| Channel | ID |
|---------|-----|
| #gene-pool | 1472639568024178878 |
| #gene-pool-prior | 1478519371692380191 |
| #zevo-mendel | 1481060173543112857 |

## Archive Index
- Location: `~/.openclaw/workspace/projects/fleet-chronicles/archive-index.json`
- Tracks `last_archived_id` per channel to enable incremental exports
- Update after every run

## Nightly Cron (Zevo)
- Cron ID: `123052da-4d8d-4935-875d-640812e97a4d`
- Schedule: 11 PM CST daily
- Archives #gene-pool + #gene-pool-prior → uploads to Drive Master Projects folder

## Pip's Chronicler Role
Pip handles:
1. **Historical backfill** — full export of #gene-pool + #gene-pool-prior once user token is available
2. **Ongoing nightly archive** — can mirror Zevo's cron or run independently
3. **Fleet-wide channel coverage** — can be extended to other channels as needed

## Output Format
Prefer **JSON** for ingestion/processing. Use **PlainText** for human-readable archives.

JSON exports contain: message ID, timestamp, author, content, attachments, reactions.

## Drive Upload
```bash
gog drive upload --account zevo.ekkerlab@gmail.com --client zevo \
  --parent 1JS-uJNQf9Ymq2JWDY2C7Z0XPJawXL5-E \
  <filepath>
```
