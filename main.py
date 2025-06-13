# custom imports
from flexible_deep_researcher.graph import build_graph
from flexible_deep_researcher.state import SummaryStateInput

# Build graph
graph = build_graph()

user_input = input("what do you want to explore today?\n")

# Test
research_input = SummaryStateInput(
    research_topic=user_input
)
summary = graph.invoke(research_input)
print(summary)