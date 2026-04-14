#!/data/data/com.termux/files/usr/bin/bash
# EduPulse — start.sh
# Termux local development session launcher.
# Usage: ./start.sh
# Make executable: chmod +x start.sh

set -e  # exit on first error

echo "──────────────────────────────────"
echo " EduPulse — Local Dev Session"
echo "──────────────────────────────────"

# ── 1. Wakelock ───────────────────────────────────────────
# Prevents Android 7 from killing Termux when you switch apps.
# Requires Termux:API companion app installed.
if command -v termux-wake-lock &>/dev/null; then
    termux-wake-lock
    echo "[+] Wakelock acquired"
else
    echo "[!] termux-wake-lock not found — install Termux:API to prevent background kills"
    echo "    Continuing without wakelock..."
fi

# ── 2. Environment ────────────────────────────────────────
if [ ! -f .env ]; then
    echo "[!] .env not found. Copy and fill .env.example first:"
    echo "    cp .env.example .env && nano .env"
    exit 1
fi
source .env
echo "[+] Environment loaded"

# ── 3. DB Init ────────────────────────────────────────────
# Safe to run every time — uses CREATE TABLE IF NOT EXISTS
python -c "
import sys; sys.path.insert(0, 'src')
from core.db import init_db
init_db()
print('[+] DB ready at data/edupulse.db')
"

# ── 4. Launch ─────────────────────────────────────────────
echo "[+] Starting bot in DEVELOPMENT (polling) mode"
echo "    Press Ctrl+C to stop"
echo "──────────────────────────────────"

python src/bot.py
