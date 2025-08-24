#!/bin/bash

# LimeBox Setup Script
# Automatically installs dependencies for LimeBox

echo "🟢 Setting up LimeBox..."
echo "=================================="

# Colors for output
LIME='\033[1;32m'
RED='\033[1;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_lime() {
    echo -e "${LIME}$1${NC}"
}

print_red() {
    echo -e "${RED}$1${NC}"
}

print_yellow() {
    echo -e "${YELLOW}$1${NC}"
}

# Check if running in Termux
if [ -n "$TERMUX_VERSION" ]; then
    print_lime "📱 Detected Termux environment"
    TERMUX=true
else
    print_lime "💻 Detected standard Linux/Mac environment"
    TERMUX=false
fi

# Update package lists
print_lime "📦 Updating package lists..."
if [ "$TERMUX" = true ]; then
    pkg update -y
    pkg upgrade -y
else
    # Try different package managers
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
    elif command -v yum &> /dev/null; then
        sudo yum update
    elif command -v brew &> /dev/null; then
        brew update
    fi
fi

# Install Python if not available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    print_yellow "🐍 Installing Python..."
    if [ "$TERMUX" = true ]; then
        pkg install -y python
    else
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y python3 python3-pip
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3 python3-pip
        elif command -v brew &> /dev/null; then
            brew install python3
        else
            print_red "❌ Could not install Python. Please install manually."
            exit 1
        fi
    fi
else
    print_lime "✅ Python is already installed"
fi

# Install pip if not available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    print_yellow "📦 Installing pip..."
    if [ "$TERMUX" = true ]; then
        pkg install -y python-pip
    else
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y python3-pip
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3-pip
        fi
    fi
else
    print_lime "✅ pip is already installed"
fi

# Install Git if not available
if ! command -v git &> /dev/null; then
    print_yellow "🔧 Installing Git..."
    if [ "$TERMUX" = true ]; then
        pkg install -y git
    else
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y git
        elif command -v yum &> /dev/null; then
            sudo yum install -y git
        elif command -v brew &> /dev/null; then
            brew install git
        else
            print_red "❌ Could not install Git. Please install manually."
        fi
    fi
else
    print_lime "✅ Git is already installed"
fi

# Install Node.js and npm (optional but recommended)
if ! command -v node &> /dev/null; then
    print_yellow "🟢 Installing Node.js..."
    if [ "$TERMUX" = true ]; then
        pkg install -y nodejs-lts
    else
        if command -v apt-get &> /dev/null; then
            # Install Node.js LTS
            curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
            sudo apt-get install -y nodejs
        elif command -v yum &> /dev/null; then
            sudo yum install -y nodejs npm
        elif command -v brew &> /dev/null; then
            brew install node
        else
            print_yellow "⚠️  Could not install Node.js. Install manually for JS projects."
        fi
    fi
else
    print_lime "✅ Node.js is already installed"
fi

# Install Python dependencies
print_lime "🐍 Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
elif command -v pip &> /dev/null; then
    pip install -r requirements.txt
else
    print_red "❌ Could not find pip. Please install Python dependencies manually."
    print_yellow "Run: pip install rich"
    exit 1
fi

# Make limebox.py executable
print_lime "🔧 Making LimeBox executable..."
chmod +x limebox.py

# Create symlink for easy access (optional)
if [ ! -f "limebox" ]; then
    echo '#!/bin/bash' > limebox
    echo 'python3 limebox.py "$@"' >> limebox
    chmod +x limebox
    print_lime "✅ Created 'limebox' shortcut"
fi

# Test installation
print_lime "🧪 Testing installation..."
if python3 -c "import rich; print('Rich library: OK')" 2>/dev/null; then
    print_lime "✅ Python dependencies installed successfully"
else
    print_red "❌ Python dependencies failed to install"
    exit 1
fi

print_lime ""
print_lime "🎉 LimeBox setup complete!"
print_lime "=================================="
print_lime "Run LimeBox with:"
print_lime "  python3 limebox.py run"
print_lime "  ./limebox start"
print_lime ""
print_lime "For help, check README.md"
print_lime "Happy coding! 🚀"