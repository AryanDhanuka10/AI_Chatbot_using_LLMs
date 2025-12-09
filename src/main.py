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
from dotenv import load_dotenv
load_dotenv()



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

    def ask(self, query: str, selected_domain: str | None = None) -> str:
        route = self.router.route(query)

        predicted_domain = route["domain"]
        confidence = route["confidence"]
        reason = route["reason"]

        # 1. NORMALIZE STRINGS (Crucial Fix)
        # Convert to lowercase and strip spaces to ensure accurate comparison
        # e.g., "Medical" becomes "medical"
        pred_clean = predicted_domain.strip().lower()
        sel_clean = selected_domain.strip().lower() if selected_domain else None

        # Debugging: Print this to your console to see what's happening
        print(f"DEBUG: Router='{pred_clean}' ({confidence}), User='{sel_clean}'")

        final_domain = predicted_domain # Default fallback

        # ✅ CASE 1: User selected a domain AND router is confident
        if sel_clean and confidence >= 0.75:
            # Check if domains match using the CLEAN versions
            if pred_clean != sel_clean:
                # OPTIONAL: Allow "General" chit-chat in any domain?
                # If prompt is "hello" (General) but user is in "Medical", maybe don't force switch?
                # if pred_clean == "general": pass (Uncomment to allow this)
                
                return (
                    f"[domain=system confidence=1.0]\n"
                    f"❌ Wrong domain selected.\n\n"
                    f"✅ Please switch to **{predicted_domain.upper()}** for this question.\n\n"
                    f"Reason: {reason}"
                )

            # ✅ If router agrees → proceed normally
            final_domain = selected_domain

        # ✅ CASE 2: User selected a domain BUT router is UNCERTAIN
        elif sel_clean and confidence < 0.75:
            # Trust user input if the router isn't sure
            final_domain = selected_domain

        # ✅ CASE 3: No domain selected → auto route
        else:
            final_domain = predicted_domain

        # 2. RUN AGENT
        # Ensure your agents dictionary keys match the normalized or raw format you prefer
        # If keys are lowercase (e.g., 'medical'), use final_domain.lower()
        agent = self.agents.get(final_domain.lower(), self.agents["general"])

        context = self.context_manager.build_context()
        output = agent.run(query, context)

        self.context_manager.add_memory(query, output)

        return (
            f"[domain={final_domain} confidence={confidence:.2f}]\n"
            f"{output}"
        )