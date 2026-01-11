# 📓 ELEC-392 Engineering Logbook System

> A hybrid documentation system combining markdown logbooks with GitHub Issues for comprehensive project tracking and reflection

## 🎯 Overview

This repository implements a **modern digital engineering logbook** specifically designed for ELEC-392 course projects. It replaces traditional paper logbooks with a structured, version-controlled system that makes documentation easier for students and grading simpler for TAs.

### Why This System?

- 📝 Document technical work and decisions
- 🧠 Reflect on learning and challenges
- 📊 Track time investment and progress
- 🎓 Demonstrate accountability in grading

This digital system **maintains all these benefits** while adding:
- ✅ Version control and automatic backups
- 🔍 Easy search and navigation
- 📈 Automated grading assistance
- 🖼️ Embedded images, equations, and code
- 🤝 Seamless team collaboration

---

## 🏗️ System Architecture

This logbook uses a **hybrid approach**:

### 1. 📂 Markdown Files (`/logbook`)
**Purpose**: Technical documentation and detailed work logs

- Daily/session-based entries in markdown format
- YAML frontmatter for metadata (date, hours, status)
- Support for LaTeX equations, code blocks, images
- Organized by week: `logbook/week-01/`, `logbook/week-02/`, etc.
- Example: `2025-01-08_circuit-design.md`

**Best for**: 
- Circuit designs and schematics
- Calculations and analysis
- Test results and measurements
- Technical diagrams and photos
- Implementation details

### 2. 🎫 GitHub Issues
**Purpose**: Reflections, learning outcomes, and grading submissions

- Weekly reflection issues using templates
- Track challenges, solutions, and learning
- Link to specific logbook entries
- Easy commenting and TA feedback
- Project Board integration for progress tracking

**Best for**:
- Weekly reflection summaries
- Learning outcomes and insights
- Challenge documentation
- Team discussions
- Grading submissions

### 3. 📊 Project Board
**Purpose**: Visual task management and progress tracking

- Columns: To Do, In Progress, Completed, Reflections, Status Reports
- Links issues and tasks together
- Provides overview of project status
- **Required columns for grading**: Reflections, Status Reports

### 4. 🖼️ Images (`/images`)

**Purpose**: Centralized storage for all project images and diagrams

- Circuit diagrams and schematics
- Oscilloscope screenshots
- PCB layouts and photos
- Test setup photos
- Data visualization plots
- Organized by week: `images/week-01/`, `images/week-02/`, etc.
- See [images/README.md](images/README.md) for naming conventions and optimization guidelines

**Best for**:

- Visual documentation of circuits and hardware
- Test results and measurements
- Progress photos
- Diagrams and flowcharts
- Any image referenced in logbook entries

### 5. 💻 Code (`/code`)

**Purpose**: Source code, scripts, and programs for your project

- Arduino/C++ sketches for microcontrollers
- Python scripts for data analysis
- MATLAB code for simulations
- Custom libraries and utilities
- Organized by week: `code/week-01/`, `code/week-02/`, etc.
- See [code/README.md](code/README.md) for organization guidelines and best practices

**Best for**:

- Microcontroller firmware and embedded code
- Data processing and analysis scripts
- Simulation and modeling code
- Testing and validation programs
- Any code referenced in logbook entries

---

## 🚀 Quick Start

### For Students

#### 1. Fork This Repository
1. Click the **Fork** button at the top right

2.    - Look for the "Fork" button in the top-right corner of this repository page
   - Click on it to open the fork creation dialog
   - **Important**: Select your personal GitHub account or your team's organization as the owner
   - Keep the repository name as-is or customize it (e.g., `elec-392-team-5-logbook`)
   - Ensure "Copy the main branch only" is checked
   - Click the green "Create fork" button
3. This creates your team's personal copy
4. Add team members as collaborators (Settings → Collaborators)
   - In your forked repository, click on the **Settings** tab (⚙️)
   - In the left sidebar, click on **Collaborators** (under "Access")
   - Click the green **"Add people"** button
   - Enter each team member's GitHub username or email
   - Select their account from the dropdown
   - Click **"Add [username] to this repository"**
   - They'll receive an email invitation - they must accept it to contribute
   - **Tip**: Make sure all team members have "Write" access so they can push changes

#### 2. Set Up Your Project Board
1. Go to **Projects** tab → **Create a project**
   - In your repository's top menu, click on **Projects**
   - Click the green **"New project"** button
   - Select **"Board"** as the template (recommended  for task tracking)
   - Name it: `ELEC-392 Logbook Board`
   - Click **"Create"**

2. Set up required columns:
   - Click **"+ Add column"** for each of these:
     - **"To Do"** (tasks planned but not started)
     - **"In Progress"** (currently working on)
     - **"Completed"** (finished work)
     - **"Reflections"** (for weekly reflection issues)
     - **"Status Reports"** (for TA grading checkpoints)
   - You can drag columns to reorder them

3. Link Issues to your Project Board:
   - Open any existing Issue
   - On the right sidebar, click **"Projects"**
   - Select your `ELEC-392 Logbook Board`
   - Choose the appropriate column (e.g., "To Do")

#### 3. Creating Daily Logbook Entries

**Option A: Using the Template (Recommended)**

1. Navigate to `logbook/.templates/` folder:
   - Click on the **"logbook"** folder in your repository
   - Click on **".templates"**
   - Click on **"daily-entry-template.md"**

2. Copy the template:
   - Click the **"Raw"** button at the top right of the file view
   - Press **Ctrl+A** (Windows/Linux) or **Cmd+A** (Mac) to select all, then **Ctrl+C** (Windows/Linux) or **Cmd+C** (Mac) to copy
3. Create your daily entry:
   - Navigate back to the appropriate week folder (e.g., `logbook/week-01/`)
   - Click **"Add file"** → **"Create new file"**
   - Name it using the format: `YYYY-MM-DD_brief-description.md`
     - Example: `2025-01-15_circuit-testing.md`
   - Paste the template content using **Ctrl+V** (Windows/Linux) or **Cmd+V** (Mac)   - Fill in all sections:
     - **Metadata** (date, hours worked, status)
     - **Work Description** (what you did)
     - **Challenges & Solutions**
     - **References** (any resources used)
   - Scroll down and click **"Commit new file"**

**Option B: Quick Entry Without Template**

1. In your week folder, click **"Add file"** → **"Create new file"**
2. Name: `YYYY-MM-DD_description.md`
3. Write your entry with these minimum sections:
```markdown
---
date: YYYY-MM-DD
hours: X.X
status: in-progress | completed
---

# Brief Description

## Work Done
- Detail what you accomplished

## Challenges
- Problems encountered and solutions
```
4. Commit the file

**++Tips++:**
- Make entries **daily** or after each work session
- Include **screenshots** using: `![Description](../images/filename.png)`
- Reference equations: $V = IR$ (inline) or $$V = IR$$ (block)
- Link related Issues: `Closes #5` or `Related to #3`

#### 4. Weekly Reflections (GitHub Issues)

1. Create a new Issue:
   - Go to the **"Issues"** tab in your repository
   - Click the green **"New issue"** button

2. Fill out the reflection:
   - **Title**: `Week [#] Reflection - [Date Range]`
     - Example: `Week 3 Reflection - Jan 15-21, 2025`
   - **Body**: Use this template:
```markdown
## Learning Outcomes
- What key concepts did you learn this week?
- Technical skills developed?

## Challenges Encountered
- Major obstacles faced
- How you solved them (or tried to)

## Progress Summary
- Link to your logbook entries for the week
- Completed tasks and achievements

## Questions/Help Needed
- Anything unclear?
- Areas where you need TA support?
```

3. Add labels:
   - Click **"Labels"** on the right sidebar
   - Select **"reflection"** (create it if it doesn't exist)
   - Add **"week-[#]"** label

4. Link to Project Board:
   - In the right sidebar, click **"Projects"**
   - Select your board
   - Place in **"Reflections"** column

5. Click **"Submit new issue"**

**++Important++**: TAs will review and comment on these weekly Issues for grading.

---

### For TAs

#### Grading Workflow

1. **Clone the student repository**:
```bash
git clone https://github.com/ELEC-392/[student-repo-name].git
cd [student-repo-name]
```

2. **Review the Project Board**:
   - Go to the **Projects** tab
   - Check the **"Reflections"** and **"Status Reports"** columns
   - Verify progress in **"Completed"** column

3. **Check weekly reflections** (Issues):
   - Go to **Issues** tab
   - Filter by label: `reflection`
   - Read each week's reflection
   - Leave feedback as comments
   - Apply grading labels: `grade-excellent`, `grade-good`, `grade-needs-improvement`

4. **Review logbook entries**:
   - Navigate to `logbook/week-[#]/` folders
   - Check for:
     - **Consistency** (regular entries)
     - **Detail level** (sufficient technical depth)
     - **Proper formatting** (markdown, equations, images)
     - **Metadata accuracy** (hours, dates)

5. **Run the grading script** (optional automation):
```bash
python scripts/generate_grading_report.py
```
   - This will analyze:
     - Total hours logged
     - Number of entries per week
     - Issue completion rate
   - Output: `grading_report.md` in the scripts folder

6. **Provide feedback**:
   - Comment on weekly reflection Issues
   - Suggest improvements
   - Highlight good practices

**++Grading Criteria++**:

_For TAs: See [Detailed Grading Rubric](#detailed-grading-rubric) below for comprehensive assessment criteria._
- **Reflections column**: Must have Reflections and Status Reports in correct columns
- **Regular entries**: At least 3-4 entries per week expected
- **Detail**: Someone else should be able to reproduce work from logbook
- **Professionalism**: Proper grammar, formatting, organization

---

### For Professors

#### Monitoring Class Progress

1. **Access all student repositories**:
   - Via GitHub Classroom dashboard
   - URL: `https://classroom.github.com/classrooms/[classroom-id]`

2. **Quick overview check**:
   - Click through student repos
   - Look at:
     - **Project Board** (are columns populated?)
     - **Recent commits** (activity level)
     - **Issues** (reflection quality)

3. **Export grading reports**:
   - Download or clone student repos
   - Run grading script on each:
```bash
for repo in */; do
  cd "$repo"
  python scripts/generate_grading_report.py
  cd ..
done
```

4. **Identify at-risk students**:
   - Look for:
     - Low commit frequency
     - Missing weekly reflections
     - Sparse logbook entries
   - Early intervention recommended

5. **Share best practices**:
   - Identify exemplary logbooks
   - Share anonymized examples with class
   - Highlight effective documentation techniques

**++Tips for instructors++**:
- Set clear expectations for entry frequency and detail
- Provide example entries in the template repository
- Consider mid-semester check-ins for logbook quality


## 📋 Repository Structure

```
.
├── README.md                          # This file - system overview
├── logbook/
│   ├── README.md                      # Logbook guidelines
│   ├── .templates/
│   │   └── daily-entry-template.md    # Template for daily entries
│   ├── week-01/
│   │   └── 2025-01-08_example-*.md    # Example entries
│   ├── week-02/
│   └── week-XX/
├── scripts/
│   └── generate_grading_report.py     # TA grading automation script
├── code/                              # Store source code here
│   └── README.md                      # Code organization guidelines
├── images/                            # Store images here
│   └── README.md                      # Image usage guidelines
└── .github/
    └── ISSUE_TEMPLATE/
        └── weekly-reflection.md       # Issue template for reflections
```

---

## 📝 Best Practices

### For Students

**✅ DO:**
- Log work **as you do it**, not after the fact
- Include measurements, calculations, and results
- Document failures and mistakes (very important!)
- Add images of circuits, oscilloscope readings, etc.
- Use clear, descriptive file names
- Fill out ALL YAML frontmatter fields
- Create weekly reflection issues
- Commit and push regularly

**❌ DON'T:**
- Write entries retroactively days later
- Skip documenting "boring" or failed attempts
- Forget to add hours worked
- Use vague titles like "work.md" or "test.md"
- Let technical jargon replace clear explanations
- Plagiarize or fabricate entries

### For TAs

#### Detailed Grading Rubric:
This rubric provides TAs with clear criteria for assessing student logbooks across four dimensions. Each criterion is evaluated on a 5-point scale (4 = Excellent, 3 = Proficient, 2 = Satisfactory, 1 = Needs Improvement, 0 = Unsatisfactory).

#### 1. Entry Frequency & Consistency (30%)

**Excellent (4):** Demonstrates consistent, regular entries (3+ per week) throughout the entire project period. Entries are made in real-time or within 24 hours of work sessions. Clear timestamps and commit history show authentic, ongoing documentation. No evidence of batch entries or retroactive documentation.

**Proficient (3):** Shows regular entries (2-3 per week) for most of the project period. Most entries appear to be made shortly after work sessions. Minor instances of delayed documentation. Commit history generally supports real-time logging.

**Satisfactory (2):** Provides basic entry frequency (1-2 per week) but with some gaps. Some evidence of batch entries or delayed documentation. Commit history shows irregular patterns with occasional clustering of entries.

**Needs Improvement (1):** Limited entries with significant gaps in documentation. Clear evidence of retroactive or batch-written entries. Commit history shows infrequent, clustered activity suggesting documentation done all at once.

**Unsatisfactory (0):** Minimal or no entries. Entries appear fabricated or entirely retroactive. No meaningful commit history or documentation pattern.

---

#### 2. Technical Depth & Documentation Quality (40%)

**Excellent (4):** Provides comprehensive technical documentation including detailed calculations, measurements, circuit diagrams, code snippets, and analysis. All YAML frontmatter fields are complete and accurate. Documentation is sufficient for another engineer to reproduce the work. Includes quantitative data, error analysis, and troubleshooting steps. Images are clear, properly captioned, and directly support the technical content.

**Proficient (3):** Includes good technical documentation with most calculations, measurements, and relevant details. YAML fields are mostly complete with minor omissions. Work can generally be understood and reproduced. Images and diagrams support the documentation. Some minor gaps in detail or analysis.

**Satisfactory (2):** Provides basic technical information but lacks depth in some areas. Calculations or measurements present but incomplete. YAML fields partially filled. Work is documented but may require clarification to reproduce. Images present but may lack proper captioning or context.

**Needs Improvement (1):** Limited technical detail. Sparse or missing calculations, measurements, or analysis. YAML fields mostly incomplete. Documentation too vague to understand or reproduce work. Few or no images, or images without proper context.

**Unsatisfactory (0):** Little to no technical content. Missing critical information. YAML fields blank or incorrect. Documentation insufficient to understand what was done.

---

#### 3. Reflection Quality & Learning Insights (20%)

**Excellent (4):** Demonstrates deep reflection on learning through thoughtful weekly Issues. Clearly articulates what was learned, challenges encountered, and problem-solving approaches. Documents failures and mistakes with analysis of why they occurred and what was learned. Shows evidence of critical thinking about design decisions and trade-offs. Connects experiences to broader engineering concepts.

**Proficient (3):** Provides good reflection in weekly Issues. Discusses learning outcomes and challenges with reasonable depth. Documents some failures and problem-solving approaches. Shows understanding of design decisions. Makes some connections to engineering principles.

**Satisfactory (2):** Includes basic reflection but lacks depth. Weekly Issues present but somewhat superficial. Mentions challenges but limited analysis of solutions or learning. Some documentation of failures but minimal interpretation. Limited connection to broader concepts.

**Needs Improvement (1):** Minimal reflection. Weekly Issues are brief or superficial. Little discussion of challenges or learning. Avoids documenting failures. No evidence of critical thinking about design decisions.

**Unsatisfactory (0):** No meaningful reflection. Missing or trivial weekly Issues. No evidence of learning or critical analysis.

---

#### 4. Completeness & Professional Standards (10%)

**Excellent (4):** All YAML frontmatter fields consistently filled with accurate information (date, hours, status, tags). File naming follows convention perfectly (`YYYY-MM-DD_descriptive-topic.md`). Markdown formatting is clean and professional. Images properly referenced with relative paths. Weekly reflection Issues created and linked to Project Board. Regular commits with meaningful commit messages. Repository structure follows template exactly.

**Proficient (3):** Most YAML fields complete and accurate with minor omissions. File naming mostly follows convention. Good markdown formatting with occasional inconsistencies. Images generally well-referenced. Most weekly Issues created. Regular commits with decent messages.

**Satisfactory (2):** Basic YAML fields filled but some missing or inaccurate. File naming partially follows convention. Markdown formatting functional but inconsistent. Some images missing references. Some weekly Issues missing. Irregular commits or vague commit messages.

**Needs Improvement (1):** Many YAML fields missing or incorrect. File naming inconsistent or incorrect. Poor markdown formatting. Images improperly referenced or missing. Many weekly Issues missing. Minimal or poor commit practices.

**Unsatisfactory (0):** YAML fields mostly blank. File naming chaotic. Markdown formatting broken. No proper image handling. No weekly Issues. No meaningful version control usage.

---

**Grade Calculation:** Each criterion is scored 0-4 and multiplied by its weight (Frequency: 30%, Technical Depth: 40%, Reflection: 20%, Completeness: 10%). Final grade is the weighted sum converted to percentage.
---

## 🛠️ Technical Features

### Markdown Capabilities

**LaTeX Equations:**
```markdown
Inline: $V = IR$
Block: $$P = \frac{V^2}{R}$$
```

**Code Blocks:**
```python
# Your embedded code here
def calculate_power(voltage, resistance):
    return (voltage ** 2) / resistance
```

**Images:**
```markdown
![Circuit Diagram](../images/week-01/circuit.png)
```

**Tables:**
```markdown
| Voltage | Current | Power |
|---------|---------|-------|
| 5V      | 100mA   | 0.5W  |
```

### Automation Scripts

**Grading Report Generator** (`scripts/generate_grading_report.py`):
- Scans all logbook entries
- Validates YAML frontmatter
- Calculates statistics (entries, hours, weeks)
- Checks for images and calculations
- Generates markdown report with grading suggestions

---



**Q: Can we write logbook entries as a team?**
A: Each team member should document their individual contributions. Use the `author` field in YAML frontmatter.

**Q: What if we forget to log something?**
A: Add it ASAP with a note explaining the delay. Don't fabricate timestamps.

**Q: How often should we create entries?**
A: Aim for **every work session**. Minimum 2-3 entries per week per person.

**Q: Can we edit old entries?**
A: Minor corrections are OK (typos, formatting). Major changes should be noted. Git tracks all edits anyway.

**Q: What about failed experiments?**
A: **Document them!** Failures are valuable learning experiences. Explain what went wrong and why.

**Q: How much detail is enough?**
A: Someone else should be able to reproduce your work from your logbook. Include all relevant numbers, equations, and decisions.

---

## 📚 Additional Resources

- [ELEC-392 Course GitBook](https://elec392.gitbook.io/elec-392) - Official course documentation and guidelines

- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Issues Documentation](https://docs.github.com/en/issues)
- [LaTeX Math Symbols](https://www.overleaf.com/learn/latex/List_of_Greek_letters_and_math_symbols)
- [Engineering Logbook Best Practices](https://engineergirl.org/125/engineering-notebook)

---

## 🆘 Getting Help

- **Technical Issues**: Open an Issue in this repository
- **Grading Questions**: Contact your TA
- **GitHub Problems**: Check [GitHub Docs](https://docs.github.com/) or ask in class

---

## 📄 License & Academic Integrity

This template is provided for ELEC-392 course use. 

**Academic Integrity Notice**: Your logbook is an individual/team assessment component. Do not share detailed technical solutions with other teams. Plagiarism will result in academic penalties.

---

**Happy Logging! 🚀**

*Remember: Your logbook is not just for grades—it's a professional skill that will serve you throughout your engineering career.*