from state import AgentState
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
        
        # 1. Privacy Filter: Redact PII from query before sending to external LLM/Logs
        clean_query = redact_pii(last_message)
        if clean_query != last_message:
            print(f"Privacy Filter: Redacted PII from query. Original: {len(last_message)} chars, Clean: {len(clean_query)} chars.")
        
        # 2. Retrieval
        print(f"Querying knowledge base for: {clean_query}")
        retrieved_docs = query_knowledge_base(clean_query)
        context = "\n\n".join(retrieved_docs)
        
        # 3. Generate Answer
        response = mock_llm_rag_response(clean_query, context)
        
        # 4. Hallucination Check / Self-Correction
        # Ask the LLM if the answer is actually supported by the context
        llm = get_llm()
        check_template = """
        You are a Fact Checker. 
        Context: {context}
        Generated Answer: {response}
        
        Does the Generated Answer rely ONLY on the Context provided? 
        If yes, return "VERIFIED". 
        If no, return "UNVERIFIED: [Reason]".
        """
        prompt = ChatPromptTemplate.from_template(check_template)
        chain = prompt | llm | StrOutputParser()
        
        try:
            verification = chain.invoke({"context": context, "response": response})
            print(f"Hallucination Check: {verification}")
            
            if "UNVERIFIED" in verification:
                response += "\n\n(Note: This information might not be fully covered in our internal documentation. Please verify with a human agent.)"
                
        except Exception as e:
            print(f"Verification failed: {e}")
        
        return {
            "messages": [{"role": "assistant", "content": response}],
            "next_agent": "END"
        }
