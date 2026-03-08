# Tricog Health - ECG Noise Detection & Filtering (ML Internship)

**Jul-Nov 2021 Tricog Health ML Internship**: Built ECG signal quality assessment pipeline achieving **90% accuracy** on PhysioNet dataset. Filtered noise for clinical-grade diagnostics.

**My Contributions** (End-to-end ownership):
- **CNN Prototype** (PyTorch): Noise detection/classification
- **SVM Baseline**: Comparative model evaluation
- **Data Pipeline**: Shell parsing → Python preprocessing (normalization)
- **Demo**: Full ML pipeline presentation to engineering team

## 🎯 Clinical Impact
Early-stage noise filtering enables reliable arrhythmia detection in wearable ECG devices.

## 🧠 ML Pipeline
- Proprietary ECG (.dat/.atr) → convert.sh (shell parsing)
                          ↓
- Raw signals → DivSetv2.py (normalization, cleaning)
                          ↓
- Features → DatasetC.csv → CNN (PyTorch) vs SVM baseline
                          ↓
- 90% accuracy → ColmOutput.csv + plots/

## 🚀 Quick Start

```bash
git clone https://github.com/amanjakunnel/tricog.git
cd tricog
pip install torch torchvision scikit-learn pandas numpy matplotlib

# Run pipeline
bash convert.sh           # Parse proprietary ECG files
python DivSet.py         # Preprocess/normalize
python Classifier.py     # CNN + SVM training
python Plot.py           # Results visualization
