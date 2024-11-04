# Automating CSV Data Analysis with LLMs: A Comprehensive Workflow


## Implementation Guide

Follow these steps to deploy the workflow:

1. **Clone the source code from GitHub**:
   ```bash
   git clone https://github.com/mail2mhossain/csv_data_analysis.git
   cd csv_data_analysis
   ```

2. **Create a Conda environment**:
   ```bash
   conda create -n csv_analysis_env python=3.11
   ```

3. **Activate the environment**:
   ```bash
   conda activate csv_analysis_env
   ```

4. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the app**:
   ```bash
   streamlit run app.py
   ```

To remove the environment when done:
```bash
conda remove --name csv_analysis_env --all
```