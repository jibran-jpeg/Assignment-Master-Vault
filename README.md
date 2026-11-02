# 🎓 Assignment Master Vault & Anti-AI Academic Engine

> **Philosophy:** *Zero AI Footprint. 100% Genuine Student Academic Integrity. Uncompromising Technical Precision.*

The **Assignment Master Vault** is a production-grade knowledge base, markdown playbook, and document generation engine. It enables university students and AI coding assistants (Antigravity, Cursor, Claude Code, ChatGPT, Windsurf) to generate assignments across **any discipline** (Computer Science, Software Engineering, Image Processing, Ethics, Mathematics, Physics, Humanities) that look, read, and feel like they were meticulously crafted by a top-tier undergraduate student.

---

## ⚡ Key Highlights

* 🛡️ **Zero AI Footprint:** Eliminates detectable LLM patterns (burstiness calibration, perplexity engineering, and a total ban on AI cliché phrases like *"In conclusion"*, *"Delving into"*, *"Tapestry"*, *"Beacon"*).
* 📄 **Cover Page Fidelity (Zero Layout Rupture):** Preserves the professor's original title page down to font sizes, logos, underlines, and border geometry.
* 🚫 **Universal Ban on Notion/Web Callouts:** Strictly eliminates single-cell bordered callout boxes and equation background shading in MS Word (the #1 dead-giveaway of AI generation).
* 📊 **Publication-Standard APA 7th Tables:** Three horizontal rules, zero vertical borders, formal captions, and `<w:cantSplit/>` row integrity.
* 👤 **Dynamic Multi-Student & Multi-University Architecture:** Adapts instantly to any student name, registration number, university, department, and semester through a local, private profile.
* 🖨️ **Dual Output Automation:** One-click compilation to clean `.docx` and publication-ready `.pdf` via headless LibreOffice.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/jibran-jpeg/Assignment-Master-Vault.git
cd Assignment-Master-Vault
```

### 2. Install Prerequisites
Python 3.8+ and `python-docx` are required. (Optional: LibreOffice for PDF compilation).
```bash
pip install python-docx
```

### 3. Configure Your Student Profile (One-time)
Run the interactive setup wizard. It will prompt you for your academic credentials:
```bash
python setup_profile.py
```
> 🔒 **Privacy Guarantee:** Your information is saved locally to `student_profile.json`, which is excluded by `.gitignore` and is **never** committed to Git.

### 4. Generate an Assignment
You can generate a formatted template assignment immediately:
```bash
# Interactive mode:
python generate_assignment.py --interactive

# Or command line flags:
python generate_assignment.py --course "Data Structures" --title "Assignment 02 - Binary Trees" --instructor "Dr. Smith"
```

---

## 🤖 Using with AI Agents (Cursor, Antigravity, Claude, ChatGPT)

When using an AI agent to solve assignments in this repository:

1. **Automatic Profile Check:** The agent will inspect `student_profile.json`. If you haven't set it up yet, the agent will **ask you for your credentials** (Name, ID, University, Course) before writing any code.
2. **Master Prompt Template:** You can copy-paste the agent prompt directly from `06 - Agent Execution & QA Cheatsheet/06.1 - The Jhengo Kisam Prompt Template.md`:

```text
Follow the master rules from the Obsidian Assignment Vault:
1. Dynamic Student Profile: Load credentials from student_profile.json or ask me for my Name, ID, University, and Course.
2. Strict Page 1 Preservation: Replicate the cover page geometry with 100% fidelity. Fill my name and reg ID into the designated blanks without breaking margins.
3. Zero AI Footprint: Write in an authentic senior undergraduate voice. Strictly ban generic AI transition phrases ("In conclusion", "delving into", "crucial to note", "tapestry", "beacon").
4. Anti-AI Tables: DO NOT generate generic 4-column summary tables. Use structured technical bullet points or APA 7th tables.
5. Standard Black Text Only: All body text, headings, and labels must be #000000.
6. No Em-Dashes: Use standard hyphens (-) or colons (:) in titles.
7. Output: Export clean .docx in ./output/<Course_Name>/ and convert to .pdf via LibreOffice.
```

---

## 🗺️ Vault Architecture & Map of Content (MOC)

```
Assignment-Master-Vault/
├── 00 - Master Index & Navigation/
│   └── 00.0 - MOC (Map of Content).md
├── 01 - Core Profile & Document Standards/
│   ├── 01.1 - Student Default Profile.md
│   ├── 01.2 - Cover Page Strict Preservation Protocol.md
│   └── 01.3 - Master Word Document (DOCX) Standards.md
├── 02 - Anti-AI & Human Writing Playbook/
│   ├── 02.1 - The Anti-AI Manifesto.md
│   ├── 02.2 - The Banned Phrase Index & Natural Replacements.md
│   ├── 02.3 - The Table Problem (Anti-AI Data Presentation).md
│   ├── 02.4 - Voice & Tone Calibration by Level.md
│   └── 02.5 - Document Design Humanization & Anti-AI Formatting Standards.md
├── 03 - Subject Playbooks/
│   ├── 03.1 - Computer Science & Software Engineering.md
│   ├── 03.2 - Digital Image Processing & Signal Processing.md
│   ├── 03.3 - Business Technology & Ethics.md
│   ├── 03.4 - Mathematics, Calculus & Applied Physics.md
│   └── 03.5 - English, Humanities & Technical Writing.md
├── 04 - Visuals & Diagram Engine/
│   ├── 04.1 - Scientific & Textbook Plotting Engine.md
│   ├── 04.2 - Architecture & Flowchart Diagrams.md
│   └── 04.3 - Mathematical & Geometric Plotting.md
├── 05 - Automation Scripts & Templates/
│   ├── 05.1 - Master python-docx Generator Template.md
│   └── 05.2 - Reference Scripts Index.md
├── 06 - Agent Execution & QA Cheatsheet/
│   ├── 06.1 - The Jhengo Kisam Prompt Template.md
│   └── 06.2 - Quality Assurance Pre-Flight Checklist.md
├── setup_profile.py              # Interactive student credential wizard
├── generate_assignment.py        # Production-grade APA 7th docx/pdf builder
├── student_profile.template.json # Configuration template
└── README.md
```

---

## ⚖️ Core Document Formatting Rules

| Rule | Requirement | AI Generator Red Flag (Avoided) |
| :--- | :--- | :--- |
| **Color Palette** | Pure `#000000` text everywhere | Cyan, teal, or colored `#0078D7` headings |
| **Section Titles** | Standard hyphens (`-`) or colons (`:`) | Em-dashes (`—`) or en-dashes (`–`) |
| **Callout Boxes** | Zero single-cell shaded boxes | Notion-style grey callouts with thick left borders |
| **Equations** | Centered plain paragraphs in Times New Roman | Tables with background fill or raw `r_k` ASCII |
| **Tables** | 3 horizontal rules (APA 7th), shaded header | Floating tables with vertical grid lines |
| **Vocabulary** | Natural student technical prose | "In conclusion", "Tapestry", "Beacon", "Delving" |

---

## 📖 Obsidian Vault Usage

This repository is a fully functional **Obsidian Vault**:
1. Open Obsidian.
2. Select **"Open folder as vault"**.
3. Choose the `Assignment-Master-Vault` directory.
4. Navigate using `00.0 - MOC (Map of Content).md` or the internal `[[Wikilinks]]`.

---

## 📜 License & Academic Integrity

This project is open-source under the MIT License. It is intended for educational purposes, helping students format professional academic documents and master technical report writing standards.
