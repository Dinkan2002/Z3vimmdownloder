#!/usr/bin/env python3
"""
Vimm ROM Downloader for RG34xx SP
Downloads ROM files from Vimm's Lair for compatible game systems
Compatible with RG35xx family handheld consoles
"""

import os
import sys
import json
import requests
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
import urllib.parse

class VimmDownloader:
    """Download ROMs from Vimm's Lair API"""
    
    # Supported systems on RG34xx SP
    SUPPORTED_SYSTEMS = {
        'nes': 'NES',
        'snes': 'SNES',
        'gb': 'Game Boy',
        'gbc': 'Game Boy Color',
        'gba': 'Game Boy Advance',
        'gen': 'Sega Genesis',
        'sms': 'Sega Master System',
        'gg': 'Game Gear',
        'psx': 'PlayStation 1',
        'n64': 'Nintendo 64',
    }
    
    def __init__(self, roms_path: str = None):
        """Initialize the downloader with optional custom ROMs path"""
        if roms_path:
            self.roms_path = Path(roms_path)
        else:
            # Default paths for RG35xx
            possible_paths = [
                Path('/roms'),
                Path.home() / 'roms',
                Path('/mnt/mmc/roms'),
            ]
            self.roms_path = next((p for p in possible_paths if p.exists()), Path.home() / 'roms')
        
        self.roms_path.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux; rv:91.0) Gecko/20100101 Firefox/91.0'
        })
    
    def search_rom(self, query: str, system: str = None) -> List[Dict]:
        """
        Search for ROMs on Vimm's Lair
        
        Args:
            query: ROM name to search for
            system: Optional system filter
            
        Returns:
            List of search results with download info
        """
        try:
            # Vimm's Lair API endpoint
            search_url = "https://www.vimm.net/api/search"
            params = {
                'q': query,
                'system': system if system else ''
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            results = response.json() if response.headers.get('content-type') == 'application/json' else []
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"Error searching Vimm: {e}")
            return []
    
    def download_rom(self, rom_url: str, filename: str, system: str, 
                    progress_callback=None) -> bool:
        """
        Download a ROM file
        
        Args:
            rom_url: Direct download URL
            filename: Output filename
            system: System type for organization
            progress_callback: Optional callback for progress updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create system-specific directory
            system_path = self.roms_path / system
            system_path.mkdir(parents=True, exist_ok=True)
            
            output_path = system_path / filename
            
            # Check if file already exists
            if output_path.exists():
                print(f"File already exists: {output_path}")
                return True
            
            print(f"Downloading: {filename}")
            response = self.session.get(rom_url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total_size:
                            progress_callback(downloaded, total_size)
            
            print(f"Downloaded to: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error downloading ROM: {e}")
            return False
    
    def extract_archive(self, archive_path: Path, extract_to: Path = None) -> bool:
        """
        Extract ROM archive (zip, 7z, rar)
        
        Args:
            archive_path: Path to archive file
            extract_to: Destination directory (default: archive's parent)
            
        Returns:
            True if successful
        """
        try:
            if extract_to is None:
                extract_to = archive_path.parent
            
            extract_to.mkdir(parents=True, exist_ok=True)
            
            if archive_path.suffix.lower() == '.zip':
                subprocess.run(['unzip', '-q', str(archive_path), '-d', str(extract_to)], 
                              check=True)
            elif archive_path.suffix.lower() in ['.7z', '.7zip']:
                subprocess.run(['7z', 'x', str(archive_path), f'-o{extract_to}'], 
                              check=True)
            elif archive_path.suffix.lower() == '.rar':
                subprocess.run(['unar', '-o', str(extract_to), str(archive_path)], 
                              check=True)
            else:
                print(f"Unsupported archive format: {archive_path.suffix}")
                return False
            
            print(f"Extracted to: {extract_to}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error extracting archive: {e}")
            return False
        except FileNotFoundError:
            print("Required extraction tool not found (unzip, 7z, or unar)")
            return False
    
    def list_systems(self) -> Dict[str, str]:
        """List all supported systems"""
        return self.SUPPORTED_SYSTEMS
    
    def list_downloaded(self, system: str = None) -> Dict[str, List[str]]:
        """List downloaded ROMs, optionally filtered by system"""
        results = {}
        
        for sys_dir in self.roms_path.iterdir():
            if sys_dir.is_dir():
                sys_name = sys_dir.name
                
                if system and sys_name != system:
                    continue
                
                roms = [f.name for f in sys_dir.iterdir() 
                       if f.is_file() and f.suffix.lower() in 
                       ['.zip', '.7z', '.rar', '.rom', '.bin', '.gb', '.gbc', '.gba']]
                
                if roms:
                    results[sys_name] = sorted(roms)
        
        return results
    
    def delete_rom(self, system: str, filename: str) -> bool:
        """Delete a downloaded ROM file"""
        try:
            rom_path = self.roms_path / system / filename
            if rom_path.exists():
                rom_path.unlink()
                print(f"Deleted: {rom_path}")
                return True
            else:
                print(f"File not found: {rom_path}")
                return False
        except Exception as e:
            print(f"Error deleting ROM: {e}")
            return False


class VimmUI:
    """Terminal UI for Vimm Downloader"""
    
    def __init__(self, downloader: VimmDownloader):
        self.downloader = downloader
    
    def print_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("Vimm ROM Downloader for RG34xx SP")
        print("="*50)
        print("1. Search and download ROM")
        print("2. List downloaded ROMs")
        print("3. Delete ROM")
        print("4. Extract archive")
        print("5. Show supported systems")
        print("6. Exit")
        print("="*50)
    
    def run(self):
        """Run the interactive UI"""
        while True:
            self.print_menu()
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                self.search_and_download()
            elif choice == '2':
                self.list_roms()
            elif choice == '3':
                self.delete_rom()
            elif choice == '4':
                self.extract_rom()
            elif choice == '5':
                self.show_systems()
            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid option, please try again")
    
    def search_and_download(self):
        """Search for and download a ROM"""
        print("\nAvailable systems:", ", ".join(self.downloader.SUPPORTED_SYSTEMS.keys()))
        system = input("Enter system (or leave blank): ").strip().lower()
        query = input("Enter ROM name to search: ").strip()
        
        if not query:
            print("Search query cannot be empty")
            return
        
        print("\nSearching...")
        results = self.downloader.search_rom(query, system if system else None)
        
        if not results:
            print("No results found")
            return
        
        print(f"\nFound {len(results)} results:")
        for i, result in enumerate(results[:10], 1):
            print(f"{i}. {result.get('title', 'Unknown')} - {result.get('size', 'Unknown')}")
        
        try:
            choice = int(input("\nSelect ROM to download (number): ")) - 1
            if 0 <= choice < len(results):
                rom = results[choice]
                download_url = rom.get('download_url')
                if download_url:
                    filename = rom.get('filename', f"rom_{choice}.zip")
                    self.downloader.download_rom(download_url, filename, system or 'misc')
                else:
                    print("No download link available")
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")
    
    def list_roms(self):
        """Display downloaded ROMs"""
        roms = self.downloader.list_downloaded()
        
        if not roms:
            print("\nNo ROMs downloaded yet")
            return
        
        print("\n" + "="*50)
        print("Downloaded ROMs")
        print("="*50)
        
        for system, files in sorted(roms.items()):
            print(f"\n{system.upper()}:")
            for filename in files:
                size = (self.downloader.roms_path / system / filename).stat().st_size
                print(f"  - {filename} ({self.format_size(size)})")
    
    def delete_rom(self):
        """Delete a ROM file"""
        roms = self.downloader.list_downloaded()
        
        if not roms:
            print("\nNo ROMs to delete")
            return
        
        print("\nAvailable ROMs:")
        items = []
        idx = 1
        
        for system, files in sorted(roms.items()):
            for filename in files:
                print(f"{idx}. {system}/{filename}")
                items.append((system, filename))
                idx += 1
        
        try:
            choice = int(input("Select ROM to delete (number): ")) - 1
            if 0 <= choice < len(items):
                system, filename = items[choice]
                confirm = input(f"Delete {filename}? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.downloader.delete_rom(system, filename)
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")
    
    def extract_rom(self):
        """Extract an archive"""
        archive_path = input("Enter path to archive file: ").strip()
        
        if not os.path.exists(archive_path):
            print("File not found")
            return
        
        extract_to = input("Extract to (leave blank for same directory): ").strip()
        
        if self.downloader.extract_archive(
            Path(archive_path),
            Path(extract_to) if extract_to else None
        ):
            print("Extraction successful")
        else:
            print("Extraction failed")
    
    def show_systems(self):
        """Display supported systems"""
        print("\nSupported Systems:")
        print("="*40)
        for code, name in sorted(self.downloader.SUPPORTED_SYSTEMS.items()):
            print(f"  {code:6} - {name}")
    
    @staticmethod
    def format_size(bytes_size):
        """Format file size for display"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024:
                return f"{bytes_size:.1f}{unit}"
            bytes_size /= 1024
        return f"{bytes_size:.1f}TB"


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Vimm ROM Downloader for RG34xx SP'
    )
    parser.add_argument('--roms-path', help='Custom ROMs directory path')
    parser.add_argument('--search', help='Search for ROM (non-interactive)')
    parser.add_argument('--system', help='Filter by system')
    parser.add_argument('--list', action='store_true', help='List downloaded ROMs')
    parser.add_argument('--extract', help='Extract ROM archive')
    
    args = parser.parse_args()
    
    downloader = VimmDownloader(args.roms_path)
    
    # Non-interactive mode
    if args.search:
        results = downloader.search_rom(args.search, args.system)
        if results:
            print(json.dumps(results, indent=2))
        else:
            print("No results found")
        return
    
    if args.list:
        roms = downloader.list_downloaded(args.system)
        print(json.dumps(roms, indent=2))
        return
    
    if args.extract:
        downloader.extract_archive(Path(args.extract))
        return
    
    # Interactive mode
    ui = VimmUI(downloader)
    ui.run()


if __name__ == '__main__':
    main()
