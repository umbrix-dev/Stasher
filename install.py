#!/usr/bin/env python3

"""
Installer script for themeswitcher
Installs requirements and sets up global PATH access on Linux
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


class ThemeSwitcherInstaller:
    def __init__(self) -> None:
        self.root_dir = Path(__file__).parent.resolve()
        self.bin_dir = self.root_dir / "bin"
        self.venv_dir = self.root_dir / ".venv"
        self.requirements_file = self.root_dir / "requirements.txt"
        self.shell_script = self.bin_dir / "themeswitcher"

    def check_platform(self) -> bool:
        """Check if running on Linux"""
        if platform.system() != "Linux":
            print("   Warning: Global PATH setup is only supported on Linux")
            print("   Requirements will still be installed")
            return False
        return True

    def create_venv(self) -> bool:
        """Create a virtual environment for the project"""
        print("Creating virtual environment...")

        if self.venv_dir.exists():
            print(f"Virtual environment already exists at {self.venv_dir}")
            return True

        try:
            subprocess.check_call([sys.executable, "-m", "venv", str(self.venv_dir)])
            print(f"Virtual environment created at {self.venv_dir}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating virtual environment: {e}")
            return False

    def install_requirements(self) -> bool:
        """Install Python requirements from requirements.txt"""
        print("Installing Python requirements...")

        if not self.requirements_file.exists():
            print(f"Error: requirements.txt not found at {self.requirements_file}")
            return False

        # Use pip from virtual environment
        venv_pip = self.venv_dir / "bin" / "pip"

        if not venv_pip.exists():
            print(f"Error: Virtual environment pip not found at {venv_pip}")
            return False

        try:
            subprocess.check_call(
                [str(venv_pip), "install", "-r", str(self.requirements_file)]
            )
            print("Requirements installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error installing requirements: {e}")
            return False

    def make_executable(self) -> bool:
        """Make the shell script executable"""
        if not self.shell_script.exists():
            print(f"Error: Shell script not found at {self.shell_script}")
            return False

        try:
            os.chmod(self.shell_script, 0o755)
            print(f"Made {self.shell_script.name} executable")
            return True
        except Exception as e:
            print(f"Error making script executable: {e}")
            return False

    def setup_global_path(self) -> bool:
        """Add bin directory to PATH via shell configuration"""
        shell = os.environ.get("SHELL", "/bin/bash")
        shell_name = Path(shell).name

        # Determine which rc file to use
        rc_files = {
            "bash": Path.home() / ".bashrc",
            "zsh": Path.home() / ".zshrc",
            "fish": Path.home() / ".config" / "fish" / "config.fish",
        }

        rc_file = rc_files.get(shell_name, Path.home() / ".bashrc")

        # PATH export line to add
        path_export = f'\n# themeswitcher PATH\nexport PATH="{self.bin_dir}:$PATH"\n'

        # Check if already in rc file
        if rc_file.exists():
            content = rc_file.read_text()
            if str(self.bin_dir) in content:
                print(f"PATH already configured in {rc_file}")
                return True

        # Add to rc file
        try:
            with open(rc_file, "a") as f:
                f.write(path_export)
            print(f"Added {self.bin_dir} to PATH in {rc_file}")
            print(f"\nPlease run: source {rc_file}")
            print(f"   Or restart your terminal for changes to take effect")
            return True
        except Exception as e:
            print(f"Error updating {rc_file}: {e}")
            return False

    def create_symlink_alternative(self) -> bool:
        """Alternative method: create symlink in /usr/local/bin"""
        local_bin = Path("/usr/local/bin")
        symlink_path = local_bin / "themeswitcher"

        if not local_bin.exists():
            print(f"{local_bin} does not exist")
            return False

        # Check if we have write permission
        if not os.access(local_bin, os.W_OK):
            print(f"\nAlternative method (requires sudo):")
            print(f"   sudo ln -sf {self.shell_script} {symlink_path}")
            return False

        try:
            if symlink_path.exists() or symlink_path.is_symlink():
                symlink_path.unlink()

            symlink_path.symlink_to(self.shell_script)
            print(f"Created symlink: {symlink_path} -> {self.shell_script}")
            return True
        except Exception as e:
            print(f"Error creating symlink: {e}")
            return False

    def run(self) -> int:
        """Run the installation process"""
        print("=" * 60)
        print("  ThemeSwitcher Installer")
        print(f"{'=' * 60}\n")

        is_linux = self.check_platform()

        if not self.create_venv():
            print("\n❌ Installation failed at virtual environment step\n")
            return 1

        if not self.install_requirements():
            print("\nInstallation failed at requirements step\n")
            return 1

        if is_linux:
            if not self.make_executable():
                print("\nInstallation failed at executable step")
                return 1

            print("\nSetting up global PATH access...")
            print(f"   Installing from: {self.bin_dir}\n")

            if self.setup_global_path():
                print("\nAlternative: You can also create a system-wide symlink:")
                print(
                    f"   sudo ln -sf {self.shell_script} /usr/local/bin/themeswitcher\n"
                )

        print("=" * 60)
        print("Installation complete!")
        print("=" * 60)

        if is_linux:
            print("\nNext steps:")
            print("   1. Restart your terminal or run: source ~/.bashrc (or ~/.zshrc)")
            print("   2. Run: themeswitcher")

        return 0


def main() -> None:
    """The main entry point for the ThemeSwitcher installer."""
    installer = ThemeSwitcherInstaller()
    sys.exit(installer.run())


if __name__ == "__main__":
    main()
