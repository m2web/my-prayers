# How to run the **Docker's and Boxed Codex CLI** running inside Ubuntu on WSL2

Below is a concise, “works-on-my-laptop” recipe for getting the **Docker‑sandboxed Codex CLI** running inside Ubuntu on WSL2.  
Everything happens inside your WSL distribution—the Windows side is only used to host Docker Desktop.

---

## 1. Prerequisites on Windows

| What | How |
|------|-----|
| **WSL 2** | From an elevated PowerShell prompt:<br>`wsl --install -d Ubuntu-22.04` (reboot if asked). |
| **Docker Desktop ≥ 4.32** | Download & install for Windows. In **Settings ▸ Resources ▸ WSL Integration** enable your Ubuntu distro and switch Docker Desktop to *Linux containers* mode. |
| **Virtualisation** | Make sure “VirtualMachinePlatform” + “WSL” Windows features are enabled and BIOS/UEFI virtualisation is on. |

---

## 2. Prep the Linux side (inside the WSL shell)

```bash
# Keep packages current
sudo apt update && sudo apt upgrade -y

# Install build tools you may need later
sudo apt install -y git build-essential

# Node.js 22 (Codex requires ≥22)
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# Verify versions
node -v   # v22.x
npm  -v   # 10.x+
```

---

## 3. Clone and build the Codex sandbox image

```bash
git clone git@github.com:ymichael/open-codex.git
cd codex/codex-cli

# Build the lightweight container image as "codex"
docker build -t codex .
```

The `Dockerfile` bakes the CLI, adds a tiny toolchain and copies a firewall script that later blocks all outbound traffic except the OpenAI API.

---

## 4. Export your API key

```bash
echo 'export OPENAI_API_KEY="sk-••••••••••••"' >> ~/.bashrc
source ~/.bashrc
```

*(The CLI also picks up a `.env` file, but an env‑var is simplest.)*

---

## 5. Run Codex inside the sandbox

The helper script `scripts/run_in_container.sh`:

* Removes any stale container  
* Launches `codex` in a detached container with `--cap-add=NET_ADMIN,NET_RAW`  
* Mounts **your current directory** into the same path in the container  
* Calls the firewall bootstrap script, then executes Codex in **Full‑Auto** mode.

Codex will open an interactive session, propose patches and commands, and execute them—all isolated inside the Docker sandbox.

---

## 6. Quality‑of‑life tips

* **Keep code on the Linux side** (e.g. `~/projects`, not `/mnt/c/...`) for much faster file‑system performance under WSL2.  
* If you ever see `Sandbox was mandated, but no sandbox is available!` you either ran plain `codex` instead of `codexc`, or Docker isn’t reachable from WSL; verify `docker info` works.  
* To upgrade Codex later:

  ```bash
  npm i -g @openai/codex@latest   # updates CLI on host
  cd ~/codex/codex-cli && git pull && docker build -t codex .
  ```

---

## 7. One‑liner cheat‑sheet

```bash
# fresh Ubuntu WSL session
sudo apt update && sudo apt install -y git curl   && curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -   && sudo apt install -y nodejs   && git clone https://github.com/openai/codex.git   && cd codex/codex-cli && docker build -t codex .   && echo 'alias codexc="$HOME/codex/codex-cli/scripts/run_in_container.sh"' >> ~/.bashrc
```

Reload your shell, set `OPENAI_API_KEY`, and you’re ready to hack with Codex—now safely sandboxed even on Linux inside WSL2!

## 8. Here is what you do now because you:
Created a handy wrapper:

```bash
# Still in codex/codex-cli
chmod +x scripts/run_in_container.sh
echo 'alias codexc="~/code/ai/open-codex/codex-cli/scripts/run_in_container.sh"' >> ~/.bashrc
source ~/.bashrc
```

Now use it from **any** repo directory (inside WSL):

```bash
cd ~/projects/my-app          # your codebase
codexc "add Jest unit tests for utils/*.ts"
```
