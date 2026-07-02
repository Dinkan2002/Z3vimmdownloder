# Vimm ROM Downloader for RG34xx SP

A Python-based ROM downloader tool that integrates with Vimm's Lair to fetch game ROMs for your RG34xx SP and other RG35xx family handhelds.

## Features

- 🎮 Support for 10+ classic gaming systems (NES, SNES, GB, GBC, GBA, Genesis, PSX, N64, etc.)
- 🔍 Search Vimm's Lair database directly from the tool
- 📥 Automatic ROM downloading and organization by system
- 📦 Built-in archive extraction (ZIP, 7Z, RAR)
- 🖥️ Interactive terminal UI + command-line interface
- 💾 File management (list, delete ROMs)
- ⚡ Supports custom ROM paths for different device configurations

## Supported Systems

- **NES** - Nintendo Entertainment System
- **SNES** - Super Nintendo Entertainment System
- **GB** - Game Boy
- **GBC** - Game Boy Color
- **GBA** - Game Boy Advance
- **Genesis** - Sega Genesis/Mega Drive
- **SMS** - Sega Master System
- **GG** - Game Gear
- **PSX** - PlayStation 1
- **N64** - Nintendo 64

## Installation

### Quick Install

```bash
# Download and run the installer
curl -fsSL https://raw.githubusercontent.com/Dinkan2002/Z3vimm/main/install-vimm-downloader.sh | bash
```

### Manual Installation

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/Dinkan2002/Z3vimm.git
   cd Z3vimm
   ```

2. **Install dependencies**
   ```bash
   pip3 install requests
   ```

3. **Optional: Install extraction tools**
   ```bash
   # For 7Z support
   sudo apt install p7zip-full
   
   # For RAR support
   sudo apt install unar
   ```

4. **Make executable**
   ```bash
   chmod +x vimm-downloader.py install-vimm-downloader.sh
   ```

## Usage

### Interactive Mode

```bash
./vimm-downloader.py
```

This launches the interactive menu where you can:
1. Search and download ROMs
2. List downloaded ROMs
3. Delete ROMs
4. Extract archives
5. View supported systems

### Command-Line Mode

**Search for a ROM:**
```bash
./vimm-downloader.py --search "Super Mario Bros" --system nes
```

**List downloaded ROMs:**
```bash
./vimm-downloader.py --list
```

**Extract an archive:**
```bash
./vimm-downloader.py --extract /path/to/rom.zip
```

**Use custom ROMs directory:**
```bash
./vimm-downloader.py --roms-path /mnt/sdcard/roms
```

## Examples

### Example 1: Download a Game Boy Advance ROM

```bash
./vimm-downloader.py
# Select option 1 (Search and download ROM)
# Enter system: gba
# Enter ROM name: Pokemon
# Select desired game from results
```

### Example 2: Batch Download (Script)

```bash
#!/bin/bash
GAMES=("Super Mario Bros" "The Legend of Zelda" "Donkey Kong")

for game in "${GAMES[@]}"; do
    python3 vimm-downloader.py --search "$game" --system nes
done
```

### Example 3: Organize Existing ROMs

```bash
# Point to your current ROMs directory
./vimm-downloader.py --roms-path /mnt/current/roms --list
```

## Configuration

Edit `config.json` to customize default settings:

```json
{
  "roms_path": "/roms",
  "preferred_systems": ["nes", "snes", "gba"],
  "auto_extract": true,
  "max_download_threads": 2,
  "timeout_seconds": 30
}
```

## File Organization

ROMs are automatically organized by system:

```
/roms/
├── nes/
│   ├── Super Mario Bros.zip
│   └── The Legend of Zelda.zip
├── snes/
│   ├── Super Mario World.zip
│   └── Donkey Kong Country.zip
├── gba/
│   └── Pokemon Emerald.zip
└── psx/
    └── Final Fantasy VII.zip
```

## Requirements

- **Python 3.6+**
- **requests** library (installed via pip)
- **Optional:** unzip (for ZIP files), 7z (for 7Z files), unar (for RAR files)

## Troubleshooting

### "No results found"
- Check your internet connection
- Try a more specific game title
- Some games might not be available on Vimm's Lair

### "Extraction failed"
- Ensure extraction tools are installed: `sudo apt install p7zip-full unzip`
- Check file integrity - the download may be corrupted

### "Permission denied"
```bash
chmod +x vimm-downloader.py
```

### "Module requests not found"
```bash
pip3 install requests
```

## Known Limitations

- Vimm's Lair has usage limits - large downloads may throttle
- Not all ROMs on Vimm's Lair are verified for compatibility
- Some systems may have limited ROM availability

## Compatibility

- ✅ RG34xx SP
- ✅ RG35xx Family (including RG35xxH)
- ✅ Any Linux system with Python 3
- ✅ Windows/Mac with WSL or similar

## Legal Notice

This tool is for downloading ROM files that you own or have permission to use. Ensure you comply with copyright laws in your jurisdiction. The author assumes no responsibility for misuse.

## Contributing

To add features or improve compatibility:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Credits

- Built for the RG35xx/RG34xx handheld community
- Part of the Z3apps project
- Inspired by the YouTube app framework

## Support

For issues or questions:
- Open an issue on GitHub
- Check the [Z3apps Reddit](https://www.reddit.com/r/SBCGaming/comments/1dfm4qz/youtube_app_for_rg35xx_family/)

## License

GPL-3.0 (See LICENSE file)

---

**Enjoy your retro gaming! 🎮**
