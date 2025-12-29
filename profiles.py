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

def save_profile_from_minecraft(profile_dir: Path, minecraft_dir: Path):
    print("Saving to profile:", profile_dir)
    mc_mods = minecraft_dir / "mods"
    mc_config = minecraft_dir / "config"

    profile_mods = profile_dir / "mods"
    profile_config = profile_dir / "config"

    if not mc_mods.exists():
        raise FileNotFoundError("Minecraft mods folder does not exist")

    # ---- Mods ----
    if profile_mods.exists():
        shutil.rmtree(profile_mods)

    shutil.copytree(mc_mods, profile_mods)

    # ---- Config ----
    if mc_config.exists():
        if profile_config.exists():
            shutil.rmtree(profile_config)

        shutil.copytree(mc_config, profile_config)

def apply_profile(profile_dir: Path, minecraft_dir: Path):
    """
    Applies a mod profile to a Minecraft directory by copying
    mods and config folders.
    """
    print("Applying profile:", profile_dir)
    profile_mods = profile_dir / "mods"
    profile_config = profile_dir / "config"

    mc_mods = minecraft_dir / "mods"
    mc_config = minecraft_dir / "config"

    if not profile_mods.exists():
        raise FileNotFoundError("Profile mods folder is missing")

    # ---- Mods ----
    if mc_mods.exists():
        shutil.rmtree(mc_mods)

    shutil.copytree(profile_mods, mc_mods)

    # ---- Config ----
    if profile_config.exists():
        if mc_config.exists():
            shutil.rmtree(mc_config)

        shutil.copytree(profile_config, mc_config)

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



# SAVING IS FOR COPYING FROM MINECRAFT FOLDER TO PROFILE AND DELETING THE ORIGINAL
# APPLYING IS FOR COPYING FROM PROFILE TO MINECRAFT FOLDER AND DELETING THE ORIGINAL