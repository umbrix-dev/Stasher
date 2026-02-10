"""
ThemeSwitcher - v0.0.1
https://www.github.com/umbrix-dev/themeSwitcher
-----------------------------------------------
Switch between themes using a simple cli tool
on Hyprland.
"""

from core.theme_switcher import ThemeSwitcher


def main() -> None:
    """The main entry point for ThemeSwitcher."""
    themeSwitcher = ThemeSwitcher()
    themeSwitcher.run()


if __name__ == "__main__":
    main()
