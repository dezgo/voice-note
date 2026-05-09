#!/usr/bin/env bash
set -euo pipefail

APP=voice-note
DIR=/var/www/voice-note
REPO=git@github.com:dezgo/voice-note.git
LOG_DIR=/var/log/voice-note

# ── Code ─────────────────────────────────────────────────────────────────────
if [ -d "$DIR/.git" ]; then
    echo "==> Pulling latest code"
    git -C "$DIR" pull
else
    echo "==> Cloning repo"
    git clone "$REPO" "$DIR"
fi

# ── Python venv ───────────────────────────────────────────────────────────────
if [ ! -d "$DIR/.venv" ]; then
    echo "==> Creating venv"
    python3 -m venv "$DIR/.venv"
fi

echo "==> Installing dependencies"
"$DIR/.venv/bin/pip" install -q -r "$DIR/requirements.txt"

# ── .env ──────────────────────────────────────────────────────────────────────
if [ ! -f "$DIR/.env" ]; then
    echo "==> Copying .env.example — fill in real values before starting the service"
    cp "$DIR/.env.example" "$DIR/.env"
fi

# ── Log dir ───────────────────────────────────────────────────────────────────
echo "==> Log directory"
sudo mkdir -p "$LOG_DIR"
sudo chown derek:www-data "$LOG_DIR"

# ── Systemd service ───────────────────────────────────────────────────────────
echo "==> Installing systemd service"
sudo cp "$DIR/deploy/voice-note.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable "$APP"
sudo systemctl restart "$APP"

# ── Nginx ─────────────────────────────────────────────────────────────────────
echo "==> Installing Nginx config"
sudo cp "$DIR/deploy/nginx-voice-note.conf" /etc/nginx/sites-available/"$APP"
if [ ! -L /etc/nginx/sites-enabled/"$APP" ]; then
    sudo ln -s /etc/nginx/sites-available/"$APP" /etc/nginx/sites-enabled/"$APP"
fi
sudo nginx -t
sudo systemctl reload nginx

# ── Sudoers ───────────────────────────────────────────────────────────────────
echo "==> Installing sudoers rules"
sudo cp "$DIR/deploy/sudoers-derek-ops" /etc/sudoers.d/derek-ops
sudo chmod 440 /etc/sudoers.d/derek-ops

echo ""
echo "Done. If this is a first install, run:"
echo "  sudo certbot --nginx -d audio.appfoundry.cc"
echo "and fill in $DIR/.env with real values, then: sudo systemctl restart $APP"
