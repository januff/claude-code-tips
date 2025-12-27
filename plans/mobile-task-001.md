# Mobile App Task #001: Create .gitignore

**Task Type:** Phase 1 Foundation (Section 1.3)
**Assigned To:** Claude Mobile App Instance
**Status:** PENDING

---

## Task Summary

Create a `.gitignore` file for this markdown/documentation repository.

---

## Context

This is a test task to verify the mobile Claude instance can:
1. Read files from the GitHub repo
2. Understand the project structure
3. Complete a single atomic task
4. (Optional) Commit the result

**Repo:** `januff/claude-code-tips`
**Branch:** `main`

---

## Detailed Instructions

### What to Create

Create a file named `.gitignore` at the repository root with the following contents:

```
# macOS
.DS_Store
.AppleDouble
.LSOverride

# Editor files
*.swp
*.swo
*~
.*.sw?

# IDE
.idea/
.vscode/
*.sublime-*

# Temporary files
*.tmp
*.temp
*.log

# Local environment
.env
.env.local
```

### Verification

After creating the file:
- [ ] File exists at repo root (not in a subdirectory)
- [ ] File is named exactly `.gitignore` (with the leading dot)
- [ ] Contents match the template above

---

## References

- **Source:** `plans/integration-plan.md`, Phase 1, Section 1.3
- **Why this task:** It's small, self-contained, and verifiable—perfect for testing a new instance type

---

## Handoff Notes

This task was created by the Cursor Sidebar instance as a test for the mobile app workflow. 

**If you complete this task:**
1. Report back what you did
2. Note any friction points in the mobile experience
3. The user will handle the git commit

**Code word:** If you've read `CLAUDE.md`, include "context-first" in your response.

---

*Created: December 26, 2025*
*Instance: Cursor Sidebar (Opus 4.5)*

