import graphviz

def generate_dot_content(room_dict):
    """Generates the content for the DOT file."""

    # Start the directed graph definition
    dot_content = "digraph GameFlow {\n"
    dot_content += '    // Global style settings\n'
    dot_content += '    rankdir=TB; // Top to Bottom layout\n'
    dot_content += '    node [shape=box, style="filled", fillcolor="aliceblue"];\n\n'
    
    # --- 1. Define Nodes (Scenes) ---
    dot_content += '    // Node Definitions\n'
    for room in room_dict.values():
        node_id = room["id"]
        node_title = room["title"]

        # Highlight End Nodes differently
        if not room["choices"]:
            style = 'fillcolor="lightgreen", peripheries=2'
        else:
            style = 'fillcolor="aliceblue"'

        dot_content += f'    {node_id} [label="{node_title}", {style}];\n'

    # --- 2. Define Edges (Paths/Choices) ---
    dot_content += '\n    // Edge Definitions\n'
    for room in room_dict.values():
        source_id = room["id"]

        for choice in room["choices"]:
            target_id = choice["id"]
            choice_text = choice["text"]

            # Use the IDs to create the connection with the choice text as the label
            dot_content += f'    {source_id} -> {target_id} [label="{choice_text}"];\n'

    # Close the graph definition
    dot_content += "}\n"

    return dot_content

def generate_image(dot_code):
    """Generates the image directly using the graphviz Python library."""
    # Create a Source object from the DOT code
    source = graphviz.Source(dot_code)
    # Render it to a file (e.g., 'game_flow.gv.png')
    source.render('game_flow', view=True, format='png') 
    # 'view=True' attempts to open the image automatically
