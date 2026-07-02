#!/bin/bash

# Installation script for Vimm ROM Downloader on RG34xx SP
# This script downloads and installs the vimm-downloader tool

set -e

INSTALL_DIR="${1:-.}/vimm-downloader"
GITHUB_URL="https://raw.githubusercontent.com/Dinkan2002/Z3vimmdownloader/main"

echo "========================================"
echo "Vimm ROM Downloader Installer"
echo "========================================"
echo "Installing to: $INSTALL_DIR"

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Download main script
echo "Downloading vimm-downloader..."
curl -s -o "$INSTALL_DIR/vimm-downloader.py" "$GITHUB_URL/vimm-downloader.py"

# Make executable
chmod +x "$INSTALL_DIR/vimm-downloader.py"

# Check dependencies
echo ""
echo "Checking dependencies..."

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required but not installed"
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is required but not installed"
    exit 1
fi
echo "✓ pip3 found"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install requests --quiet || pip install requests --quiet

# Check extraction tools
echo ""
echo "Checking archive tools..."

for tool in unzip 7z unar; do
    if command -v $tool &> /dev/null; then
        echo "✓ $tool found"
    else
        echo "⚠ $tool not found (optional)"
    fi
done

# Create a launcher script
echo ""
echo "Creating launcher script..."
cat > "$INSTALL_DIR/vimm-downloader" << 'EOF'
#!/bin/bash
# Vimm Downloader Launcher
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/vimm-downloader.py" "$@"
EOF

chmod +x "$INSTALL_DIR/vimm-downloader"

# Create config file
echo ""
echo "Creating configuration..."
cat > "$INSTALL_DIR/config.json" << 'EOF'
{
  "roms_path": "/roms",
  "preferred_systems": ["nes", "snes", "gba"],
  "auto_extract": true,
  "max_download_threads": 2,
  "timeout_seconds": 30
}
EOF

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "Usage:"
echo "  ./vimm-downloader              # Interactive mode"
echo "  ./vimm-downloader --search 'game_name'"
echo "  ./vimm-downloader --list"
echo "  ./vimm-downloader --extract archive.zip"
echo ""
echo "Location: $INSTALL_DIR"
echo ""
echo "To add to PATH, run:"
echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
echo ""
