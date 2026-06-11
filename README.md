# Local Note Assistant

Local Note Assistant is an experimental Obsidian assistant for querying, organizing, and gradually improving a personal Markdown knowledge vault.

The project started as a safe local search tool, and has grown into a chat-style Obsidian plugin with local-first retrieval, optional model APIs, draft writing, migration review tools, and a concept-card system that acts as the assistant's emerging knowledge structure.

Current version: `0.4.85`

## Project Goal

The goal is not to replace Obsidian or to make an AI write uncontrolled notes.

The goal is to build a local assistant that can:

- search a Markdown vault even when the user cannot remember exact wording;
- answer questions using note evidence and source links;
- help create and revise AI draft notes;
- review possible note migrations before applying them;
- learn a structured map of concepts from mathematical notes;
- preserve human control over every risky change.

The long-term direction is an agent that understands the user's note system well enough to choose tools, retrieve relevant evidence, propose safe edits, and explain why it is doing so.

## Current Features

### Chat-Style Note Search

The plugin provides a chat panel inside Obsidian.

It can search Markdown notes and return:

- relevant note paths;
- headings;
- snippets;
- source links;
- note-based answers.

The assistant supports different answer modes, including note-only and model-plus-note modes.

### Multi-Provider Model Support

The project was designed to support local and API-based models.

Supported configuration areas include:

- Ollama local models;
- OpenAI-compatible APIs;
- Qwen / DashScope-compatible settings;
- Gemini settings;
- custom API endpoints;
- vision model settings for screenshot or image-to-Markdown workflows.

API usage is optional. Local-only use remains possible.

### Knowledge Index

The knowledge index scans the vault and builds a local map of:

- note titles;
- headings;
- tags;
- links and backlinks;
- mathematical callouts;
- domains and folders;
- source snippets.

The current index is designed for mathematical Obsidian notes, especially notes that use callout blocks such as:

```markdown
> [!definition]
> ...

> [!proposition]
> ...

> [!theorem]
> ...
```

Proof blocks are treated as auxiliary evidence. They are useful as proof entrances, but they are not treated as primary concepts.

The index excludes generated AI folders such as `AI Drafts`, `AI Handoffs`, and `AI generated`.

### Concept Cards

Concept cards are the beginning of the assistant's "brain".

They are generated from definitions, propositions, theorems, examples, remarks, notation blocks, links, and backlinks. They are not meant to be blindly trusted. They are candidates that can be reviewed, accepted, rejected, renamed, and reorganized.

Current concept-card features include:

- review queues:
  - needs review;
  - ready to trust;
  - insufficient evidence;
  - changed;
  - confirmed;
  - rejected;
- editable display title;
- editable aliases and search words;
- editable parent topic;
- card notes;
- possible duplicate detection;
- technical-detail downranking;
- filtering of invalid cards such as `no heading`;
- safer proof entrances based on local evidence;
- persistence of user card edits across rebuilds.

In the latest vault experiment, the system generated `2322` concept cards from `535` searchable notes and separated them into review queues.

The next major design direction is to upgrade concept cards from a simple parent-topic model into a richer concept genealogy:

```json
{
  "title": "Density",
  "lineages": [
    {
      "axis": "Topological context",
      "path": ["Topology", "Topological space", "Closure", "Density"]
    },
    {
      "axis": "Approximation context",
      "path": ["Analysis", "Function space", "Approximation", "Density"]
    }
  ],
  "prerequisites": [
    {
      "target": "Closure",
      "kind": "definition",
      "strength": "hard"
    }
  ]
}
```

This is planned because mathematical concepts usually form overlapping lineages, not a single tree.

### Draft Writing

The assistant can create and work with AI draft notes.

Current draft features include:

- creating blank or generated draft files;
- appending selected assistant answers;
- rewriting answers into Markdown note style;
- asking the assistant to modify draft content;
- keeping draft operations separate from formal notes unless explicitly requested.

### Migration Review Tools

The plugin includes migration tools for careful note maintenance.

These are useful when a concept, symbol, or note link has changed.

The migration workflow emphasizes review before modification:

- scan affected notes;
- generate candidate replacements;
- show original text and proposed changes;
- allow the user to approve selected rows;
- apply only confirmed changes;
- keep undo information for recent migration operations.

The migration UI is separate from normal chat because note editing requires more care than ordinary Q&A.

### Agent Routing

The assistant includes a tool-routing layer.

Instead of only answering in chat, it can route user intent to tools such as:

- note search;
- topic organization;
- draft insertion;
- migration review;
- image-to-Markdown;
- concept-card review;
- GPT handoff.

There is also an AI pause option, so the user can temporarily stop model-driven actions and keep only local note search.

### Memory and Feedback

The plugin includes early memory features:

- conversation memory;
- returning to previous conversations;
- negative feedback tags for unsatisfactory answers;
- tool-use reliability checks.

This is intended to help the assistant avoid repeating known mistakes.

### ChatGPT Handoff

For users who have access to stronger ChatGPT models through a personal account, the plugin can generate compact Markdown prompt packages.

The idea is:

1. locally gather relevant note context;
2. create a concise prompt package;
3. paste it into ChatGPT;
4. import or use the result back in Obsidian.

This avoids requiring direct access to a personal ChatGPT account through the plugin.

## Safety Principles

This project is designed around safety and human review.

Important principles:

- existing Markdown notes should not be modified by indexing or concept-card generation;
- concept-card edits are stored as plugin metadata, not written into original notes;
- generated AI content is separated from source notes;
- migration tools require review before formal note edits;
- API usage is optional and should be clearly configured by the user;
- API keys, vault contents, and private plugin data should not be committed to GitHub.

Before publishing or sharing this project, check that the repository does not include:

- real API keys;
- private Obsidian notes;
- `.obsidian` plugin data from a personal vault;
- generated AI draft files unless intentionally shared;
- test reports containing sensitive note titles.

## Repository Layout

```text
local-note-assistant-stage3/
  main.js          Obsidian plugin logic
  styles.css       Plugin UI styles
  manifest.json    Obsidian plugin manifest

tools/
  *_eval.py        Regression checks
  *_experiment.py  Local experiments against a vault copy
  *_report.md      Generated test reports

README.md          Project overview
```

## Development and Testing

This project currently uses plain JavaScript for the Obsidian plugin.

Useful checks include:

```powershell
node --check local-note-assistant-stage3/main.js
python tools/concept_card_eval.py
python tools/concept_card_experiment.py
python tools/knowledge_index_eval.py
python tools/knowledge_citation_eval.py
```

The experiment scripts are designed for local vault testing and may need path adjustments before another collaborator runs them.

## Current Status

This is still an experimental local assistant, not a polished public plugin.

The strongest current parts are:

- local note retrieval;
- knowledge indexing;
- concept-card review;
- draft workflows;
- migration review;
- tool routing.

The main open direction is to make the concept-card system more like a real mathematical knowledge graph:

- multiple concept lineages;
- prerequisite relations;
- AI-generated card improvement proposals;
- split / merge proposals;
- card review center;
- retrieval that follows concept genealogy instead of only keyword similarity.

## Collaboration Notes

Good next contributions would be:

- improving concept-card proposal generation;
- designing the concept genealogy data model;
- improving UI for card review and graph navigation;
- adding safer tests for note migration;
- separating private local experiment paths from reusable project code;
- creating a clearer installation guide for non-technical Obsidian users.

The project should remain local-first, evidence-based, and review-oriented.

