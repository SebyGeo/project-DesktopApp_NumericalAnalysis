# Numerical Analysis — Polynomial Approximation & Interpolation

O aplicație grafică desktop (GUI) dezvoltată în **Python** cu **PyQt5** și **Matplotlib**, destinată studiului metodelor de aproximare și interpolare a funcțiilor numerice: **Polinoame Bernstein** și **Interpolare Lagrange** (cu opțiuni de comparare SciPy și Cubic Spline).

---

## 📋 Cuprins

- [Caracteristici Principale](#-caracteristici-principale)
- [Fundament Matematic](#-fundament-matematic)
  - [Aproximare cu Polinoame Bernstein](#1-aproximare-cu-polinoame-bernstein)
  - [Interpolare Lagrange](#2-interpolare-lagrange)
- [Structura Proiectului](#-structura-proiectului)
- [Cerințe de Sistem](#-cerințe-de-sistem)
- [Instalare și Rulare](#-instalare-și-rulare)
- [Ghid de Utilizare](#-ghid-de-utilizare)
  - [1. Modul Bernstein](#1-modul-bernstein)
  - [2. Modul Lagrange](#2-modul-lagrange)
  - [3. Exportul Graficelor](#3-exportul-graficelor)
- [Formatul Fișierelor de Date (CSV/TXT)](#-formatul-fișierelor-de-date-csvtxt)

---

## 🚀 Caracteristici Principale

- **Interfață Grafică Intuitivă**: Realizată cu PyQt5, separată în module dedicate pentru fiecare tip de problemă.
- **Evaluare Dinamică de Funcții**: Permite introducerea oricărei expresii matematice compatibile cu NumPy (ex. `np.sin(x)`, `cos(x) + x**2`, `exp(-x)`).
- **Aproximare Bernstein**:
  - Ajustare dinamică a intervalului $[a, b]$ și a gradului polinomului $n$.
  - Evaluare punctuală a erorilor: eroare absolută și eroare relativă procentuală.
- **Interpolare Lagrange**:
  - Introducere date fie manual de la tastatură (puncte X calculate pe baza funcției alese), fie prin încărcare din fișier extern (`.csv`, `.txt`).
  - Implementare proprie a metodei Lagrange.
  - **Mod Comparativ**: Compară grafic implementarea proprie cu `scipy.interpolate.lagrange` și `CubicSpline` (spline cubic).
- **Vizualizare Interactivă & Export**:
  - Grafice generate în timp real folosind Matplotlib.
  - Exportul graficelor în formate de înaltă rezoluție: PNG, JPG, PDF.

---

## 📐 Fundament Matematic

### 1. Aproximare cu Polinoame Bernstein
Pentru o funcție continuă $f : [a, b] \to \mathbb{R}$, polinomul Bernstein de ordin $n$ este definit ca:

$$B_n(f; x) = \sum_{k=0}^{n} f\left(a + \frac{k}{n}(b - a)\right) \binom{n}{k} \left(\frac{x - a}{b - a}\right)^k \left(1 - \frac{x - a}{b - a}\right)^{n - k}$$

Aplicația calculează și erorile de aproximare într-un punct dat $x_{\text{eval}} \in [a, b]$:
- **Eroare absolută**: $\epsilon_{\text{abs}} = |f(x) - B_n(x)|$
- **Eroare relativă**: $\epsilon_{\text{rel}} = \frac{|f(x) - B_n(x)|}{|f(x)|} \times 100\%$

### 2. Interpolare Lagrange
Pentru un set de $n+1$ noduri distincte $(x_0, y_0), (x_1, y_1), \dots, (x_n, y_n)$, polinomul de interpolare Lagrange de grad cel mult $n$ este dat de:

$$L(x) = \sum_{j=0}^{n} y_j \ell_j(x)$$

unde polinoamele de bază Lagrange sunt:

$$\ell_j(x) = \prod_{\substack{0 \le i \le n \\ i \neq j}} \frac{x - x_i}{x_j - x_i}$$

---

## 📂 Structura Proiectului

```text
├── gui.py             # Definiția interfeței grafice (generată via PyQt5)
├── main.py            # Punctul de intrare (logica GUI, plotting, gestionare evenimente)
├── math_functions.py  # Algoritmii numerici (Bernstein, Lagrange, parsare expresii)
├── requirements.txt   # Dependențele proiectului
└── README.md          # Documentația proiectului
```

---

## 💻 Cerințe de Sistem

- **Python 3.8+**
- Pachete Python:
  - `numpy`
  - `scipy`
  - `matplotlib`
  - `PyQt5`

---

## 🔧 Instalare și Rulare

1. **Clonează depozitul Git:**
   ```bash
   git clone https://github.com/username/nume-proiect.git
   cd nume-proiect
   ```

2. **Creează un mediu virtual (recomandat):**
   ```bash
   python -m venv venv
   # Pe Linux/macOS:
   source venv/bin/activate
   # Pe Windows:
   venv\Scripts\activate
   ```

3. **Instalează dependențele:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Dacă nu ai `requirements.txt`, rulează direct: `pip install numpy scipy matplotlib PyQt5`)*

4. **Lansează aplicația:**
   ```bash
   python main.py
   ```

---

## 📖 Ghid de Utilizare

### 1. Modul Bernstein
1. Selectează **Approximation (Bernstein)** din lista derulantă superioară.
2. Completează parametrii:
   - **Function f(x)**: expresia funcției (ex. `np.sin(x)`, `np.exp(x)`).
   - **Lower bound (a)** și **Upper bound (b)**: limitele intervalului ($a < b$).
   - **Maximum order (n)**: gradul polinomului Bernstein.
   - **Evaluation point (x)**: punctul în care dorești calculul numeric al erorii.
3. Apasă pe **Calculate**. Panoul lateral va afișa valorile exacte, aproximate și erorile, iar graficul va prezenta $f(x)$ vs. $B_n(x)$.

### 2. Modul Lagrange
1. Selectează **Interpolation (Lagrange)**.
2. Alege sursa datelor (**Data source**):
   - **Keyboard**: introdu nodurile $X$ separate prin virgulă (ex: `0, 1, 2, 3`) și funcția $f(x)$ pentru generarea automată a punctelor $Y$.
   - **File**: încarcă un fișier CSV/TXT conținând coordonatele $(x, y)$.
3. *(Opțional)* Bifează **Compare (Scipy Lagrange & Cubic Spline)** pentru a suprapune pe grafic aproximarea spline cubică și metoda din SciPy.
4. Apasă pe **Calculate**.

### 3. Exportul Graficelor
- După generarea oricărui grafic, apasă butonul **Export Plot**.
- Selectează locația și formatul dorit (`.png`, `.jpg` sau `.pdf`).

---

## 📄 Formatul Fișierelor de Date (CSV/TXT)

Pentru opțiunea de încărcare din fișier la interpolarea Lagrange, fișierele trebuie să conțină valori numerice separate prin virgulă, pe două coloane sau două rânduri:

```csv
0.0, 0.0
1.0, 0.8414
2.0, 0.9092
3.0, 0.1411
```

Sau pe două rânduri:
```csv
0.0, 1.0, 2.0, 3.0
0.0, 0.8414, 0.9092, 0.1411
```