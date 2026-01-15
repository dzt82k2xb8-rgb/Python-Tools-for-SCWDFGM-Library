# Python Tools for SCWD-FGM Library

## Overview

This repository provides a **Python code collection for integrating FlameMaster with OpenFOAM**. The package extracts required parameters from FlameMaster simulation results and generates an **SCWD-FGM (Statistically Conditioned Weakly-Dissipative Flamelet Generated Manifold) library** for OpenFOAM by integrating preset probability density functions (PDFs) over multiple control variables.

The workflow starts from FlameMaster-generated flamelet data and ends with FGM tables that can be **directly used in OpenFOAM simulations**.

---

## Features

* Automatic extraction of required parameters from FlameMaster `.kg` files
* Progressive generation of **3D → 4D → 5D FGM libraries**
* PDF-based integration using:

  * **Beta-PDF** for mixture fraction
  * **Delta-PDF** for progress variables, dilution factor, and enthalpy loss factor
* Direct export of OpenFOAM-readable FGM tables

---

## Script Overview

The package consists of **7 Python scripts**, each serving a specific role in the SCWD-FGM library generation process.

### 1. `LT2need.py`

**Purpose:**
Reads multiple FlameMaster-generated files (`.kg`) from a specified directory, extracts the required parameters, and merges them into sorted small flamelet solutions. The processed data are saved in **CSV format** for subsequent steps.

---

### 2. `FGM_3D.py`

**Purpose:**
Reads the CSV-format flamelet solution files, integrates the **mixture fraction** using a **Beta-PDF**, and integrates the **normalized progress variables** using a **Delta-PDF**. The result is a **3D FGM data file** stored in `.npy` format.

---

### 3. `FGM_3Dto4D.py`

**Purpose:**
Reads the 3D FGM data file and integrates the **dilution factor** using a **Delta-PDF**, producing a **4D FGM data file** in `.npy` format.

---

### 4. `FGM_4Dto5D.py`

**Purpose:**
Reads the 4D FGM data file and integrates the **enthalpy loss factor** using a **Delta-PDF**, generating the final **5D FGM data file** in `.npy` format.

---

### 5. `FGM_5D_print.py`

**Purpose:**
Converts the 5D FGM data stored in `.npy` format into a structure **directly readable by OpenFOAM**. The resulting files are saved in the `FGM_table` directory.

---

### 6. `beta_integration.py`

**Purpose:**
Provides subroutines for **Beta-PDF integration** of relevant control variables.

---

### 7. `flamelet_integration.py`

**Purpose:**
Contains subroutines for integrating **small flamelet solutions**, used throughout the FGM generation process.

---

## Requirements

* **Python version:** Python 3.12 (tested)
* **Required libraries:**

  * `numpy`
  * `pandas`
  * other standard scientific Python libraries as needed

> ⚠️ Compatibility with Python versions other than 3.12 has not been fully tested.

---

## Usage

1. Place the required FlameMaster-generated `.kg` files into the designated input directory.
2. Run the scripts in the following order:

   ```bash
   python LT2need.py
   python FGM_3D.py
   python FGM_3Dto4D.py
   python FGM_4Dto5D.py
   ```
3. Convert the final 5D FGM data into OpenFOAM-readable tables:

   ```bash
   python FGM_5D_print.py
   ```
4. Use the generated FGM tables in your OpenFOAM simulations.

---

## Important Notes

* Ensure that **input paths and output directories** are correctly set in each script before execution.
* Large datasets may require significant memory during the PDF integration steps.

---

## License

This project is licensed under the **MIT License**.

---

## Contributions

Contributions are welcome!
Feel free to fork this repository and submit pull requests for improvements, optimizations, or bug fixes.

---

## Acknowledgements

This work builds upon the foundational theories and numerical methods in **computational combustion research**.
Special thanks to the developers and research communities behind **FlameMaster** and **OpenFOAM**, whose tools make this integration possible.
