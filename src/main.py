"""Module: main

High-level controller: routing, agents, context, and RAG integration.
"""

from __future__ import annotations

from src.agents.coding_agent import CodingAgent
from src.agents.education_agent import EducationAgent
from src.agents.general_agent import GeneralAgent
from src.agents.legal_agent import LegalAgent
from src.agents.medical_agent import MedicalAgent
from src.rag.rag_pipeline import RAGPipeline
from src.router.domain_router import DomainRouter
from src.utils.context_manager import ContextManager


class MultiDomainAssistant:
    def __init__(self) -> None:
        self.context_manager = ContextManager()
        self.router = DomainRouter()
        self.rag = RAGPipeline()  # single shared RAG pipeline

        # create agents
        self.agents = {
            "education": EducationAgent(),
            "coding": CodingAgent(),
            "medical": MedicalAgent(),
            "legal": LegalAgent(),
            "general": GeneralAgent(),
        }

        # Attach RAG to selected agents only (change list as desired)
        rag_enabled = {"education", "medical", "legal"}
        for name, agent in self.agents.items():
            if name in rag_enabled:
                agent.enable_rag(self.rag)

    def ask(self, query: str) -> str:
        routing = self.router.route(query)
        domain = routing.get("domain", "general")
        confidence = float(routing.get("confidence", 0.0))
        reason = routing.get("reason", "")

        agent = self.agents.get(domain, self.agents["general"])

        context = {
            "memory": self.context_manager.memory,
            "domain": domain,
            "router_confidence": confidence,
        }

        response_text = agent.run(query, context)

        # store memory (safe format)
        self.context_manager.add_memory(query, response_text)

        # return metadata header + response
        return (
            f"[domain={domain} confidence={confidence:.2f}]\n"
            f"{response_text}\n"
            f"Router reason: {reason}"
        )
