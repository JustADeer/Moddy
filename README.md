# Moddy

> A minimal, no-frills helper for managing mod profiles and launching a mod-enabled application.

Moddy is designed to stay out of your way. It provides just enough structure to define, switch, and launch mod profiles—without pulling in heavy dependencies or complex frameworks.

---

## ✨ Features

- **Profile Management** – Create, list, and switch between named mod profiles
- **Simple Launcher** – Central entry point for loading profiles and starting the app
- **Static UI Ready** – Includes a lightweight HTML file for previews or basic UI needs
- **Zero Dependencies** – Uses only the Python standard library

---

## 📁 Project Structure

```
Moddy/
├─ main.py              # Launcher and orchestration
├─ profiles.py          # Mod profile logic
├─ static/
│  └─ index.html        # Minimal static UI
└─ LICENSE
```

---

## 🚀 Getting Started

### Requirements

- **Python 3.8+** (recommended)

### Optional: Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.\.venv\Scripts\activate       # Windows (PowerShell)
```

### Run Moddy

```bash
python main.py
```

### Run the Profiles Utility

```bash
python profiles.py
```

---

## 🧩 Usage

### Profiles

All profile-related logic lives in **`profiles.py`**. It includes utilities to:

- Create new mod profiles
- List existing profiles
- Switch the active profile

Open the file directly to see available commands and example usage.

### Static UI

The **`static/index.html`** file can be opened directly in a browser or served by your own tooling. It’s intentionally minimal and meant as a starting point—not a full UI framework.

---

## 🛠 Development

- Run scripts directly with Python (see Getting Started)
- Extend functionality by editing `main.py` and `profiles.py`
- No test suite is included by default

### Testing (Optional)

If you add tests, a common convention is:

```
Moddy/
└─ tests/
```

Run them using your preferred test runner (e.g. `unittest`, `pytest`).

---

## 🤝 Contributing

Contributions are welcome.

- Open an issue for bugs or feature ideas
- Submit focused pull requests with a clear description of changes
- Keep scope small and behavior easy to understand

---

## 📄 License

See the `LICENSE` file for details.

---

## 🔮 Next Steps

Potential improvements you might want to add:

- `requirements.txt` or `pyproject.toml`
- Example commands and workflows for `profiles.py`
- A small interactive UI built on top of `static/index.html`
- Basic logging or config file support

Moddy is intentionally minimal—extend it only as far as your project needs.
