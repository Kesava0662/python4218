#!/usr/bin/env bash
set -e
 
APP_DIR=/app
export DISPLAY=:99
export PATH=$PATH:/usr/local/bin:/usr/bin
 
# ---------------------------
# Start Xvfb (virtual display)
# ---------------------------
echo ">>> Starting Xvfb..."
Xvfb :99 -screen 0 1920x1080x24 -ac +extension RANDR > $APP_DIR/xvfb.log 2>&1 &
sleep 2
echo "✅ Xvfb running on :99"
 
# ---------------------------
# Start x11vnc
# ---------------------------
echo ">>> Starting x11vnc..."
x11vnc -display :99 -forever -nopw -rfbport 5900 -shared -bg -noxdamage > $APP_DIR/x11vnc.log 2>&1
echo "✅ x11vnc running on port 5900"
 
# ---------------------------
# Start noVNC
# ---------------------------
if [ -x "$APP_DIR/novnc/utils/launch.sh" ]; then
    echo ">>> Starting noVNC via launch.sh..."
    $APP_DIR/novnc/utils/launch.sh --vnc localhost:5900 --listen 6080 > $APP_DIR/novnc.log 2>&1 &
else
    echo ">>> Starting noVNC via websockify..."
    websockify --web=/usr/share/novnc/ --wrap-mode=ignore 6080 localhost:5900 > $APP_DIR/novnc.log 2>&1 &
fi
sleep 2
echo "✅ noVNC running on http://localhost:6080/vnc.html"
 
# ---------------------------
# Start XFCE Desktop
# ---------------------------
echo ">>> Starting XFCE Desktop..."
dbus-launch startxfce4 > $APP_DIR/xfce.log 2>&1 &
sleep 8
echo "✅ XFCE started on :99"
 
# ---------------------------
# Start Google Chrome inside XFCE session
# ---------------------------
echo ">>> Launching Google Chrome inside noVNC desktop..."
DISPLAY=:99 google-chrome --no-sandbox --disable-gpu --start-maximized --new-window "about:blank" > $APP_DIR/chrome.log 2>&1 &
sleep 5
echo "✅ Chrome is now visible in noVNC desktop"
 
# ---------------------------
# Run Python Selenium Tests INSIDE xfce4-terminal
# ---------------------------
echo ">>> Running Python Selenium tests inside GUI terminal..."
if [ -f "$APP_DIR/main.py" ]; then
    DISPLAY=:99 xfce4-terminal --geometry=120x30 --title="Selenium Tests" \
        --hold -e "bash -c 'cd $APP_DIR && python -u main.py; exec bash'" &
elif [ -f "$APP_DIR/pytest.ini" ] || [ -d "$APP_DIR/tests" ]; then
    DISPLAY=:99 xfce4-terminal --geometry=120x30 --title="Pytest Execution" \
        --hold -e "bash -c 'cd $APP_DIR && pytest -v --capture=no; exec bash'" &
elif [ -d "$APP_DIR/features" ]; then
    DISPLAY=:99 xfce4-terminal --geometry=120x30 --title="Behave Execution" \
        --hold -e "bash -c 'cd $APP_DIR && behave; exec bash'" &
else
    echo "⚠️ No Python entrypoint found (main.py / pytest / behave)."
fi
 
# ---------------------------
# Keep container alive
# ---------------------------
echo ">>> Container setup complete."
echo "🌐 Access desktop via noVNC: http://localhost:6080/vnc.html"
tail -f /dev/null
