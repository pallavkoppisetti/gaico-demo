# 📊 GAICo Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gaico-demo.streamlit.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Interactive demonstration of **GAICo (Generative AI Comparator)** — a unified framework for evaluating GenAI outputs across multiple modalities.

> 🎯 **AAAI-26 Demo Track** | January 23, 2026 | USC AI Institute

![GAICo Demo Screenshot](https://via.placeholder.com/800x400?text=GAICo+Demo+Screenshot)

## ✨ Features

- **📝 Text Evaluation** — Compare LLM responses with BLEU, ROUGE, BERTScore
- **🖼️ Image Evaluation** — Assess generated images with SSIM, perceptual hashing
- **🔊 Audio Evaluation** — Evaluate TTS with SNR, spectrogram distance
- **📊 Structured Data** — Compare planning sequences, time-series forecasts

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/ai4society/gaico-demo.git
cd gaico-demo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
gaico-demo/
├── app.py                 # Landing page
├── config.py              # ⚙️ Configuration (paths, constants, styling)
├── pages/                 # Demo sections
│   ├── 2_🧳_Case_Study.py
│   ├── 3_��_Text_Evaluation.py
│   ├── 4_📊_Structured_Data.py
│   ├── 5_💬_LLM_FAQ.py
│   └── 6_🎨_Multi_Modal.py
├── utils/                 # Shared utilities
│   ├── data_loader.py
│   ├── metric_info.py
│   ├── visualizations.py
│   └── ui_components.py
├── data/                  # Evaluation data
└── assets/                # Static assets
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Edit Guide

| Task | File |
|------|------|
| Update conference info | `config.py` |
| Modify page content | `pages/*.py` |
| Change styling | `config.py` → `CUSTOM_CSS` |
| Add metrics | `utils/metric_info.py` |

## 🔗 GAICo Resources

- **GitHub**: [ai4society/GenAIResultsComparator](https://github.com/ai4society/GenAIResultsComparator)
- **PyPI**: [pip install gaico](https://pypi.org/project/gaico/)
- **Documentation**: [ai4society.github.io](https://ai4society.github.io/projects/GenAIResultsComparator/)

## 📄 Citation

```bibtex
@article{gupta2025gaico,
  title={GAICo: A Deployed and Extensible Framework for Evaluating Diverse and Multimodal Generative AI Outputs},
  author={Gupta, Nitin and Koppisetti, Pallav and Lakkaraju, Kausik and Srivastava, Biplav},
  journal={arXiv preprint arXiv:2508.16753},
  year={2025}
}
```

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## 📧 Contact

- **Email**: ai4societyteam@gmail.com
- **Website**: [AI4Society](https://ai4society.github.io/)
