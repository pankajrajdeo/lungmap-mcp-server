#!/bin/bash

# LungMAP MCP Server Setup Script
# This script sets up the complete directory structure and files

set -e

echo "🫁 Setting up LungMAP MCP Server..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p tools
mkdir -p tests

# Create __init__.py files
echo "📝 Creating __init__.py files..."
touch tools/__init__.py
touch tests/__init__.py

# Check if Python 3.10+ is available
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.10 or higher is required (found $python_version)"
    exit 1
fi

echo "✅ Python version $python_version is compatible"

# Install dependencies
echo "📦 Installing dependencies..."
if command -v uv &> /dev/null; then
    echo "Using uv package manager..."
    uv pip install -e .
elif command -v pip &> /dev/null; then
    echo "Using pip package manager..."
    pip install -e .
else
    echo "❌ Error: No package manager found (pip or uv required)"
    exit 1
fi

# Test the server
echo "🧪 Testing server startup..."
timeout 3 python3 lungmap_mcp_server.py > /dev/null 2>&1 || true

if [ $? -eq 124 ]; then
    echo "✅ Server starts successfully (timed out as expected for stdio)"
else
    echo "⚠️  Server may have issues, check manually"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Verify all tool files are in the tools/ directory"
echo "2. Test the server: python3 lungmap_mcp_server.py"
echo "3. Configure your MCP client (see README.md)"
echo ""
echo "📖 For usage instructions, see README.md"
