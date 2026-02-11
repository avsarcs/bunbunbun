#!/bin/bash
# Grammar Drill — Linux desktop shortcut installer

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/grammar-drill.desktop"

echo "Grammar Drill installer"
echo "========================"

# Check Python 3
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found."
    echo "Install it with your package manager, e.g.:"
    echo "  sudo apt install python3 python3-tk"
    exit 1
fi

# Check tkinter
if ! python3 -c "import tkinter" &>/dev/null; then
    echo "ERROR: tkinter not found."
    echo "Install it for your distro:"
    echo "  Debian/Ubuntu:  sudo apt install python3-tk"
    echo "  Fedora:         sudo dnf install python3-tkinter"
    echo "  Arch:           sudo pacman -S tk"
    exit 1
fi

# Create desktop entry
mkdir -p "$DESKTOP_DIR"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Name=Grammar Drill
Comment=Spaced-repetition grammar practice
Exec=python3 $SCRIPT_DIR/main.py
Path=$SCRIPT_DIR
Icon=accessories-text-editor
Type=Application
Terminal=false
Categories=Education;
EOF

chmod +x "$DESKTOP_FILE"

echo ""
echo "Done! Grammar Drill has been added to your application menu."
echo "You can also launch it directly with:"
echo "  python3 $SCRIPT_DIR/main.py"