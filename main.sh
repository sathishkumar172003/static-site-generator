if python3 --version >/dev/null 2>&1; then
  python3 -m http.server 8888 --directory docs
else
  py -3 -m http.server 8888 --directory docs
fi