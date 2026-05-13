# rMATS-Suite Portal

### **Independent Portal for Alternative Splicing Analysis & Sashimi Visualization**

rMATS-Suite is a high-performance bioinformatics GUI built with Streamlit. It provides a user-friendly wrapper around **rMATS-turbo** and **MISO (Sashimi Plot)**, allowing researchers to move from raw BAM files to publication-ready splicing visualizations without using the command line.

---

## 🌟 Features

* **Automated Analysis:** Compare two groups of RNA-Seq replicates for differential splicing (SE, MXE, A3SS, A5SS, RI).
* **Live Logging:** Real-time terminal output streaming directly to the web interface.
* **Gene Search:** Instantly find specific genes and view all detected splicing events in a searchable table.
* **Interactive Sashimi Plots:** Generate and save high-resolution PDFs of genomic coverage and junction counts.

---

## 📋 Prerequisites

### **Hardware Requirements**

* **Storage:** SSD is highly recommended for faster I/O processing of BAM files.
* **Memory:** Minimum 8GB RAM (16GB+ recommended for large-scale replicates).
* **CPU:** Multi-core processor (at least 4 threads recommended).

### **Software Requirements**

1. **Docker:** [Install Docker Engine](https://docs.docker.com/engine/install/)
2. **Python 3.8+**
3. **SAMtools:** Required for indexing BAM files locally (`sudo apt install samtools`).

---

## 🚀 Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/omprakash24d/rMATS-Suite.git
cd rMATS-Suite

```

### 2. Build the Docker Image

The analysis engine runs inside a container to ensure all legacy dependencies (Python 2.7, GFortran 3, MISO) are perfectly configured. Ensure to run this command from the rMATS-Suite dir, you can check your current working directory using pwd

```bash
docker build -t rmats-suite:latest .

```

### 3. Install Python Dependencies

Install the Streamlit interface requirements:

```bash
pip install -r requirements.txt

```

---

## 🛠 Usage

### 1. Launch the Portal

```bash
streamlit run app.py

```

### 2. Data Preparation

Before running the analysis, ensure your BAM files are coordinate-sorted and indexed. If you see an error regarding missing `.bai` files, run:

```bash
samtools index your_file.bam

```

### 3. Running Analysis

1. Navigate to the **"🚀 Pipeline"** tab.
2. Input the absolute paths to your Group 1 and Group 2 BAM files.
3. Select your GTF annotation and thread count.
4. Click **Execute Analysis**.

### 4. Generating Plots

1. Navigate to the **"📊 Visualization"** tab.
2. Select the directory containing your rMATS results.
3. Search for a gene (e.g., `SRSF11`).
4. Choose the **Event ID** from the table and click **Generate Plot**.

---

## 📁 Project Structure

```text
.
├── app.py                      # Main Streamlit application
├── Dockerfile                  # rMATS binary folder
├── Homo_sapiens.GRCh38.111.chr.gtf         # ReferenceGenome
├── Readme.md                   # Documentation
├── requirements.txt
├── rmats2sashimiplot           # Sashimi plotting scripts
│   ├── __init__.py
│   └── rmats2sashimiplot.py
└── rMATS-turbo-Linux-UCS4
    ├── README-rMATS-turbo.md
    ├── rMATS_C
    │   └── rMATSexe
    ├── rMATS_P
    │   ├── FDR.py
    │   ├── inclusion_level.py
    │   ├── joinFiles.py
    │   └── paste.py
    ├── rmatspipeline.so
    └── rmats.py

```

---

## 🔒 Permission Issues (Linux)

Since Docker runs as root, generated files may be "locked" (read-only). To unlock your results after an analysis, run:

```bash
sudo chown -R $USER:$USER /path/to/your/output_folder

```

---

## 📝 Troubleshooting

* **Docker Error:** Ensure your user is in the docker group: `sudo usermod -aG docker $USER` (then log out and back in).
* **Library Not Found:** If `libgfortran.so.3` is missing, ensure you are using the `rmats-suite:latest` image built from the provided Dockerfile.
* **Sashimi Plot Error:** Ensure the BAM paths provided are absolute and accessible by the Docker container volume mapping.

---

## 🤝 Contributing

Feel free to fork this repo, open issues, or submit pull requests to improve the visualization features!

---

## 🎖️ Credits & Acknowledgements

This portal acts as a graphical wrapper around the following foundational bioinformatics tools developed by the **Xing Lab**:

* **rMATS-turbo**: The high-performance C-engine used for the multivariate analysis of transcript variations.
🔗 [GitHub: Xinglab/rmats-turbo](https://github.com/Xinglab/rmats-turbo)
* **rmats2sashimiplot**: The visualization engine used to produce Sashimi plots from rMATS output and BAM files.
🔗 [GitHub: Xinglab/rmats2sashimiplot](https://github.com/Xinglab/rmats2sashimiplot)
* **MISO (Mixture of Isoforms)**: The underlying framework used by the plotting engine for probabilistic transcript analysis.

### **Citations**

If you use this portal for published research, please ensure you cite the original rMATS paper:

> Shen S, Park JW, Lu ZX, Lin L, Henry MD, Wu YN, Zhou Q, Xing Y. **rMATS: Robust and flexible detection of differential alternative splicing from replicate RNA-Seq data.** *Proc Natl Acad Sci U S A.* 2014;111(51):E5593-601.

---