# 🤝 Contributing to Bug Bounty Mastery

Thank you for your interest in contributing! This project aims to be the most comprehensive, high-quality free bug bounty resource on GitHub. Every contribution helps the community.

---

## 📋 How to Contribute

### Types of Contributions Welcome

- 📝 **Content additions** — new techniques, tools, or examples
- 🐛 **Bug fixes** — correcting errors in existing content
- 🔗 **Resource additions** — new labs, tools, or references
- 🌍 **Translations** — make content accessible in other languages
- ✅ **Lab exercises** — practical exercises for any module
- 💡 **Real-world examples** — anonymized bug bounty stories

### Content Standards

All contributions must:

1. **Be accurate** — technically correct and up-to-date
2. **Be ethical** — focus on defensive knowledge and legal testing
3. **Be original** — your own work or properly attributed
4. **Match the style** — consistent with existing module format
5. **Include examples** — code blocks, payloads, or commands where relevant

---

## 🚀 Getting Started

### Fork and Clone

```bash
# Fork via GitHub UI first, then:
git clone https://github.com/YOUR_USERNAME/Bug-Bounty-Mastery.git
cd Bug-Bounty-Mastery
```

### Create a Branch

```bash
# Use a descriptive branch name
git checkout -b feature/add-ssrf-techniques
git checkout -b fix/module-05-typo
git checkout -b content/module-16-new-script
```

### Make Your Changes

Follow the module format:
```markdown
## Overview
## Why It Matters
## Real-World Example
## Step-by-Step Methodology
## Tools Used
## Payload Examples (code blocks)
## Prevention
## Practice Labs
```

### Submit a Pull Request

```bash
git add .
git commit -m "Add: SSRF bypass techniques to Module 14"
git push origin feature/add-ssrf-techniques
```

Then open a Pull Request on GitHub with:
- Clear title
- Description of what you added/changed
- Why it's valuable

---

## 📏 Style Guide

### Markdown Conventions

- Use `##` for main sections, `###` for subsections
- Use emoji at the start of headers (matching existing style)
- Code blocks with language specification: ` ```bash `, ` ```python `, etc.
- Tables for comparisons and tool lists
- Bold (`**text**`) for important terms
- Navigation links at bottom of each module

### Code Examples

- Include comments explaining what each line does
- Use realistic but fictional target URLs (`target.com`, `example.com`)
- Never use real vulnerable sites as examples
- Include both the attack and the defense where applicable

### Ethical Guidelines

- Only include techniques for **legal** security testing
- Always note that techniques should only be used with **permission**
- Include prevention/remediation for every attack technique
- Do not include actual malware, working exploits for unpatched systems, or content that could cause real harm

---

## 🚫 What We Don't Accept

- Content promoting illegal hacking
- Working exploits for actively vulnerable systems
- Plagiarized content from other courses or books
- Unverified or inaccurate technical information
- Spam or self-promotional content

---

## 📝 Pull Request Template

```
## What does this PR do?
[Brief description]

## Module affected
[e.g., Module 07 - Cross-Site Scripting]

## Type of change
- [ ] New content
- [ ] Bug fix
- [ ] Enhancement
- [ ] Translation

## Checklist
- [ ] Content is technically accurate
- [ ] Follows the module format
- [ ] Includes code examples where relevant
- [ ] Includes prevention/remediation (for attack content)
- [ ] Tested/verified the content
```

---

## 🏆 Recognition

All contributors will be:
- Listed in the Contributors section
- Credited in the specific modules they improve
- Part of building the community's best free bug bounty resource

---

## ❓ Questions?

Open an [Issue](https://github.com/vibhor-777/Bug-Bounty-Mastery/issues) with the `question` label.

---

<div align="center">

**Thank you for helping make security education accessible to everyone! 🙏**

</div>
