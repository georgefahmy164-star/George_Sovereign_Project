#!/bin/bash
git add .
git commit -m "System Update: $(date +'%Y-%m-%d %H:%M')"
git push origin main
echo "[+] Project Synced to GitHub Successfully."
