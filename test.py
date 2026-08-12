from pathlib import Path

content = """# Python
__pycache__/
*.pyc
.venv/
venv/

# Secrets – never commit these
.env
.env.local
*.key

# OS
.DS_Store
"""

path = Path.cwd() / ".gitignore"
path.write_text(content, encoding="utf-8")

print(f"Created: {path}")