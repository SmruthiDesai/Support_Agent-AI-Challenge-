"""Order specialist agent for handling order-related queries."""

import logging
from typing import Dict, Any, List

from agents.base_agent import BaseAgent
from tools.order_tools import order_tools

logger = logging.getLogger(__name__)


class OrderAgent(BaseAgent):
    """Specialized agent for order management and tracking."""

    def __init__(self):
        # agent_type = "order"
        super().__init__("order")

    def get_system_prompt(self) -> str:
        """Get the system prompt for the order agent (still used for logs / future LLM use)."""
        return """
        You are an Order Management Specialist for a customer service team. Your expertise includes:
        
        - Order lookup and status tracking
        - Delivery and shipping information
        - Order modifications and cancellations
        - Return and exchange processes
        - Warranty status and coverage
        - Billing and payment issues
        
        Guidelines:
        - Always verify order information before making changes
        - Provide accurate delivery estimates and tracking information
        - Explain return and warranty policies clearly
        - Offer alternatives when modifications aren't possible
        - Be empathetic about order issues and delays
        - Escalate complex billing issues to appropriate teams
        
        Use the available tools to retrieve accurate order information and provide helpful solutions.
        Keep responses concise but comprehensive, focusing on resolving the customer's specific order concerns.
        """

    async def process_request(self, user_message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process order-related requests.

        IMPORTANT:
        This version does NOT call an external LLM (OpenAI).
        It builds the response directly from local mock data via order_tools.
        """
        try:
            # Extract order ID from message or context
            order_id = self._extract_order_id(user_message, context)

            tool_results: List[Dict[str, Any]] = []
            tools_used: List[str] = []

            order_info: Dict[str, Any] | None = None
            tracking_info: Dict[str, Any] | None = None
            warranty_info: Dict[str, Any] | None = None
            return_info: Dict[str, Any] | None = None

            if order_id:
                # 1) Get basic order info
                order_info = await order_tools.get_order_info(order_id)
                if order_info:
                    tool_results.append({
                        "tool": "get_order_info",
                        "result": order_info
                    })
                    tools_used.append("order_lookup")

                    # 2) Warranty details if user asks about it
                    if "warranty" in user_message.lower():
                        warranty_info = await order_tools.check_warranty(order_id)
                        tool_results.append({
                            "tool": "check_warranty",
                            "result": warranty_info
                        })
                        tools_used.append("warranty_check")

                    # 3) Tracking info if user asks to track / shipping / delivery
                    if any(word in user_message.lower() for word in ["track", "shipping", "delivery", "where is"]):
                        tracking_info = await order_tools.track_shipment(order_id)
                        tool_results.append({
                            "tool": "track_shipment",
                            "result": tracking_info
                        })
                        tools_used.append("shipment_tracking")

                    # 4) Return / exchange / refund flow
                    if any(word in user_message.lower() for word in ["return", "exchange", "refund"]):
                        return_reason = self._extract_return_reason(user_message)
                        return_info = await order_tools.initiate_return(order_id, return_reason)
                        tool_results.append({
                            "tool": "initiate_return",
                            "result": return_info
                        })
                        tools_used.append("return_processing")

            # -------------------------------
            # Build response WITHOUT OpenAI
            # -------------------------------
            if not order_id:
                response_text = (
                    "I can help you with your order, but I couldn't find an order number "
                    "in your message. Please share your order ID (for example: order #12345)."
                )
                confidence = 0.4

            elif not order_info:
                response_text = (
                    f"I checked our records, but I couldn't find any order with ID #{order_id}. "
                    "Please confirm the number or share more details."
                )
                confidence = 0.5

            else:
                # Build a detailed summary from mock order data
                oi = order_info
                response_lines: List[str] = [
                    f"Here are the details for order #{order_id}:",
                    f"- Customer: {oi.get('customer')}",
                    f"- Product: {oi.get('product')} (${oi.get('price')})",
                    f"- Status: {str(oi.get('status', '')).capitalize()}",
                    f"- Ordered on: {oi.get('order_date')}",
                    f"- Delivery date: {oi.get('delivery_date')}",
                    f"- Warranty: {oi.get('warranty')} (valid until {oi.get('warranty_expires')})",
                ]

                # Add tracking info if available
                if tracking_info:
                    ti = tracking_info
                    response_lines.append("")
                    response_lines.append("📦 Shipping / Tracking:")
                    if "status" in ti:
                        response_lines.append(f"- Shipment status: {ti['status']}")
                    if "expected_delivery" in ti and ti["expected_delivery"]:
                        response_lines.append(f"- Expected delivery: {ti['expected_delivery']}")
                    if "carrier" in ti:
                        response_lines.append(f"- Carrier: {ti['carrier']}")
                    if "tracking_number" in ti:
                        response_lines.append(f"- Tracking number: {ti['tracking_number']}")

                # Add warranty tool info if used
                if warranty_info:
                    wi = warranty_info
                    response_lines.append("")
                    response_lines.append("🛡 Warranty details:")
                    if "status" in wi:
                        response_lines.append(f"- Warranty status: {wi['status']}")
                    if "coverage" in wi:
                        response_lines.append(f"- Coverage: {wi['coverage']}")

                # Add return info if requested
                if return_info:
                    ri = return_info
                    response_lines.append("")
                    response_lines.append("↩ Return / Exchange:")
                    response_lines.append(f"- Return status: {ri.get('status', 'initiated')}")
                    if ri.get("reason"):
                        response_lines.append(f"- Reason recorded: {ri['reason']}")
                    if ri.get("instructions"):
                        response_lines.append(f"- Next steps: {ri['instructions']}")

                response_text = "\n".join(response_lines)
                confidence = 0.9

            return {
                "response": response_text,
                "agent_used": self.agent_type,
                "tools_used": tools_used,
                "tool_results": tool_results,
                "confidence": confidence,
                "thinking_process": (
                    "Response generated directly from local mock order data and tools "
                    "without calling an external LLM (useful when API quota is unavailable)."
                ),
            }

        except Exception as e:
            logger.error(f"Error in OrderAgent.process_request: {e}")
            return {
                "response": (
                    "I apologize, but I'm having trouble accessing order information right now. "
                    "Please provide your order number and I'll help you as soon as possible."
                ),
                "agent_used": self.agent_type,
                "tools_used": [],
                "tool_results": [],
                "confidence": 0.3,
                "thinking_process": f"Error occurred while processing order request: {str(e)}",
            }

    def _extract_order_id(self, message: str, context: Dict[str, Any]) -> str | None:
        """Extract order ID from message or context."""
        import re

        # Try to find order number in message, like "order #12345"
        order_pattern = r'order\s*#?(\d+)'
        match = re.search(order_pattern, message.lower())
        if match:
            return match.group(1)

        # Fallback: use most recently discussed order from context
        if context.get("orders_discussed"):
            return context["orders_discussed"][-1]  # Return most recent

        return None

    def _extract_return_reason(self, message: str) -> str:
        """Extract return reason from message."""
        message_lower = message.lower()

        # Map keywords to return reasons
        reason_map = {
            "defective": "defective",
            "broken": "defective",
            "damaged": "damaged_shipping",
            "wrong": "wrong_item",
            "not working": "defective",
            "doesn't work": "defective",
            "won't turn on": "defective",
            "performance": "performance_issue",
            "slow": "performance_issue",
            "changed mind": "customer_preference",
            "don't need": "customer_preference",
            "size": "size_issue",
        }

        for keyword, reason in reason_map.items():
            if keyword in message_lower:
                return reason

        return "other"  # Default reason
