# 🟢 LimeBox

**A sleek terminal-based project runner that works anywhere - from your phone to your server.**

LimeBox automatically detects your project type, installs dependencies, and runs your applications with beautiful lime-colored terminal output. Perfect for Termux on Android, Linux, macOS, or any terminal environment.

```
██╗     ██╗███╗   ███╗███████╗██████╗  ██████╗ ██╗  ██╗
██║     ██║████╗ ████║██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝
██║     ██║██╔████╔██║█████╗  ██████╔╝██║   ██║ ╚███╔╝ 
██║     ██║██║╚██╔╝██║██╔══╝  ██╔══██╗██║   ██║ ██╔██╗ 
███████╗██║██║ ╚═╝ ██║███████╗██████╔╝╚██████╔╝██╔╝ ██╗
╚══════╝╚═╝╚═╝     ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝

Terminal Project Runner v1.0.0
```

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/tgkiddo666/limebox.git
cd limebox
bash setup.sh
```

### 2. Run LimeBox
```bash
python limebox.py run
```

Or use the shorthand:
```bash
./limebox start
```

## ✨ Features

- 🔍 **Auto-detection** - Automatically identifies your project framework
- 📦 **Smart dependencies** - Installs missing packages automatically  
- 🖥️ **Terminal-only** - Pure terminal experience, no GUI required
- 🌐 **Local & Online** - Run on localhost or expose to the internet
- 📱 **Mobile-friendly** - Perfect for Termux on Android
- 🟢 **Lime aesthetics** - Beautiful lime green terminal interface
- 📋 **Live logging** - Real-time colored output for debugging

## 🎯 Supported Frameworks

| Framework | Detection | Auto-Install | Run Command |
|-----------|-----------|--------------|-------------|
| Next.js | ✅ | `npm install` | `npm run dev` |
| React | ✅ | `npm install` | `npm start` |
| Vue.js | ✅ | `npm install` | `npm run serve` |
| Angular | ✅ | `npm install` | `ng serve` |
| Svelte | ✅ | `npm install` | `npm run dev` |
| Node.js | ✅ | `npm install` | `npm start` |
| Flask | ✅ | `pip install -r requirements.txt` | `python app.py` |
| Django | ✅ | `pip install -r requirements.txt` | `python manage.py runserver` |
| FastAPI | ✅ | `pip install -r requirements.txt` | `uvicorn main:app --reload` |
| Python | ✅ | `pip install -r requirements.txt` | `python main.py` |
| PHP | ✅ | `composer install` | `php -S localhost:8000` |
| Static HTML | ✅ | None | `python -m http.server 8000` |

## 📋 Usage

### Main Menu Options
```
1. 📁 Add Local Project    - Add existing project from your filesystem
2. 🌐 Clone from GitHub    - Clone and add a repository
3. 🚀 Run Project         - Start your application with live logs  
4. 📋 List Projects       - View all added projects
5. 🗑️  Remove Project      - Remove project from LimeBox
6. ⚙️  Settings           - View configuration
0. 🚪 Exit               - Close LimeBox
```

### Adding Projects

**Local Project:**
```bash
# LimeBox will prompt you for:
Enter project path: /path/to/your/project
Project name: my-awesome-app
✓ Detected: React
✅ Added project 'my-awesome-app' successfully!
```

**GitHub Repository:**
```bash
# LimeBox will prompt you for:
GitHub repository URL: https://github.com/user/repo.git
Project name: repo
🔄 Cloning repository...
✓ Detected: Next.js  
✅ Cloned and added 'repo' (Next.js)
```

### Running Projects

When you run a project, LimeBox will:
1. 📦 Install dependencies automatically
2. 🚀 Start the development server
3. 📋 Show live logs in beautiful lime colors
4. 🌐 Ask if you want localhost-only or online exposure

## 📱 Termux Setup (Android)

Perfect for mobile development! Install on Android using Termux:

```bash
# Install Termux from F-Droid or Play Store
# Then run these commands:

pkg update && pkg upgrade
pkg install git python nodejs-lts
pip install rich

git clone https://github.com/yourusername/limebox.git
cd limebox
bash setup.sh
python limebox.py run
```

## 🛠️ Installation Details

### Prerequisites
- Python 3.7+
- Git (for cloning repos)
- Node.js & npm (for JavaScript projects)
- pip (for Python projects)

### Manual Setup
If the setup script doesn't work:

```bash
# Install Python dependencies
pip install rich

# Make executable (Linux/Mac)
chmod +x limebox.py

# Run
python limebox.py run
```

## 🎨 Screenshots

```
┌─ Main Menu ──────────────────────────────────────┐
│  1  📁 Add Local Project                         │
│  2  🌐 Clone from GitHub                         │
│  3  🚀 Run Project                               │  
│  4  📋 List Projects                             │
│  5  🗑️  Remove Project                           │
│  6  ⚙️  Settings                                 │
│  0  🚪 Exit                                      │
└──────────────────────────────────────────────────┘
```

```
┌─ Running Project ────────────────────────────────┐
│ 🚀 Starting my-app (React)                      │
│ Command: npm start                               │
│ Path: /home/user/projects/my-app                 │
│ Press Ctrl+C to stop                            │
└──────────────────────────────────────────────────┘

📋 Live Logs:
────────────────────────────────────────────────────
webpack compiled successfully
Local:            http://localhost:3000
On Your Network:  http://192.168.1.100:3000
```

## ⚡ Advanced Usage

### Configuration File
LimeBox stores your projects in `config.json`:

```json
{
  "projects": {
    "my-react-app": {
      "path": "/home/user/projects/react-app",
      "type": "React",
      "source": "local",
      "added": "2024-01-15T10:30:00"
    },
    "awesome-api": {
      "path": "/home/user/projects/fastapi-app", 
      "type": "FastAPI",
      "source": "github",
      "repo_url": "https://github.com/user/awesome-api.git",
      "added": "2024-01-15T11:00:00"
    }
  },
  "last_updated": "2024-01-15T11:00:00"
}
```

### Command Line Arguments
```bash
python limebox.py start    # Start LimeBox (default)
python limebox.py run      # Same as start
./limebox start           # Shorthand (if executable)
```

## 🔧 Troubleshooting

**"Command not found" errors:**
```bash
# Install missing dependencies
# For Node.js projects:
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# For Python projects:
sudo apt install python3-pip

# For PHP projects: 
sudo apt install php composer
```

**Permission denied:**
```bash
chmod +x limebox.py
chmod +x setup.sh
```

**Import errors:**
```bash
pip install --upgrade rich
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

MIT License - feel free to use LimeBox in your projects!

## ⭐ Support

If LimeBox helps you, please give it a star! ⭐

Found a bug? [Open an issue](https://github.com/yourusername/limebox/issues)

---

**Made with 💚 for developers who love terminals**