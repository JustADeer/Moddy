**ModHelper**

- **Purpose:**: A minimal helper for managing mod profiles and launching a mod-enabled application.

**Overview**
- **Repository:**: ModHelper — simple utilities to load and manage mod profiles and static assets.
- **Contents:**: `main.py`, `profiles.py`, `static/index.html`, `LICENSE`.

**Features**
- **Profiles**: Manage named mod profiles via `profiles.py`.
- **Launcher**: Entry point and orchestration via `main.py`.
- **Static UI**: A simple static HTML in `static/index.html` for any lightweight UI needs.

**Requirements**
- **Python:**: 3.8+ recommended.

**Quick Start**
- **Install dependencies (if any):**: This project has no pinned dependencies. Create and activate a Python venv if desired:

	`python -m venv .venv`

	`.
	\.venv\Scripts\activate`  (Windows PowerShell)

- **Run the main script:**

	`python main.py`

- **Run the profiles utility:**

	`python profiles.py`

**Usage**
- **Profiles:**: `profiles.py` holds logic to create, list, and switch mod profiles. Inspect the file for available commands and examples.
- **Static files:**: Serve or open `static/index.html` in a browser for any simple UI or preview.

**Development**
- **Run locally:**: Use the commands in Quick Start. Edit `main.py` and `profiles.py` to extend functionality.
- **Testing:**: No automated tests included. Add tests under a `tests/` folder and run them with your preferred test runner.

**Contributing**
- **Issues & PRs:**: Open issues or pull requests with improvements or bug fixes.
- **Style:**: Keep changes small and focused; include short descriptions of behavior changes.

**License**
- See `LICENSE` for license details.

**Contact / Next Steps**
- If you want, I can: add a `requirements.txt`, add examples for `profiles.py`, or create a minimal UI around `static/index.html`.
