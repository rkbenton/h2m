# h2m (HTML to Markdown)

**h2m** is a lightweight macOS utility that captures HTML content directly from your system pasteboard, converts it into clean **GitHub-Flavored Markdown (GFM)**, and copies it back to your pasteboard.

It uses `PyObjC` to interact with native macOS pasteboard "flavors," ensuring that even complex structures like tables and nested lists are preserved during conversion.

## Features

- **Flavor Audit:** Logs every data format currently in your pasteboard (HTML, Plain Text, WebArchive, etc.).
- **GFM Optimized:** Produces clean ATX headers, dash-style bullets, and formatted tables.
- **Smart Fallback:** If no native HTML flavor is found, it attempts to parse raw string data containing HTML tags.
- **Auto-Cleaning:** Automatically strips out `<script>`, `<style>`, and `<meta>` tags to keep your Markdown pure.

---

## Setup (New Machine)

### 1. Prerequisites

- **macOS**
- **Python 3.12+**
- **uv** — install with `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 2. Make executable and symlink into PATH

The script uses inline uv dependencies and a self-executing shebang, so no virtual environment setup is needed.

```bash
chmod +x /path/to/h2m/h2m.py
ln -s /path/to/h2m/h2m.py ~/.local/bin/h2m
```

For example, if the project lives in Dropbox. **Note that Dropbox uses one of two
locations depending on how it was installed** — check which one exists on your machine
before copying a command:

```bash
ls -d ~/Dropbox ~/Library/CloudStorage/Dropbox 2>/dev/null
```

Older installs (and machines upgraded from them) use `~/Dropbox`:

```bash
chmod +x ~/Dropbox/PythonStuff/h2m/h2m.py
ln -s ~/Dropbox/PythonStuff/h2m/h2m.py ~/.local/bin/h2m
```

Newer installs use the File Provider path under `~/Library/CloudStorage`:

```bash
chmod +x ~/Library/CloudStorage/Dropbox/PythonStuff/h2m/h2m.py
ln -s ~/Library/CloudStorage/Dropbox/PythonStuff/h2m/h2m.py ~/.local/bin/h2m
```

Or let the shell pick whichever is present:

```bash
for d in ~/Dropbox ~/Library/CloudStorage/Dropbox; do
  [ -f "$d/PythonStuff/h2m/h2m.py" ] || continue
  chmod +x "$d/PythonStuff/h2m/h2m.py"
  ln -sf "$d/PythonStuff/h2m/h2m.py" ~/.local/bin/h2m
  break
done
```

That's it. Run `h2m` from any directory.

> **Use a symlink (`ln -s`), not a hard link.** A hard link points at the file's inode
> rather than its path, so if Dropbox ever replaces `h2m.py` instead of editing it in
> place, `h2m` will keep silently running a stale copy of the script. Check what you
> have with `ls -l ~/.local/bin/h2m` — a symlink shows an `->` arrow. If it doesn't,
> replace it: `rm ~/.local/bin/h2m` and re-run the `ln -s` above.

> `~/.local/bin` must be on your PATH. If it isn't, add this to your `~/.zshrc`:
> ```bash
> export PATH="$HOME/.local/bin:$PATH"
> ```

---

## Usage

```bash
h2m
```

**Example output:**

```
Pasteboard Flavor Audit:
  - public.html
  - public.utf8-plain-text
  - com.apple.webarchive
-----------------------------------
Success!
   Input:  1240 characters (HTML)
   Output: 850 characters (GFM Markdown)
Your pasteboard now contains the Markdown version.
```

---

## macOS Shortcut (Global Keybind)

To trigger h2m from anywhere without opening a terminal:

1. Open the **Shortcuts** app and create a new Shortcut.
2. Add a **"Run Shell Script"** action.
3. Configure:
   - Shell: `/bin/zsh`
   - Input: `None`
   - Content:
     ```bash
     export PATH="$HOME/.local/bin:$PATH"
     h2m
     ```
4. In the **Shortcut Details** sidebar, click **Add Keyboard Shortcut** — recommended: `Cmd+Shift+M`.

---

## Project Structure

- `h2m.py` — core script with conversion logic and pasteboard interaction
- `pyproject.toml` — project metadata and dependencies
- `README.md` — this file
