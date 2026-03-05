# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OwnAI is an AI Agent framework built on Python, based on the OpenClaw concept. The project aims to reduce context consumption and token usage by leveraging RAG (Retrieval Augmented Generation) for tool discovery and agent capabilities.

## Development Environment

This project uses Python with a virtual environment.

```bash
# Activate the virtual environment (Windows)
venv\Scripts\activate

# Activate the virtual environment (Unix/Mac)
source venv/bin/activate

# Run the main entry point
python main.py
```

## Project Structure

```files
OwnAI/
├── main.py              # Main entry point
├── src/                 # Source code modules
│   ├── agent/          # Agent framework code
│   ├── logger/         # Logging utilities
│   ├── message/        # Agent communication system
│   └── rag/            # RAG/vector database integration
├── agents/             # Agent definitions (system and sub-agents)
├── tools/              # External skill tools
├── system/             # Built-in system tools
├── data/               # Runtime data (gitignored)
├── qdrant_store/       # RAG vector storage via Qdrant (gitignored)
└── logs/               # Application logs
```

## Key Architecture Concepts

### Tool Categories

1. **System Tools** - Built-in tools with permission management:
   - File operations (read, write, create, delete) with blacklist protection for internal folders
   - Bash terminal execution with command blacklist
   - Sub-agent creation/deletion with context isolation
   - Browser integration for web search
   - Inter-agent communication
   - RAG queries for skill discovery
   - Permission requests for external folder access

2. **Skill Tools** - External tools not included in default prompts:
   - Each skill has documentation + Python implementation
   - Discovered via RAG queries when needed
   - Registered per-agent but not auto-sent in context

### Agent Types

- **system-Agent**: Built-in agents with predefined roles
- **sub-Agent**: Dynamically created agents with isolated contexts

### Core Systems

- **RAG System**: Uses Qdrant for vector storage of skills, agent capabilities, and long-term memory
- **Message System**: Feishu-like inbox/outbox for agent communication with `history_*.md` persistence
- **Permission Management**: External folder access requires user approval with persistent records
- **Status Markdown**: Task tracking managed only by specific agents (Task Review Agent, Task List Creation Agent)

## Important Notes

- The `.env` file is gitignored - store API keys and secrets there
- Runtime data in `data/` and `qdrant_store/` is not version controlled
- Development documentation in Chinese is in `dev_doc/` (gitignored)
- Primary development documentation: [Agent开发文档.md](Agent开发文档.md)
