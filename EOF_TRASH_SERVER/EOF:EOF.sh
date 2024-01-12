#!/bin/bash


cd ~/EOF_SeparateTrashCollection/EOF_TRASH_SERVER/
source .server_venv/bin/activate
export QT_QPA_PLATFORM=wayland
python3 main.py
