# Quantum Pigeonhole Paradox

**Author:** Dikran Meliksetian (Qiskit Advocate)  
**Date:** 2025  
**Compatible Qiskit version:** 2.x

---

## 🧠 Overview
This tutorial explores the **quantum pigeonhole paradox** — a counterintuitive result from pre-/post-selection quantum mechanics, where three particles appear never to share two boxes.

We show:
1. How a **single ancilla parity check** reveals the paradox for any pair.  
2. Why using **three ancillas simultaneously** collapses the interference pattern.  
3. How a **weak, reversible probe** (compute → $R_y(ε)$ → uncompute) restores the paradox, connecting to **weak measurement theory**.

---

## 🧩 Learning Goals
- Represent pre-/post-selection circuits in Qiskit.  
- Understand ancilla-based parity checking and post-selection.  
- Observe interference collapse and recovery via weak measurement.  
- Compute weak values and confidence intervals.  

---

## ⚙️ Requirements

You can install dependencies with:

```bash
conda env create -f environment.yml
conda activate pigeonhole
```

or with `pip`:

```bash
pip install qiskit qiskit-aer matplotlib numpy
```

---

## ▶️ Running the Notebook

Launch Jupyter and open:

```
quantum_pigeonhole_paradox_qiskit_tutorial.ipynb
```

Execute all cells sequentially. Inline circuit diagrams will appear automatically.

---

## 🧪 References

- Y. Aharonov, D. Rohrlich, *Quantum Paradoxes: Quantum Theory for the Perplexed*, Wiley-VCH (2005).  
- N. Katz *et al.*, “Reversal of the weak measurement of a quantum state in a superconducting phase qubit,” *Phys. Rev. Lett.* **101**, 200401 (2008).  
- Y. Aharonov *et al.*, “Quantum violation of the pigeonhole principle,” *PNAS* **111** (14), 4602–4605 (2014).  

---

## 🧾 Citation

If you use or adapt this work, please cite:

> Dikran Meliksetian (Qiskit Advocate),  
> *The Quantum Pigeonhole Paradox in Qiskit 2.x: From Strong to Weak Measurements*,   
> DOI: 10.5281/zenodo.17387139.

---

## 🤖 Acknowledgments
This notebook was developed with assistance from AI tools(ChatGPT Anthropic Claude and Google Gemini) for drafting, code refactoring, and LaTeX/Markdown formatting. All content was reviewed and verified by the author.
