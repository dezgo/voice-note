# Voice Note — Status

## Live
https://audio.appfoundry.cc/api/voice-note

## Stack
- Flask + Gunicorn (unix socket: `/run/voice-note/voice-note.sock`)
- Nginx + Let's Encrypt SSL
- Systemd service: `voice-note.service`
- Server: `do-personal` (209.38.91.37)
- Code: `/var/www/voice-note`

## Apple Shortcut
Single shortcut on Apple Watch:
1. **Dictate Text** — records and transcribes in one step
2. **Get Contents of URL** — POST to endpoint with `transcript` field

Note: audio attachment was dropped — Apple Watch Shortcuts cannot send files via URL action.

## Environment Variables
See `.env.example`. Required on server at `/var/www/voice-note/.env`.

## Deploy
```bash
ssh do-personal
cd /var/www/voice-note
git pull
sudo systemctl restart voice-note
```

## Logs
```bash
sudo tail -f /var/log/voice-note/access.log
sudo tail -f /var/log/voice-note/error.log
journalctl -u voice-note -f
```

## Planned
- AI dispatcher to classify intent (todo, reminder, idea, etc.)
- Connector to Markd (todo app) at markd.appfoundry.cc
