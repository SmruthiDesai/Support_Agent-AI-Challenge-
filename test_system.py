#!/usr/bin/env python3
"""Test script to validate the multi-agent customer care system."""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Test basic module imports without API dependencies."""
    print("🧪 Testing basic module imports...")
    
    try:
        from memory.session_memory import memory
        print("✅ Memory system imported successfully")
        
        from planning.planner import planner  
        print("✅ Planning module imported successfully")
        
        from data.mock_data import orders, products, knowledge_base
        print(f"✅ Mock data imported successfully - {len(orders)} orders, {len(products)} products, {len(knowledge_base)} knowledge items")
        
        return True
    except Exception as e:
        print(f"❌ Basic import failed: {e}")
        return False

def test_memory_system():
    """Test the memory system functionality."""
    print("\n🧪 Testing memory system...")
    
    try:
        from memory.session_memory import memory
        
        # Create test session
        session_id = "test-session-123"
        created_id, session = memory.get_or_create_session(session_id)
        print(f"✅ Session created: {created_id}")
        
        # Add test messages
        memory.add_message(session_id, "user", "Test message from user")
        memory.add_message(session_id, "assistant", "Test response from assistant")
        
        # Retrieve conversation
        history = memory.get_conversation_history(session_id)
        print(f"✅ Conversation history retrieved: {len(history)} messages")
        
        # Get context
        context = memory.get_context_for_agents(session_id)
        print(f"✅ Agent context generated: {len(context)} items")
        
        return True
    except Exception as e:
        print(f"❌ Memory system test failed: {e}")
        return False

def test_planning_system():
    """Test the planning system functionality."""
    print("\n🧪 Testing planning system...")
    
    try:
        from planning.planner import planner
        import asyncio
        
        async def test_plan():
            # Test plan creation
            test_request = "My laptop order #12345 won't turn on, I need help!"
            test_context = {"orders_discussed": ["12345"]}
            
            plan = await planner.create_plan(test_request, test_context)
            print(f"✅ Plan created: {plan.plan_id} with {len(plan.steps)} steps")
            
            # Test plan validation
            is_valid, issues = await planner.validate_plan(plan)
            print(f"✅ Plan validation: {'PASSED' if is_valid else 'FAILED'}")
            if issues:
                print(f"   Issues: {issues}")
            
            return True
        
        # Run async test
        result = asyncio.run(test_plan())
        return result
        
    except Exception as e:
        print(f"❌ Planning system test failed: {e}")
        return False

def test_data_access():
    """Test mock data access functionality."""
    print("\n🧪 Testing data access...")
    
    try:
        from data.mock_data import get_order, get_product, search_knowledge_base, get_policy
        
        # Test order lookup
        order = get_order("12345")
        if order:
            print(f"✅ Order lookup successful: {order['customer']} - {order['product']}")
        else:
            print("❌ Order lookup failed")
            return False
        
        # Test product lookup
        product = get_product("TB-PRO-15")
        if product:
            print(f"✅ Product lookup successful: {product['name']} - ${product['price']}")
        else:
            print("❌ Product lookup failed")
            return False
        
        # Test knowledge base search
        steps = search_knowledge_base("laptop won't turn on")
        if steps:
            print(f"✅ Knowledge base search successful: {len(steps)} steps found")
        else:
            print("❌ Knowledge base search failed")
            return False
        
        # Test policy lookup
        policy = get_policy("return")
        if policy:
            print(f"✅ Policy lookup successful: {policy['period_days']} day return period")
        else:
            print("❌ Policy lookup failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Data access test failed: {e}")
        return False

def test_tools_without_api():
    """Test tools that don't require API keys."""
    print("\n🧪 Testing tools (without API keys)...")
    
    try:
        # Test order tools
        from tools.order_tools import order_tools
        import asyncio
        
        async def test_order_tools():
            order_info = await order_tools.get_order_info("12345")
            if order_info:
                print(f"✅ Order tools working: Order status = {order_info['status']}")
            else:
                print("❌ Order tools failed")
                return False
            
            return True
        
        result = asyncio.run(test_order_tools())
        return result
        
    except Exception as e:
        print(f"❌ Tools test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Multi-Agent Customer Care System - Test Suite")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_memory_system,
        test_planning_system,
        test_data_access,
        test_tools_without_api
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("✅ PASSED\n")
            else:
                print("❌ FAILED\n")
        except Exception as e:
            print(f"❌ FAILED with exception: {e}\n")
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to run.")
        print("\n📝 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up API keys in .env file (optional - system works without them)")
        print("3. Run the server: python main.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()