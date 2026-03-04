#!/bin/bash
# screenshot.sh - 网页截图工具

CHROME="/home/node/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome"
OUTPUT_DIR="$HOME/.openclaw/workspace"

show_help() {
    echo "Usage: screenshot.sh <URL> [output_filename]"
    echo ""
    echo "Examples:"
    echo "  screenshot.sh https://web.mit.edu"
    echo "  screenshot.sh https://google.com google.png"
    echo ""
    echo "Output saved to: $OUTPUT_DIR/"
}

if [ $# -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    show_help
    exit 0
fi

URL="$1"
FILENAME="${2:-screenshot_$(date +%Y%m%d_%H%M%S).png}"
OUTPUT="$OUTPUT_DIR/$FILENAME"

echo "📸 Taking screenshot of: $URL"
echo "💾 Saving to: $OUTPUT"

$CHROME --headless --no-sandbox --disable-gpu \
    --screenshot="$OUTPUT" \
    --window-size=1920,1080 \
    --hide-scrollbars \
    "$URL" 2>/dev/null

if [ -f "$OUTPUT" ]; then
    SIZE=$(du -h "$OUTPUT" | cut -f1)
    echo "✅ Screenshot saved: $OUTPUT ($SIZE)"
else
    echo "❌ Screenshot failed"
    exit 1
fi
