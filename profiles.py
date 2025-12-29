import os
import json
import shutil
from pathlib import Path
from datetime import datetime

APP_NAME = "Moddy"

def get_app_data_dir() -> Path:
    if os.name == "nt":  # Windows
        return Path(os.environ["APPDATA"]) / APP_NAME
    else:  # Linux / macOS
        return Path.home() / ".local" / "share" / APP_NAME
    
def create_profile(
        name: str,
        minecraft_version: str,
        loader: str,
        loader_version: str,
):
    """
    Creates a new mod profile.
    Returns the path to the created profile.
    """

    base_dir = get_app_data_dir()
    profiles_dir = base_dir / "profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)

    # Sanitize folder name (important)
    safe_name = name.replace(" ", "_").lower()
    profile_dir = profiles_dir / safe_name

    if profile_dir.exists():
        raise FileExistsError(f"Profile '{name}' already exists")

    # Create folders
    mods_dir = profile_dir / "mods"
    config_dir = profile_dir / "config"
    mods_dir.mkdir(parents=True)
    config_dir.mkdir()

    # Profile metadata
    profile_data = {
        "name": name,
        "minecraftVersion": minecraft_version,
        "loader": loader,
        "loaderVersion": loader_version,
        "createdAt": datetime.utcnow().isoformat(),
        "mods": []
    }

    # Write profile.json
    profile_json_path = profile_dir / "profile.json"
    with open(profile_json_path, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=4)

    return profile_dir

def add_mod_to_profile(profile_dir: Path, mod_file: Path):
    """
    Copies a mod .jar file into the profile's mods folder.
    """

    if not mod_file.exists():
        raise FileNotFoundError("Mod file does not exist")

    if mod_file.suffix.lower() != ".jar":
        raise ValueError("Only .jar mod files are supported")

    mods_dir = profile_dir / "mods"
    mods_dir.mkdir(exist_ok=True)

    destination = mods_dir / mod_file.name

    if destination.exists():
        raise FileExistsError(f"Mod '{mod_file.name}' already exists in profile")

    shutil.copy2(mod_file, destination)

    # Optional: update profile.json
    profile_json = profile_dir / "profile.json"
    if profile_json.exists():
        with open(profile_json, "r", encoding="utf-8") as f:
            profile_data = json.load(f)

        profile_data.setdefault("mods", []).append({
            "file": mod_file.name
        })

        with open(profile_json, "w", encoding="utf-8") as f:
            json.dump(profile_data, f, indent=4)

if __name__ == "__main__":
    add_mod_to_profile(get_app_data_dir() / "profiles" / "1.20.1 Forge", )
