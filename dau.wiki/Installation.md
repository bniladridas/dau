# Installation Guide

## Prerequisites
- Python 3.8+
- pip package manager

## Setup Steps

### 1. Clone the Repository
```bash
git clone https://github.com/bniladridas/dau.git
cd dau
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
# Run Comprehensive Demo
python3 -m comprehensive_demo

# OR Run Full Workflow
./dau_analysis.sh
```

## Troubleshooting
- Ensure you have the latest version of pip
- Check Python version compatibility
- Refer to [Troubleshooting](Troubleshooting) for common issues
