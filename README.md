\# Wumpus-Style Disaster Search \& Rescue Agent



A Python and Pygame-based simulation of a knowledge-based intelligent agent designed for disaster search and rescue.



The project is inspired by the classic \*\*Wumpus World\*\* problem and applies concepts from \*\*Artificial Intelligence and Intelligent Agents\*\*, including knowledge representation, logical inference, model-based reasoning, and goal-based decision making.



\## Project Overview



The system simulates a collapsed-building environment represented as a grid.



The rescue agent must:



1\. Explore the disaster environment.

2\. Detect hazards using sensor percepts.

3\. Use its Knowledge Base to reason about safe and potentially dangerous cells.

4\. Locate a survivor.

5\. Rescue the survivor.

6\. Navigate back to the exit safely.



The agent does not simply follow a predefined path. It maintains internal knowledge about the environment and uses that knowledge to make decisions.



\## AI Techniques



The main AI techniques used in this project are:



\- Knowledge-Based Agent

\- Knowledge Representation

\- Logical Inference

\- Model-Based Agent Architecture

\- Goal-Based Reasoning

\- Wumpus World-inspired reasoning

\- BFS/DFS-based navigation



\## System Architecture



```text

&#x20;            Disaster Environment

&#x20;                    │

&#x20;                    ▼

&#x20;                 Sensors

&#x20;                    │

&#x20;                    ▼

&#x20;                 Percepts

&#x20;                    │

&#x20;                    ▼

&#x20;             Knowledge Base

&#x20;                    │

&#x20;                    ▼

&#x20;            Logical Inference

&#x20;                    │

&#x20;                    ▼

&#x20;            Decision Engine

&#x20;                    │

&#x20;                    ▼

&#x20;             Goal-Based Agent

&#x20;                    │

&#x20;                    ▼

&#x20;                  Action

&#x20;                    │

&#x20;                    ▼

&#x20;             Environment Update

