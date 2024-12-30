
# SLE Detection Using Machine Learning

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-green)](https://www.python.org/downloads/)
[![GitHub Issues](https://img.shields.io/github/issues/norsechurros/SLE-Detection)](https://github.com/norsechurros/SLE-Detection/issues)

## Overview

This repository focuses on early detection of **Systemic Lupus Erythematosus (SLE)** in **Indian patients** using machine learning models. It includes end-to-end pipelines for preprocessing gene expression datasets, feature engineering, and building predictive models.

The objective is to compare and evaluate models like:
- **Fuzzy Random Forests (RF)** for differential gene expression (DEG) analysis.
- **Recurrent Neural Networks (RNN)** and **k-Nearest Neighbors (KNN)** for classification and risk prediction.

---

## Prerequisites

Ensure the following are installed:
- **Python 3.10+**
- **Git**
- Required Python packages:
  ```bash
  pip install -r requirements.txt
  ```

---

## Workflow: How to Use This Repository

### 1. Clone the Repository
```bash
git clone https://github.com/norsechurros/SLE-Detection.git
cd SLE-Detection
```

### 2. Data Preparation

1. **Download GEO Datasets**  
   Use `geoparse.py` to fetch datasets from the GEO database:
   ```bash
   python extraction/geoparse.py
   ```

2. **Map Gene Expressions to Platform Annotations**  
   Use `mapper.py` to map expression data to gene metadata:
   ```bash
   python extraction/mapper.py
   ```

3. **Label and Clean Metadata**  
   Use `label_metadata.py` to generate labeled metadata:
   ```bash
   python preprocessing/label_metadata.py
   ```

### 3. Preprocess Data

Run the preprocessing pipeline to clean, normalize, and prepare datasets:
```bash
python preprocessing/preprocess.py
```

### 4. Train Models

Navigate to the `models/` folder and train your machine learning models:
```bash
python train_model.py
```

### 5. Analyze Results

Open Jupyter notebooks to visualize and analyze the results:
```bash
jupyter notebook
```

---

## Future Work

- Integration with the **INSPIRE database** for Indian demographic-specific SLE research.
- Adding more ML models like Support Vector Machines (SVM) and Gradient Boosting.
- Visualization dashboards for interactive data analysis.

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to your branch (`git push origin feature-branch`).
5. Create a Pull Request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

**Vansh Yadav**  
GitHub: [@norsechurros](https://github.com/norsechurros)

---

## Acknowledgements

- [GEO Database](https://www.ncbi.nlm.nih.gov/geo/) for providing gene expression data.
- [INSPIRE Database](https://www.ncbi.nlm.nih.gov/) for Indian patient demographics.
- Open-source contributors for supporting this work.
```

---

### Steps to Use It:
1. Save this content as `README.md` in your repository.
2. Replace placeholder details (e.g., database links, personal details) with specifics of your project.
3. Push it to GitHub using:
   ```bash
   git add README.md
   git commit -m "Add project README"
   git push
   ```

Let me know if further adjustments are required!
