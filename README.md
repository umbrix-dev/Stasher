# ThemeSwitcher

A unique config manager for Hyprland that tracks your dotfiles and lets you swap between themes instantly.

## Installation

```bash
git clone https://github.com/yourusername/themeswitcher.git
cd themeswitcher
python3 install.py
```

Restart your terminal or source your shell config:

```bash
source ~/.bashrc  # or ~/.zshrc
```

## Usage

### Managing Paths

Tell ThemeSwitcher which config files to track:

```bash
themeswitcher path -a ~/.config/hypr/hyprland.conf
themeswitcher path -a ~/.config/waybar/config
themeswitcher path -l  # list all tracked paths
```

### Creating Themes

Create a snapshot of your current configs:

```bash
themeswitcher theme -c nord
themeswitcher theme -c catppuccin
themeswitcher theme -l  # list all themes
```

### Switching Themes

Apply any saved theme:

```bash
themeswitcher theme -a nord
themeswitcher theme -r  # reload configs (waybar, hyprland, etc)
```

## Commands

<details>
<summary>View all commands</summary>

### Path Management
```
-a, --add path       Add a config file to track
-r, --remove path    Remove a tracked file
-l, --list           Show all tracked paths
--wipe               Clear all paths
```

### Theme Management
```
-c, --create name    Save current configs as a theme
-d, --delete name    Delete a theme
-a, --apply name     Switch to a theme
-l, --list           Show all themes
-r, --reload         Reload Hyprland/Waybar/etc
--wipe               Delete all themes
```

</details>

## How it works

ThemeSwitcher tracks your dotfiles and creates snapshots. When you apply a theme, it swaps out your config files and optionally reloads your environment. Simple as that.

## Requirements

- Python 3.14.2+
- Hyprland (optional, for reload functionality)

## License

MIT