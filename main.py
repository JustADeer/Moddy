import base64
import json
import os
import zipfile

import fastapi
import httpx
import uvicorn
from fastapi import HTTPException
from fastapi.responses import FileResponse, HTMLResponse

MINECRAFT_PATH = r"C:\Users\shaqu\AppData\Roaming\.minecraft"


def get_mods_folder(path: str = "mods"):
    return os.path.join(MINECRAFT_PATH, path)


def read_manifest(jar_path) -> dict | None:
    manifest_data = None
    fabric_json_data = None
    icon_data = None
    error_message = ""

    try:
        with zipfile.ZipFile(jar_path, "r") as z:
            # 1. Try to read the manifest
            try:
                with z.open("META-INF/MANIFEST.MF") as f:
                    manifest_data = f.read().decode("utf-8")
            except KeyError:
                error_message += "META-INF/MANIFEST.MF not found. "

            # 2. Try to find and read the fabric.mod.json
            found_json = False
            for file_name in z.namelist():
                if not file_name.endswith("fabric.mod.json"):
                    continue
                found_json = True
                try:
                    raw = z.read(file_name).decode("utf-8-sig")
                    fabric_json_data = json.loads(raw)

                    # 3. IF fabric.mod.json was found, try to get its icon
                    if not fabric_json_data:
                        return None
                    if "icon" in fabric_json_data:
                        return None

                    icon_path = fabric_json_data.get("icon")
                    try:
                        # Read the icon's binary data
                        with z.open(icon_path) as icon_file:
                            icon_binary = icon_file.read()
                            # Encode as Base64 string to send via JSON
                            icon_data = base64.b64encode(icon_binary).decode("utf-8")

                    except KeyError:
                        error_message += f"Icon file '{icon_path}' not found in .jar. "
                    except Exception as e:
                        error_message += f"Error reading icon: {e}. "

                except json.JSONDecodeError as e:
                    error_message += f"Failed to parse {file_name}: {e}. "
                except UnicodeDecodeError as e:
                    error_message += f"Failed to decode {file_name}: {e}. "

                break

            if not found_json and "MANIFEST.MF not found" not in error_message:
                pass

    except zipfile.BadZipFile:
        error_message += "File is not a valid .jar (zip) file. "
    except Exception as e:
        error_message += f"An unexpected error occurred: {e} "

    return {
        "manifest": manifest_data,
        "fabric_json": fabric_json_data,
        "error": error_message.strip(),
        "icon_data": icon_data,
    }


def get_mods() -> list:
    mods = []
    for file_name in os.listdir(get_mods_folder()):
        file_path = os.path.join(get_mods_folder(), file_name)
        if os.path.isfile(file_path):
            if os.path.splitext(file_name)[-1].lower() == ".jar":
                mods.append(file_path)
    return mods


app = fastapi.FastAPI()


@app.get("/api/mods")
async def get_mods_api():
    """API endpoint to get data for all mods."""
    print("Got mods")
    mods_list = []
    for file_path in get_mods():
        file_name = os.path.basename(file_path)
        data = read_manifest(file_path)
        mods_list.append(
            {
                "file_name": file_name,
                "path": file_path,
                "manifest": data.get("manifest"),
                "fabric_json": data.get("fabric_json"),
                "error": data.get("error"),
                "icon_data": data.get("icon_data"),
            }
        )
    return mods_list


@app.get("/", response_class=HTMLResponse)
async def get_root():
    """Serves the main HTML page."""
    return FileResponse("index.html")


@app.post("/api/check_updates")
async def check_for_updates(body):
    """Checks Modrinth for updates based on file hashes."""
    if not body.hashes:
        return {}

    modrinth_payload = {
        "hashes": body.hashes,
        "algorithm": "sha1",
        "loaders": [body.loader.lower()],
        "game_versions": [body.game_version],
    }

    headers = {
        "User-Agent": "ModdyModManager/1.0 (shaquille.at.work@gmail.com)"
    }  # Polite API usage

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{MODRINTH_API_URL}/version_files/update",
                json=modrinth_payload,
                headers=headers,
                timeout=15.0,
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Modrinth API error: {response.text}",
            )

        modrinth_data = response.json()

        # Simplify the response for the frontend
        updates = {}
        for local_hash, version_data in modrinth_data.items():
            project_slug = version_data.get("project_slug", "")
            updates[local_hash] = {
                "latest_version": version_data.get("version_number", "Unknown"),
                "project_slug": project_slug,
                "url": f"https://modrinth.com/project/{project_slug}",
            }
        return updates

    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail="Modrinth API timed out.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking updates: {e}")


if __name__ == "__main__":
    print("--- Minecraft Mod Inspector UI ---")
    print(f"Reading mods from: {get_mods_folder()}")
    print("Starting FastAPI server...")
    print("Access the UI at: http://127.0.0.1:8000")
    print("-----------------------------------")
    uvicorn.run(app, host="127.0.0.1", port=8000)
