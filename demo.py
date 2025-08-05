#!/usr/bin/env python3
"""
Oracle EBS R12 i-Supplier Assistant - Demo Script
This script demonstrates the chatbot functionality without the full web interface
"""

import asyncio
import json
import sys
import os

# Add the workspace to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.oracle_agent import OracleEBSAgent
from backend.models import SessionState, WorkflowStatus
from backend.session_manager import SessionManager

class ChatDemo:
    def __init__(self):
        self.agent = OracleEBSAgent()
        self.session_manager = SessionManager()
        self.session_id = "demo_session_001"
        
    async def initialize(self):
        """Initialize the agent"""
        await self.agent.initialize()
        print("🤖 Oracle EBS R12 i-Supplier Assistant - Demo Mode")
        print("=" * 60)
        print("Welcome to the Oracle EBS R12 i-Supplier Assistant for Tanger Med!")
        print("This assistant can help you with:")
        print("• Creating work confirmations")
        print("• Submitting invoices") 
        print("• Viewing purchase orders")
        print("• Querying Oracle EBS data")
        print()
        print("Type 'help' for available commands or 'quit' to exit")
        print("-" * 60)
        
    async def run_demo(self):
        """Run the interactive demo"""
        await self.initialize()
        
        while True:
            try:
                # Get user input
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Thank you for using Oracle EBS Assistant!")
                    break
                    
                # Get session
                session = self.session_manager.get_session(self.session_id)
                
                # Process message
                print("\n🤖 Assistant: ", end="", flush=True)
                response = await self.agent.process_message(user_input, session)
                
                # Print response
                print(response.message)
                
                # Update session
                self.session_manager.update_session(self.session_id, response.session_state)
                
                # Show current step if available
                if response.current_step:
                    print(f"\n📋 Current Step: {response.current_step.title}")
                    if response.current_step.screenshot:
                        print(f"📸 Screenshot: {response.current_step.screenshot}")
                        
                # Show suggestions
                if response.suggestions:
                    print(f"\n💡 Suggestions: {', '.join(response.suggestions)}")
                    
                # Show session progress
                if response.session_state.current_procedure:
                    completed = len(response.session_state.completed_steps)
                    current_step = response.session_state.current_step
                    print(f"\n📊 Progress: {completed} steps completed")
                    if current_step:
                        print(f"   Current: {current_step}")
                        
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                
async def run_automated_demo():
    """Run an automated demo showing different features"""
    demo = ChatDemo()
    await demo.initialize()
    
    # Demo scenarios
    scenarios = [
        "help",
        "start work confirmation", 
        "done",
        "next",
        "done", 
        "show purchase orders",
        "search po-2024-001",
        "list invoices"
    ]
    
    print("\n🎬 Running Automated Demo...")
    print("=" * 40)
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n[Demo Step {i}] User: {scenario}")
        
        # Get session
        session = demo.session_manager.get_session(demo.session_id)
        
        # Process message
        response = await demo.agent.process_message(scenario, session)
        
        # Print response (truncated for demo)
        response_preview = response.message[:200] + "..." if len(response.message) > 200 else response.message
        print(f"Assistant: {response_preview}")
        
        # Update session
        demo.session_manager.update_session(demo.session_id, response.session_state)
        
        # Show progress
        if response.session_state.current_procedure:
            print(f"📊 Procedure: {response.session_state.current_procedure}")
            print(f"   Completed Steps: {len(response.session_state.completed_steps)}")
            
        # Wait between steps
        await asyncio.sleep(1)
        
    print("\n✅ Automated demo completed!")

def show_procedures():
    """Show available procedures"""
    try:
        with open('procedures.json', 'r') as f:
            data = json.load(f)
            procedures = data.get('procedures', {})
            
        print("\n📋 Available Procedures:")
        print("=" * 40)
        
        for proc_id, proc_data in procedures.items():
            print(f"\n🔹 {proc_data['title']}")
            print(f"   ID: {proc_id}")
            print(f"   Category: {proc_data.get('category', 'N/A')}")
            print(f"   Description: {proc_data['description']}")
            print(f"   Steps: {len(proc_data.get('steps', []))}")
            
            if proc_data.get('prerequisites'):
                print("   Prerequisites:")
                for prereq in proc_data['prerequisites']:
                    print(f"   • {prereq}")
                    
    except FileNotFoundError:
        print("❌ procedures.json not found")
    except Exception as e:
        print(f"❌ Error loading procedures: {e}")

def show_oracle_data():
    """Show sample Oracle data"""
    print("\n🗄️  Sample Oracle EBS Data:")
    print("=" * 40)
    
    # This would normally come from the agent
    sample_data = {
        "Purchase Orders": [
            {"PO": "PO-2024-001", "Supplier": "Tanger Med Services", "Amount": "50,000 MAD"},
            {"PO": "PO-2024-002", "Supplier": "Mediterranean Logistics", "Amount": "25,000 MAD"}
        ],
        "Invoices": [
            {"Invoice": "INV-2024-001", "PO": "PO-2024-001", "Status": "Submitted"}
        ],
        "Suppliers": [
            {"ID": "SUP-001", "Name": "Tanger Med Services", "Status": "Active"},
            {"ID": "SUP-002", "Name": "Mediterranean Logistics", "Status": "Active"}
        ]
    }
    
    for category, items in sample_data.items():
        print(f"\n📊 {category}:")
        for item in items:
            print(f"   • {', '.join([f'{k}: {v}' for k, v in item.items()])}")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "auto":
            print("Running automated demo...")
            asyncio.run(run_automated_demo())
        elif command == "procedures":
            show_procedures()
        elif command == "data":
            show_oracle_data()
        elif command == "help":
            print("Oracle EBS Assistant Demo Commands:")
            print("  python demo.py          - Interactive chat demo")
            print("  python demo.py auto     - Automated demo")
            print("  python demo.py procedures - Show available procedures")
            print("  python demo.py data     - Show sample Oracle data")
            print("  python demo.py help     - Show this help")
        else:
            print(f"Unknown command: {command}")
            print("Use 'python demo.py help' for available commands")
    else:
        # Interactive demo
        asyncio.run(ChatDemo().run_demo())

if __name__ == "__main__":
    main()