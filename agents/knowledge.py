from state import AgentState, AuditLogger
from utils.llm import mock_llm_rag_response, get_llm
from utils.rag import query_knowledge_base, redact_pii
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class KnowledgeAgent:
    def __init__(self):
        pass

    def run(self, state: AgentState):
        print("--- Knowledge Agent ---")
        messages = state['messages']
        last_message = messages[-1]['content']
        
        # 1. Privacy Filter: Redact PII
        clean_query = redact_pii(last_message)
        if clean_query != last_message:
            print(f"Privacy Filter: Redacted PII from query.")
        
        # 2. Check for conversation context (multi-turn)
        conversation_summary = state.get("conversation_summary", "")
        if conversation_summary:
            clean_query = f"Context: {conversation_summary}\n\nNew Question: {clean_query}"
        
        # 3. Retrieval
        print(f"Querying knowledge base for: {clean_query[:50]}...")
        retrieved_docs = query_knowledge_base(clean_query)
        context = "\n\n".join(retrieved_docs)
        
        # Calculate retrieval confidence based on document relevance
        retrieval_confidence = min(len(retrieved_docs) / 3, 1.0)  # Max 3 docs = 100%
        
        # 4. Generate Answer
        response = mock_llm_rag_response(clean_query, context)
        
        # 5. Hallucination Check & Confidence Calculation
        llm = get_llm()
        check_template = """
        You are a Fact Checker analyzing an IT support response.
        
        Context (from knowledge base):
        {context}
        
        Generated Answer:
        {response}
        
        Evaluate:
        1. Is the answer fully supported by the context? (VERIFIED/UNVERIFIED)
        2. Confidence score (0.0-1.0)
        3. Brief reason
        
        Format: VERIFIED|0.85|Answer directly from policy docs
        or: UNVERIFIED|0.3|Answer includes speculation
        """
        prompt = ChatPromptTemplate.from_template(check_template)
        chain = prompt | llm | StrOutputParser()
        
        confidence = 0.5
        confidence_reason = "Default confidence"
        verified = True
        
        try:
            verification = chain.invoke({"context": context, "response": response})
            print(f"Verification: {verification}")
            
            # Parse response
            parts = verification.strip().split("|")
            if len(parts) >= 3:
                verified = "VERIFIED" in parts[0].upper()
                try:
                    confidence = float(parts[1])
                except:
                    confidence = 0.5
                confidence_reason = parts[2] if len(parts) > 2 else "Verified by LLM"
            
            if not verified:
                response += "\n\n⚠️ *Note: This information may not be fully covered in our documentation. Please verify with IT support.*"
                confidence = min(confidence, 0.5)
                
        except Exception as e:
            print(f"Verification failed: {e}")
            confidence = 0.4
            confidence_reason = "Verification unavailable"
        
        # Combine retrieval and verification confidence
        final_confidence = (retrieval_confidence * 0.4) + (confidence * 0.6)
        
        # Add confidence indicator to response
        confidence_emoji = "🟢" if final_confidence > 0.7 else "🟡" if final_confidence > 0.4 else "🔴"
        response += f"\n\n{confidence_emoji} *Confidence: {final_confidence:.0%}*"
        
        # Log the action
        audit_log = AuditLogger.log(state, "KnowledgeAgent", "rag_query", {
            "query": clean_query[:100],
            "docs_retrieved": len(retrieved_docs),
            "confidence": final_confidence
        })
        
        return {
            "messages": [{"role": "assistant", "content": response}],
            "next_agent": "END",
            "confidence": final_confidence,
            "confidence_reason": confidence_reason,
            "audit_log": audit_log
        }
