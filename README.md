# Numerical-Analysis-GUI

This repository provides a user-friendly GUI application built with CustomTkinter for performing numerical analysis tasks, specifically solving linear systems and numerical integration.

![image](https://github.com/AkramOM606/Numerical-Analysis-GUI/assets/162604610/c36c0dac-33fb-4c4b-8704-b1989c636e83)

![image](https://github.com/AkramOM606/Numerical-Analysis-GUI/assets/162604610/faf5b9b9-7814-4f8e-986e-224c2c49e4bb)

## Description

It offers functionalities for:

* **Solving Linear Systems (Ax = B):**
    * **Inverse of A:** Computes the exact solution using the matrix inverse.
    * **Gaussian Elimination:** Solves the system using forward and backward substitution after LU decomposition.
    * **LU Decomposition:** Factors the coefficient matrix (A) into a lower triangular matrix (L) and an upper triangular matrix (U) for efficient solution.
    * **Cholesky Decomposition (for positive definite A):** Exploits the positive definite nature of the matrix for a more efficient solution process.
* **Numerical Integration:**
    * **Trapezoidal Rule:** Approximates the definite integral of a function using trapezoidal segments.
    * **Simpson's Rule:** Provides a more accurate approximation compared to the trapezoidal rule using parabolic segments.

## Key Features

* **Intuitive GUI:** Easy-to-use interface for inputting matrices, vectors, functions, and integration limits.
* **Clear Output:** Presents solutions and integration results in a structured format.
* **Customization:** Supports adjustments to matrix/vector dimensions and integration parameters.

## Installation

**Prerequisites and Dependencies:**

* Python (assumed to be installed)
* CustomTkinter
* NumPy
* NumExpr
* Pillow

## Running the Application

1. Clone this repository:
```bash
git clone https://github.com/AkramOM606/Numerical-Analysis-GUI.git
```
2. Install the additional dependencies if not present:
```bash
pip install -r requirements.txt
```
3. Launch the application using Python
```bash
python main.py
```

## Usage

The application features a user-friendly interface that allows you to directly interact with its functionalities. Simply launch the application and explore the available options within the GUI. The intuitive design guides you through matrix/vector input, method selection, and function/integration parameter specification.

## Contributing

We welcome contributions to enhance this project! Here's how you can participate:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Open a pull request to propose your changes.

We'll review your pull request and provide feedback promptly.

## License

This project is licensed under the MIT License: [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT) (see LICENSE.md for details).
