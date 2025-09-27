"""Base agent class for all specialized agents."""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import openai
from config import OPENAI_API_KEY, AGENT_CONFIGS

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all customer service agents."""
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.config = AGENT_CONFIGS.get(agent_type, AGENT_CONFIGS["orchestrator"])
        
        if OPENAI_API_KEY:
            self.client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
        else:
            logger.warning(f"OpenAI API key not configured - {agent_type} agent will use mock responses")
            self.client = None
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent."""
        pass
    
    @abstractmethod
    async def process_request(self, user_message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a user request and return response."""
        pass
    
    async def generate_response(self, user_message: str, context: Dict[str, Any], 
                             tools_used: List[str] = None) -> Dict[str, Any]:
        """Generate AI response using OpenAI API."""
        if not self.client:
            return await self._generate_mock_response(user_message, context)
        
        try:
            # Prepare conversation history
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "user", "content": self._format_user_message(user_message, context)}
            ]
            
            # Add recent conversation history if available
            if context.get("recent_conversation"):
                for msg in context["recent_conversation"][-3:]:  # Last 3 messages
                    messages.insert(-1, {
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Generate response
            response = await self.client.chat.completions.create(
                model=self.config["model"],
                messages=messages,
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"]
            )
            
            agent_response = response.choices[0].message.content
            
            return {
                "response": agent_response,
                "agent_type": self.agent_type,
                "tools_used": tools_used or [],
                "confidence": self._estimate_confidence(agent_response),
                "thinking_process": f"Analyzed request using {self.agent_type} expertise and provided specialized response"
            }
            
        except Exception as e:
            logger.error(f"Error generating response for {self.agent_type}: {e}")
            return await self._generate_mock_response(user_message, context)
    
    def _format_user_message(self, user_message: str, context: Dict[str, Any]) -> str:
        """Format user message with context for the AI."""
        formatted_message = f"Customer Message: {user_message}\n\n"
        
        # Add relevant context
        if context.get("customer_context"):
            formatted_message += f"Customer Context: {context['customer_context']}\n\n"
        
        if context.get("orders_discussed"):
            formatted_message += f"Orders Previously Discussed: {', '.join(context['orders_discussed'])}\n\n"
        
        if context.get("issues_mentioned"):
            formatted_message += f"Issues Previously Mentioned: {', '.join(context['issues_mentioned'])}\n\n"
        
        return formatted_message
    
    def _estimate_confidence(self, response: str) -> float:
        """Estimate confidence level based on response characteristics."""
        # Simple heuristic - longer, more detailed responses tend to be more confident
        if len(response) > 200 and ("specific" in response.lower() or "recommend" in response.lower()):
            return 0.9
        elif len(response) > 100:
            return 0.7
        else:
            return 0.5
    
    async def _generate_mock_response(self, user_message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock response when OpenAI API is not available."""
        mock_responses = {
            "order": "I've located your order information and can help with any questions about status, tracking, or modifications.",
            "tech_support": "I can help troubleshoot your technical issue. Let me provide some steps to resolve this problem.",
            "product": "I can provide detailed product information and help you compare different options to find the best fit.",
            "solutions": "I understand you need assistance with a return or exchange. Let me help you with the best solution for your situation."
        }
        
        return {
            "response": mock_responses.get(self.agent_type, "I'm here to help with your request."),
            "agent_type": self.agent_type,
            "tools_used": [],
            "confidence": 0.6,
            "thinking_process": f"Generated mock response using {self.agent_type} agent (API not configured)"
        }
    
    def format_final_response(self, agent_response: Dict[str, Any], 
                            tool_results: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format the final response with tool results."""
        return {
            "response": agent_response["response"],
            "agent_used": self.agent_type,
            "tools_used": agent_response.get("tools_used", []),
            "tool_results": tool_results or [],
            "confidence": agent_response.get("confidence", 0.5),
            "thinking_process": agent_response.get("thinking_process", "")
        }