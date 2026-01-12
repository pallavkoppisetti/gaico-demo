# Contributing to GAICo Demo

Thank you for your interest in contributing! This guide will help you get started.

## 🚀 Quick Setup

```bash
# Clone the repository
git clone https://github.com/ai4society/gaico-demo.git
cd gaico-demo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

## 📁 Project Structure

```
├── app.py              # Landing page
├── config.py           # ⚙️ Configuration (edit this for constants)
├── pages/              # Individual demo pages
├── utils/              # Shared utilities
├── data/               # Data files (JSON, CSV)
└── assets/             # Static assets (plots)
```

## 🛠️ How to Contribute

### Updating Content

| Task | File to Edit |
|------|--------------|
| Conference info, dates | `config.py` |
| Page content | `pages/*.py` |
| Styling (CSS) | `config.py` → `CUSTOM_CSS` |
| Metric descriptions | `utils/metric_info.py` |

### Adding a New Page

1. Create `pages/N_🔤_Page_Name.py`
2. Use this template:

```python
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.ui_components import display_header, display_sidebar_links, display_footer

st.set_page_config(page_title="GAICo Demo - Page Name", page_icon="📊", layout="wide")

with st.sidebar:
    display_sidebar_links()

display_header()
st.header("Your Page Title")

# Your content here

display_footer()
```

### Adding Data

1. Add files to `data/` or `data/gaico_results/`
2. Update paths in `config.py` if needed
3. Add loader in `utils/data_loader.py` if needed

## 📋 Pull Request Guidelines

1. **Branch naming**: `feature/description` or `fix/description`
2. **Commits**: Use clear, descriptive messages
3. **Testing**: Run `streamlit run app.py` locally before submitting
4. **Documentation**: Update README if adding new features

## 🐛 Reporting Issues

Please include:
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

## 📜 Code Style

- Follow PEP 8
- Use type hints where helpful
- Keep docstrings concise
- Use meaningful variable names

## 📧 Questions?

Contact: ai4societyteam@gmail.com
