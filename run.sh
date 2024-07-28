/usr/bin/Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xdummy.log -config /etc/X11/xorg.conf :1 > /dev/null 2>&1 &
export DISPLAY=:1
python3.10 test_run.py
tail -f /dev/null
