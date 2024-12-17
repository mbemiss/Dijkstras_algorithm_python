#######################################################################################################################
# This code models a manufacturing process for rubber-to-metal bonded assemblies using NetworkX to analyze workflow 
# efficiency. It implements three key algorithms: 1) Dijkstra's algorithm to find the critical path, which identifies the 
# longest sequence of dependent tasks determining the minimum project completion time of 94 time units, 2) Breadth-First 
# Search (BFS) to systematically explore the manufacturing process flow, and 3) Centrality analysis to identify the most 
# crucial tasks based on their connections within the workflow. The visual diagram shows three parallel production paths - 
# rubber processing, chemical treatment, and cleaning/adhesive treatment - that converge at the assembly stage before 
# proceeding through final operations like injection molding, testing, and shipping. The critical path includes tasks like 
# "Calendar Rubber Sheets," "Injection Molding Operation," and "Paint & Finishing," which are essential for timely project 
# completion. The BFS traversal path highlights the sequential order of tasks, starting from the "Start" node and ending at 
# the "End" node. Centrality analysis reveals the most critical tasks based on their degree and betweenness centrality 
# measures, with "Assemble Components for Injection Molding" and "Paint & Finishing" emerging as key nodes in the workflow. 
# This analysis provides valuable insights into the manufacturing process, enabling managers to optimize task sequences, 
# allocate resources efficiently, and enhance overall productivity.
#######################################################################################################################

# Importing Required Libraries
import networkx as nx # The NetworkX library is used for graph analysis

# Create a directed graph
G = nx.DiGraph() # Directed graph (DiGraph) is used for modeling the manufacturing process below

# Add nodes (tasks)
tasks = [ # (task, duration)
    ('Start', 0),
    ('Create Work Order', 2),
    ('Process Rubber Blending', 10),
    ('Mill Rubber', 8),
    ('Calendar Rubber Sheets', 14),
    ('Sandblast Parts', 10),
    ('Wash Parts for Chemical Treatment', 2),
    ('Chemical Treatment Group 1', 6),
    ('Chemical Treatment Group 2', 10),
    ('Chemical Treatment Group 3', 4),
    ('Spray Treatment', 8),
    ('Assemble Components for Injection Molding', 8),
    ('Clean Outer & Inner Members', 4),
    ('Special Adhesive Treatment', 12),
    ('Special Sandblast', 6),
    ('Wash Parts OM & IM', 2),    
    ('Injection Molding Operation', 18),
    ('Bond Testing', 6),
    ('Paint & Finishing', 14),
    ('Final Inspection', 6),
    ('Packaging', 6),
    ('Shipping', 2),
    ('End', 0)
]

# Add nodes with duration as attribute
for task, duration in tasks: # (task, duration)
    G.add_node(task, duration=duration) # Add node with duration attribute

# Add edges (task dependencies)
edges = [ # (task1, task2)
    ('Start', 'Create Work Order'),
    ('Create Work Order', 'Process Rubber Blending'),
    ('Create Work Order', 'Sandblast Parts'),
    ('Create Work Order', 'Clean Outer & Inner Members'),
    ('Process Rubber Blending', 'Mill Rubber'),
    ('Mill Rubber', 'Calendar Rubber Sheets'),    
    ('Calendar Rubber Sheets', 'Assemble Components for Injection Molding'),
    ('Sandblast Parts', 'Wash Parts for Chemical Treatment'),
    ('Wash Parts for Chemical Treatment', 'Chemical Treatment Group 1'),
    ('Wash Parts for Chemical Treatment', 'Chemical Treatment Group 2'),
    ('Wash Parts for Chemical Treatment', 'Chemical Treatment Group 3'),
    ('Chemical Treatment Group 1', 'Spray Treatment'),
    ('Chemical Treatment Group 2', 'Spray Treatment'),
    ('Chemical Treatment Group 3', 'Spray Treatment'),
    ('Spray Treatment', 'Assemble Components for Injection Molding'),
    ('Clean Outer & Inner Members', 'Special Adhesive Treatment'),
    ('Special Adhesive Treatment', 'Special Sandblast'),
    ('Special Sandblast', 'Wash Parts OM & IM'),
    ('Wash Parts OM & IM', 'Assemble Components for Injection Molding'),
    ('Assemble Components for Injection Molding', 'Injection Molding Operation'),
    ('Injection Molding Operation', 'Bond Testing'),
    ('Bond Testing', 'Paint & Finishing'),
    ('Paint & Finishing', 'Final Inspection'),
    ('Final Inspection', 'Packaging'),
    ('Packaging', 'Shipping'),
    ('Shipping', 'End')
]

G.add_edges_from(edges) # Add edges to the graph

def find_critical_path(G): # Find the critical path in the graph
    # Create a copy of the graph with negated weights
    G_neg = G.copy() # Copy the graph
    for u, v, data in G_neg.edges(data=True): # Iterate through the edges
        data['weight'] = -G.nodes[u]['duration'] # Negate the weight

    # Find the longest path (shortest path with negated weights)
    path = nx.dijkstra_path(G_neg, 'Start', 'End', weight='weight') # Find the longest path
    
    # Calculate the total duration of the critical path
    total_duration = sum(G.nodes[task]['duration'] for task in path) # Calculate the total duration
    
    return path, total_duration # Return the critical path and total duration

critical_path, total_duration = find_critical_path(G) # Find the critical path

print("Critical Path:") # Print the critical path
for task in critical_path: # Iterate through the critical path
    print(f"- {task} (Duration: {G.nodes[task]['duration']})") # Print the task and duration
print(f"Total Duration: {total_duration} time units") # Print the total duration

# Breadth-First Search Implementation
def perform_bfs(G, start='Start'): # Perform Breadth-First Search (BFS) traversal
    bfs_path = list(nx.bfs_edges(G, start)) # Perform BFS traversal
    print("\nBFS Traversal Path:") # Print the BFS traversal path
    for edge in bfs_path: # Iterate through the BFS path
        print(f"- {edge[0]} → {edge[1]}") # Print the edge
    return bfs_path # Return the BFS path

# Centrality Analysis Implementation
def analyze_centrality(G): # Analyze centrality measures
    degree_centrality = nx.degree_centrality(G) # Calculate degree centrality
    betweenness_centrality = nx.betweenness_centrality(G) # Calculate betweenness centrality
    
    print("\nDegree Centrality (Top 5 nodes):") # Print the top 5 nodes by degree centrality
    sorted_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5] # Sort by degree centrality
    for node, centrality in sorted_degree: # Iterate through the top 5 nodes
        print(f"- {node}: {centrality:.3f}") # Print the node and centrality
        
    print("\nBetweenness Centrality (Top 5 nodes):") # Print the top 5 nodes by betweenness centrality
    sorted_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5] # Sort by betweenness centrality
    for node, centrality in sorted_betweenness: # Iterate through the top 5 nodes
        print(f"- {node}: {centrality:.3f}") # Print the node and centrality

# Execute additional algorithms
perform_bfs(G) # Perform BFS traversal
analyze_centrality(G) # Analyze centrality measures
