# bird-x Node Setup

## Fleet Install Status

| Node | Installed | Auth Token Set | Tested | Notes |
|------|-----------|---------------|--------|-------|
| Buster | ✅ v0.8.0 | ❌ needs token | ❌ | `/home/uvy/.npm-global/bin/bird` |
| Uvy | ❌ | ❌ | ❌ | |
| Atlas | ❌ | ❌ | ❌ | |
| Zevo | ❌ | ❌ | ❌ | |
| Jimmy | ❌ | ❌ | ❌ | |

*Update this table as nodes come online.*

## Getting the Auth Token

1. Log into x.com in your browser (use a read-only/secondary account if possible)
2. Open DevTools → Application → Cookies → `https://x.com`
3. Find the `auth_token` cookie → copy its value
4. On the target node:
   ```bash
   echo 'export TWITTER_AUTH_TOKEN=your_token_here' >> ~/.bashrc
   source ~/.bashrc
   ```
5. Test: `bird whoami`

## Install Command

```bash
npm install -g @steipete/bird
bird whoami  # confirm auth
```

## Troubleshooting

- **401/auth error**: Re-extract `auth_token` — cookies expire or rotate
- **Rate limit**: Space requests out; bird uses unofficial API with no documented limits
- **Command not found**: Check npm global bin is in PATH (`npm bin -g`)
