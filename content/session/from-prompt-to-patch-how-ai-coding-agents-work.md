---
title: "From Prompt to Patch: How AI Coding Agents Actually Work"
slug: "from-prompt-to-patch-how-ai-coding-agents-work"
speakers:
  - "manukumar-vs"
communities:
  - "tamilnadu-java-user-group"
years: ["2026"]
track: "AI Agents & Developer Productivity"
session_type: "Talk"
duration: "45 mins"
---

What happens between asking an AI coding agent to change a project and receiving a patch? This talk follows a representative agent workflow: gathering context, choosing tools, observing results, and deciding when to stop. We make those steps visible so developers can reason about the work behind the reassuring "done" message.

Using a small, deliberately constructed Java ownership example, we examine how apparently correct values can hide shared mutable state, why an explicit requirement matters, and what an engineer should inspect before accepting a change. The walkthrough supports a practical explanation of agent-assisted development; contrasting autonomous agents with simple autocomplete and highlighting the importance of verification loops.

Attendees will learn how agents explore codebases, why explicit constraints and observable completion checks are essential, and how engineers can effectively audit machine-generated patches.

### Key Takeaways

- **Beyond Autocomplete**: Understand the structural differences between predictive inline autocomplete and autonomous coding agents that gather context, invoke tools, and iterate on feedback.
- **Inside the Agent Workflow**: Demystify the multi-step loop behind an agent prompt—discovering repository context, selecting tools, running commands, and deciding termination conditions.
- **Auditing Patches & State Invariants**: Learn what to inspect before accepting an agent's patch using a practical Java ownership example, exposing how subtle bugs like shared mutable state escape superficial review.
- **Grounding Agents with Verification**: Learn how to supply explicit constraints, define observable completion checks, and establish reliable test harnesses to ensure code correctness.

### Target Audience

- Software developers, backend engineers, and architects curious about how AI coding agents work under the hood.
- Java practitioners and engineering teams looking to incorporate AI coding agents reliably into their software engineering workflows.
- Developers of all experience levels seeking practical frameworks to evaluate, prompt, and inspect AI-generated pull requests and patches.

### Prerequisites

- Basic understanding of programming concepts and general familiarity with Java or modern backend languages.
- No prior experience with AI coding agents or machine learning is required.
