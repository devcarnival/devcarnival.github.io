---
title: "Nullable Is Not a User Word: What Building Fast Still Misses"
slug: "nullable-is-not-a-user-word-what-building-fast-still-misses"
speakers:
  - "janani-prasad"
communities:
  - "azure-developer-community-tamilnadu"
years: ["2027"]
track: "AI & Future of Software"
session_type: "Talk"
duration: "45 mins"
---

With generative AI and modern development assistants, shipping software has never been faster. A feature that once took two weeks can now be drafted in an afternoon, and unit test suites can be generated in minutes. Yet working code is not the same as a viable product.

This talk confronts the critical UX, domain, and data integrity gaps that pass every automated test suite and still reach paying users in production. Drawing on live case studies from AI document intelligence and enterprise procurement systems, we examine subtle failure modes—such as an LLM that hallucinated a non-existent corporate approver simply because the prompt contract never taught it how to declare "not found".

Attendees will explore why high-velocity AI generation frequently overlooks domain boundary nuances, how to design cognitive safety nets for human users, and practical strategies to surface product defects before end users encounter them.

### Key Takeaways
- **The Speed vs. Product Gap:** Understand why passing unit tests fails to protect products against cognitive and semantic errors.
- **Handling the Absence of Truth:** Architect AI workflows and UX patterns that gracefully handle missing, incomplete, or ambiguous inputs.
- **Domain Edge Cases in AI:** Identify blind spots in automated test generation where LLMs hallucinate plausible but catastrophic defaults.
- **Pragmatic Quality Gates:** Implement human-in-the-loop and verification heuristics that preserve developer velocity while protecting product trust.

### Target Audience
- Product managers, engineering leads, software designers, and full-stack developers navigating the challenges of AI-assisted software delivery.

### Prerequisites
- General familiarity with software development lifecycles and product development processes.
