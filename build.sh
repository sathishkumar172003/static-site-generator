if python3 --version >/dev/null 2>&1; then
  MSYS_NO_PATHCONV=1 python3 src/main.py "/static-site-generator/"
else
  MSYS_NO_PATHCONV=1 py -3 src/main.py "/static-site-generator/"
fi
