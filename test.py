from app.agents.content_planner_agent.agent import ContentPlannerAgent
from app.agents.content_planner_agent.schema import ContentPlannerInput
from pprint import pprint

def main():
    agent = ContentPlannerAgent()
    input_data = ContentPlannerInput(
        original_topic="AI and mental health",
        persona="Curious Educator",
        tone="thoughtful",
        style="conversational",
        content_type="thread"
    )

    try:
        output = agent.run(input_data)
        print("\n✅ Output:")
        pprint(output.dict(), sort_dicts=False)
    except Exception as e:
        print(f"\n❌ Error occurred while running agent:\n{e}")

if __name__ == "__main__":
    main()
