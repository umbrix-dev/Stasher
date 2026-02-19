# Stasher

Stasher - A simple snapshot manager for Linux.

## Installation

```bash
git clone https://github.com/umbrix-dev/stasher.git
cd stasher
python3 install.py
```

Restart your terminal or source your shell config:

```bash
source ~/.bashrc  # or ~/.zshrc
```

## Usage

### Managing Paths

Tell stasher which files or directories to track:

```bash
stasher path -a ~/.config/hypr/hyprland.conf
stasher path -a ~/.config/waybar/config
stasher path -l  # list all tracked paths
```

### Creating Stashes

Create a snapshot of your tracked files or directories:

```bash
stasher stash -c home
stasher stash -c work
stasher stash -l  # list all stashes
```

### Switching Stashes

Apply any saved stash:

```bash
stasher stash -a home
stasher stash -r  # reload known configs (waybar, hyprland, etc...)
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

### Stash Management
```
-c, --create name    Save tracked items as a stash
-d, --delete name    Delete a stash
-a, --apply name     Switch to a stash
-l, --list           Show all stashes
-r, --reload         Reload known configs (waybar, hyprland, etc...)
--wipe               Delete all stashes
```

</details>

## How it works

Stasher lets you track items and create snapshots of them. When you apply a stash, it swaps out your current files and directorys and optionally reloads your environment. Simple as that.

## Requirements

- Python 3.14.2+

## License

MIT