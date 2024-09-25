import subprocess
import os

def run_command(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
    return result.stdout.strip()

def install_fonts():
    """Install Noto emoji fonts on Arch Linux using pacman or yay."""
    print("Updating package database and installing emoji fonts...")
    
    # Check if pacman is available
    if run_command("command -v pacman"):
        update_command = "sudo pacman -Syu --noconfirm"
        install_command = "sudo pacman -S noto-fonts noto-fonts-emoji noto-fonts-cjk noto-fonts-legacy --noconfirm"
    elif run_command("command -v yay"):
        update_command = "yay -Syu --noconfirm"
        install_command = "yay -S noto-fonts noto-fonts-emoji noto-fonts-cjk noto-fonts-legacy --noconfirm"
    else:
        print("Error: Neither pacman nor yay is installed. Please install one of them first.")
        return

    run_command(update_command)
    output = run_command(install_command)
    print(output)

def configure_font_settings():
    """Create font configuration for Noto Color Emoji."""
    config_dir = os.path.expanduser("~/.config/fontconfig")
    config_file = os.path.join(config_dir, "fonts.conf")
    
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    config_content = '''<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <match target="pattern">
    <edit name="family" mode="prepend">
      <string>Noto Color Emoji</string>
    </edit>
  </match>
</fontconfig>'''
    
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print(f"Font configuration file created at: {config_file}")

def update_font_cache():
    """Update the font cache."""
    print("Updating font cache...")
    output = run_command("fc-cache -fv")
    print(output)

def main():
    install_fonts()
    configure_font_settings()
    update_font_cache()
    print("\nAll emoji fonts installed! You can test by typing an emoji in your terminal or text editor. 😊")

if __name__ == "__main__":
    main()

