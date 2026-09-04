---
title: "Agentic Patterns with Spring AI"
speakers:
  - "udayani"
years: ["2026"]
track: "AI Agents & Developer Productivity"
session_type: "Talk"
duration: "60 mins"
---

Spring AI makes it straightforward to integrate LLMs into Java applications. But what happens when you need more than a simple chatbot? Building real-world AI applications introduces universal engineering challenges: managing skyrocketing token budgets, preventing models from skipping steps in complex tasks, and orchestrating complex workflows.

Agentic patterns are the architectural solutions to these problems. If you are using Spring AI, it provides out-of-the-box implementations for these patterns, allowing you to easily invoke and apply them in your applications.

In this talk, we’ll go beyond the basics and explore how to apply the patterns that turn a simple chat application into an intelligent agent:

- **Dynamic Tool Discovery & Prompt Caching**: Achieve massive token savings by lazy-loading context and caching redundant prompts
- **Tool Argument Augmentation**: Build explainable agents by capturing the model's inner reasoning during tool execution
- **Agent Skills**: Provide on-demand domain expertise without bloating the context window
- **AskUserQuestion**: Allow agents to interactively gather requirements instead of hallucinating assumptions
- **TodoWrite**: Make planning explicit to prevent agents from dropping steps in complex tasks
- **Subagent Orchestration & A2A**: Coordinate workflows using multi-model routing locally, and the Agent2Agent protocol for cross-application collaboration

Each pattern is introduced through the real-world problem it solves, backed by practical code examples. Whether you're optimizing costs, improving reliability, or building multi-agent systems, you'll walk away with a concrete toolkit you can start using immediately—all LLM-portable, all in Spring.

### Key Takeaways
- **Cost Optimization**: Discover techniques like Dynamic Tool Discovery and Prompt Caching to drastically reduce token usage and API costs.
- **Smarter Reasoning & Adaptation**: Learn how to prevent the "lost in the middle" problem using explicit planning patterns (TodoWrite) and modular domain knowledge (Agent Skills).
- **Better Interaction & Understanding**: Prevent blind assumptions and build explainable AI using human-in-the-loop clarifications (AskUserQuestion) and Tool Argument Augmentation.
- **Orchestration**: Understand how to architect multi-agent systems by delegating tasks to specialized subagents and giving them modular domain expertise.

### Target Audience
- Java/Backend Developers and Software Engineers looking to integrate LLMs into enterprise applications.
- Software Architects designing scalable, production-ready, and cost-efficient AI systems.
- Spring Boot practitioners who want to move beyond basic chatbots into complex, multi-agent workflows.

### Prerequisites
- Basic proficiency in Java and the Spring Boot ecosystem.
- A high-level understanding of basic generative AI concepts.
- No prior experience with Spring AI is strictly required, but having a basic understanding of Spring AI is recommended.
