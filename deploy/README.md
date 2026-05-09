# Deploy

Server config files for reference. Copy to the correct locations on the server.

| File | Server path |
|---|---|
| `voice-note.service` | `/etc/systemd/system/voice-note.service` |
| `nginx-voice-note.conf` | `/etc/nginx/sites-available/voice-note` |
| `sudoers-derek-ops` | `/etc/sudoers.d/derek-ops` |

## Setup steps

```bash
# 1. Clone and install
cd /var/www
git clone git@github.com:dezgo/voice-note.git
cd voice-note
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Create .env
cp .env.example .env
nano .env

# 3. Create log dir
sudo mkdir -p /var/log/voice-note
sudo chown derek:derek /var/log/voice-note

# 4. Install systemd service
sudo cp deploy/voice-note.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now voice-note

# 5. Install Nginx config
sudo cp deploy/nginx-voice-note.conf /etc/nginx/sites-available/voice-note
sudo ln -s /etc/nginx/sites-available/voice-note /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 6. SSL
sudo certbot --nginx -d audio.appfoundry.cc

# 7. Sudoers (optional, for remote management)
sudo cp deploy/sudoers-derek-ops /etc/sudoers.d/derek-ops
```
