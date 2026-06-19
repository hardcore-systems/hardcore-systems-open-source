# FDE Compiler Self-Healing / Docstring Backpropagation

This module demonstrates how to use compiler feedback and execution errors to automatically tune tool descriptions (docstrings) for LLMs.

In agentic workflows, the prompt/docstring is the LLM's only understanding of the tool's interface. If the tool interface is strict and the docstring is vague, the agent will fail. 

By capturing exception tracebacks and passing them back to a "compiler LLM" to rewrite the docstrings, we create a closed-loop system where the docstrings automatically adapt to match the exact tool constraints.
