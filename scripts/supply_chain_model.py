"""
Optoelectronics Supply Chain Network Model
===========================================

This script models an optoelectronics supply chain as a directed graph
and simulates the impact of localized disruptions on system-level performance.

Author: Academic Prototype Project
Purpose: Demonstrate how small inefficiencies can create larger system impacts
"""

import networkx as nx
import matplotlib.pyplot as plt
import os

# ============================================================================
# SECTION 1: CREATE THE BASE SUPPLY CHAIN GRAPH
# ============================================================================

def create_graph():
    """
    Creates a directed graph representing the optoelectronics supply chain.
    
    Returns:
        G: A NetworkX directed graph with nodes and edges representing
           the supply chain structure
    """
    # Initialize a directed graph
    G = nx.DiGraph()
    
    # Define all nodes in the supply chain
    # Suppliers (upstream)
    suppliers = [
        "Wafer Supplier",
        "Lens Supplier",
        "PCB Supplier",
        "Packaging Supplier"
    ]
    
    # Manufacturing stages (middle)
    manufacturing = [
        "Component Assembly",
        "Optical Calibration",
        "Final Testing"
    ]
    
    # Downstream entities
    downstream = [
        "Distributor",
        "OEM Customer"
    ]
    
    # Add all nodes to the graph
    G.add_nodes_from(suppliers)
    G.add_nodes_from(manufacturing)
    G.add_nodes_from(downstream)
    
    # Define edges representing material flow and dependencies
    # All suppliers feed into Component Assembly
    edges = [
        ("Wafer Supplier", "Component Assembly"),
        ("Lens Supplier", "Component Assembly"),
        ("PCB Supplier", "Component Assembly"),
        ("Packaging Supplier", "Component Assembly"),
        
        # Manufacturing flow
        ("Component Assembly", "Optical Calibration"),
        ("Optical Calibration", "Final Testing"),
        
        # Distribution flow
        ("Final Testing", "Distributor"),
        ("Distributor", "OEM Customer")
    ]
    
    # Add edges to the graph
    G.add_edges_from(edges)
    
    return G

# ============================================================================
# SECTION 2: COMPUTE STRUCTURAL METRICS
# ============================================================================

def compute_metrics(G, case_name="Base Case"):
    """
    Computes key structural metrics for the supply chain network.
    
    Parameters:
        G: NetworkX directed graph
        case_name: String identifier for the case (e.g., "Base Case" or "Disrupted")
    
    Returns:
        metrics_dict: Dictionary containing computed metrics
    """
    print(f"\n{'='*70}")
    print(f"{case_name} - Network Metrics")
    print(f"{'='*70}\n")
    
    metrics_dict = {}
    
    # Compute in-degree and out-degree for each node
    print("Node Metrics:")
    print(f"{'Node':<25} {'In-Degree':<12} {'Out-Degree':<12} {'Betweenness':<12}")
    print("-" * 70)
    
    # Calculate betweenness centrality
    # This measures how often a node appears on shortest paths between other nodes
    betweenness = nx.betweenness_centrality(G)
    
    node_metrics = []
    for node in G.nodes():
        in_deg = G.in_degree(node)
        out_deg = G.out_degree(node)
        between = betweenness[node]
        
        print(f"{node:<25} {in_deg:<12} {out_deg:<12} {between:<12.4f}")
        
        node_metrics.append({
            'node': node,
            'in_degree': in_deg,
            'out_degree': out_deg,
            'betweenness': between
        })
    
    metrics_dict['node_metrics'] = node_metrics
    
    # Compute average shortest path length (if graph is connected)
    print("\nNetwork-Level Metrics:")
    print("-" * 70)
    
    # Check if the graph is weakly connected
    # For directed graphs, we need to check if there's a path considering direction
    if nx.is_weakly_connected(G):
        # For directed acyclic graphs (DAGs) like supply chains,
        # we compute average path length only for reachable pairs
        try:
            # Try to compute for strongly connected components
            avg_path_length = nx.average_shortest_path_length(G)
            print(f"Average Shortest Path Length: {avg_path_length:.4f}")
            metrics_dict['avg_path_length'] = avg_path_length
        except nx.NetworkXError:
            # If not strongly connected, compute for reachable node pairs
            total_length = 0
            count = 0
            for source in G.nodes():
                lengths = nx.single_source_shortest_path_length(G, source)
                for target, length in lengths.items():
                    if source != target:
                        total_length += length
                        count += 1
            
            if count > 0:
                avg_path_length = total_length / count
                print(f"Average Shortest Path Length (reachable pairs): {avg_path_length:.4f}")
                metrics_dict['avg_path_length'] = avg_path_length
            else:
                print("Average Shortest Path Length: N/A (No reachable pairs)")
                metrics_dict['avg_path_length'] = None
    else:
        print("Average Shortest Path Length: N/A (Graph is not connected)")
        metrics_dict['avg_path_length'] = None
    
    # Number of nodes and edges
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    print(f"Number of Nodes: {num_nodes}")
    print(f"Number of Edges: {num_edges}")
    
    metrics_dict['num_nodes'] = num_nodes
    metrics_dict['num_edges'] = num_edges
    
    return metrics_dict

# ============================================================================
# SECTION 3: VISUALIZE THE NETWORK
# ============================================================================

def plot_graph(G, filename, title):
    """
    Creates a publication-quality visualization of the supply chain network.
    
    Parameters:
        G: NetworkX directed graph
        filename: Path where the figure will be saved
        title: Title for the graph
    """
    # Create a new figure with high resolution
    plt.figure(figsize=(14, 10))
    
    # Define node categories for coloring
    suppliers = [
        "Wafer Supplier",
        "Lens Supplier",
        "PCB Supplier",
        "Packaging Supplier"
    ]
    
    manufacturing = [
        "Component Assembly",
        "Optical Calibration",
        "Final Testing"
    ]
    
    downstream = [
        "Distributor",
        "OEM Customer"
    ]
    
    # Create color map for nodes
    node_colors = []
    for node in G.nodes():
        if node in suppliers:
            node_colors.append('#3498db')  # Blue for suppliers
        elif node in manufacturing:
            node_colors.append('#e74c3c')  # Red for manufacturing
        elif node in downstream:
            node_colors.append('#2ecc71')  # Green for downstream
        else:
            node_colors.append('#95a5a6')  # Gray for others
    
    # Use hierarchical layout to show upstream -> downstream flow
    # Create position dictionary manually for better control
    pos = {}
    
    # Position suppliers at the top (y=3)
    supplier_x_positions = [-3, -1, 1, 3]
    for i, supplier in enumerate(suppliers):
        if supplier in G.nodes():
            pos[supplier] = (supplier_x_positions[i], 3)
    
    # Position manufacturing stages in the middle
    if "Component Assembly" in G.nodes():
        pos["Component Assembly"] = (0, 2)
    if "Optical Calibration" in G.nodes():
        pos["Optical Calibration"] = (0, 1)
    if "Final Testing" in G.nodes():
        pos["Final Testing"] = (0, 0)
    
    # Position downstream entities at the bottom
    if "Distributor" in G.nodes():
        pos["Distributor"] = (0, -1)
    if "OEM Customer" in G.nodes():
        pos["OEM Customer"] = (0, -2)
    
    # Draw the network
    nx.draw_networkx_nodes(G, pos, 
                          node_color=node_colors,
                          node_size=3000,
                          alpha=0.9,
                          edgecolors='black',
                          linewidths=2)
    
    nx.draw_networkx_labels(G, pos,
                           font_size=10,
                           font_weight='bold',
                           font_family='sans-serif')
    
    nx.draw_networkx_edges(G, pos,
                          edge_color='#34495e',
                          arrows=True,
                          arrowsize=20,
                          arrowstyle='->',
                          width=2,
                          alpha=0.7,
                          connectionstyle='arc3,rad=0.1')
    
    # Add title and legend
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    
    # Create legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#3498db', edgecolor='black', label='Suppliers'),
        Patch(facecolor='#e74c3c', edgecolor='black', label='Manufacturing'),
        Patch(facecolor='#2ecc71', edgecolor='black', label='Downstream')
    ]
    plt.legend(handles=legend_elements, loc='upper right', fontsize=12)
    
    # Remove axes
    plt.axis('off')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nGraph saved to: {filename}")
    plt.close()

# ============================================================================
# SECTION 4: SAVE METRICS TO FILE
# ============================================================================

def save_metrics_to_file(metrics_dict, filename, case_name):
    """
    Saves computed metrics to a text file.
    
    Parameters:
        metrics_dict: Dictionary containing metrics
        filename: Path where the metrics will be saved
        case_name: Name of the case (e.g., "Base Case")
    """
    with open(filename, 'w') as f:
        f.write("="*70 + "\n")
        f.write(f"{case_name} - Network Metrics\n")
        f.write("="*70 + "\n\n")
        
        f.write("Node Metrics:\n")
        f.write(f"{'Node':<25} {'In-Degree':<12} {'Out-Degree':<12} {'Betweenness':<12}\n")
        f.write("-" * 70 + "\n")
        
        for node_data in metrics_dict['node_metrics']:
            f.write(f"{node_data['node']:<25} "
                   f"{node_data['in_degree']:<12} "
                   f"{node_data['out_degree']:<12} "
                   f"{node_data['betweenness']:<12.4f}\n")
        
        f.write("\nNetwork-Level Metrics:\n")
        f.write("-" * 70 + "\n")
        
        if metrics_dict['avg_path_length'] is not None:
            f.write(f"Average Shortest Path Length: {metrics_dict['avg_path_length']:.4f}\n")
        else:
            f.write("Average Shortest Path Length: N/A (Graph is not connected)\n")
        
        f.write(f"Number of Nodes: {metrics_dict['num_nodes']}\n")
        f.write(f"Number of Edges: {metrics_dict['num_edges']}\n")
    
    print(f"Metrics saved to: {filename}")

# ============================================================================
# SECTION 5: SIMULATE DISRUPTION
# ============================================================================

def simulate_disruption(G, node_to_remove):
    """
    Simulates a supply chain disruption by removing a node.
    
    Parameters:
        G: Original NetworkX directed graph
        node_to_remove: Name of the node to remove
    
    Returns:
        G_disrupted: New graph with the node removed
    """
    # Create a copy of the graph
    G_disrupted = G.copy()
    
    # Remove the specified node
    if node_to_remove in G_disrupted.nodes():
        G_disrupted.remove_node(node_to_remove)
        print(f"\n{'='*70}")
        print(f"DISRUPTION SIMULATION")
        print(f"{'='*70}")
        print(f"\nRemoved node: {node_to_remove}")
        print(f"This simulates a manufacturing stage becoming unavailable.")
    else:
        print(f"\nWarning: Node '{node_to_remove}' not found in graph.")
    
    return G_disrupted

# ============================================================================
# SECTION 6: COMPARE RESULTS
# ============================================================================

def compare_results(base_metrics, disrupted_metrics, output_file):
    """
    Compares base case and disrupted case metrics.
    
    Parameters:
        base_metrics: Dictionary of base case metrics
        disrupted_metrics: Dictionary of disrupted case metrics
        output_file: Path to save comparison results
    """
    print(f"\n{'='*70}")
    print("COMPARISON: Base Case vs. Disrupted Case")
    print(f"{'='*70}\n")
    
    comparison_text = []
    comparison_text.append("="*70)
    comparison_text.append("COMPARISON: Base Case vs. Disrupted Case")
    comparison_text.append("="*70)
    comparison_text.append("")
    
    # Compare network-level metrics
    comparison_text.append("Network-Level Changes:")
    comparison_text.append("-" * 70)
    
    print("Network-Level Changes:")
    print("-" * 70)
    
    # Number of nodes
    node_change = disrupted_metrics['num_nodes'] - base_metrics['num_nodes']
    print(f"Nodes: {base_metrics['num_nodes']} -> {disrupted_metrics['num_nodes']} (Change: {node_change})")
    comparison_text.append(f"Nodes: {base_metrics['num_nodes']} -> {disrupted_metrics['num_nodes']} (Change: {node_change})")
    
    # Number of edges
    edge_change = disrupted_metrics['num_edges'] - base_metrics['num_edges']
    print(f"Edges: {base_metrics['num_edges']} -> {disrupted_metrics['num_edges']} (Change: {edge_change})")
    comparison_text.append(f"Edges: {base_metrics['num_edges']} -> {disrupted_metrics['num_edges']} (Change: {edge_change})")
    
    # Average path length
    if base_metrics['avg_path_length'] is not None and disrupted_metrics['avg_path_length'] is not None:
        path_change = disrupted_metrics['avg_path_length'] - base_metrics['avg_path_length']
        print(f"Avg Path Length: {base_metrics['avg_path_length']:.4f} -> {disrupted_metrics['avg_path_length']:.4f} (Change: {path_change:+.4f})")
        comparison_text.append(f"Avg Path Length: {base_metrics['avg_path_length']:.4f} -> {disrupted_metrics['avg_path_length']:.4f} (Change: {path_change:+.4f})")
    elif base_metrics['avg_path_length'] is not None and disrupted_metrics['avg_path_length'] is None:
        print(f"Avg Path Length: {base_metrics['avg_path_length']:.4f} -> N/A (Graph became disconnected)")
        comparison_text.append(f"Avg Path Length: {base_metrics['avg_path_length']:.4f} -> N/A (Graph became disconnected)")
    
    comparison_text.append("")
    comparison_text.append("Key Observations:")
    comparison_text.append("-" * 70)
    
    print("\nKey Observations:")
    print("-" * 70)
    
    # Analyze connectivity
    if base_metrics['avg_path_length'] is not None and disrupted_metrics['avg_path_length'] is None:
        obs = "• The network became DISCONNECTED after the disruption"
        print(obs)
        comparison_text.append(obs)
        obs = "• This indicates a critical bottleneck was removed"
        print(obs)
        comparison_text.append(obs)
    
    # Analyze edge loss
    if edge_change < 0:
        obs = f"• Lost {abs(edge_change)} supply chain connections"
        print(obs)
        comparison_text.append(obs)
    
    # Analyze structural impact
    obs = "• Removing a single manufacturing stage disrupted the entire downstream flow"
    print(obs)
    comparison_text.append(obs)
    
    obs = "• This demonstrates how localized inefficiencies can have system-level impacts"
    print(obs)
    comparison_text.append(obs)
    
    # Save to file
    with open(output_file, 'w') as f:
        f.write('\n'.join(comparison_text))
    
    print(f"\nComparison saved to: {output_file}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main function that orchestrates the entire analysis.
    """
    print("\n" + "="*70)
    print("OPTOELECTRONICS SUPPLY CHAIN NETWORK ANALYSIS")
    print("="*70)
    print("\nThis analysis demonstrates how small localized disruptions")
    print("can create significant system-level impacts in supply chains.")
    print("="*70)
    
    # Define output paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    graphs_dir = os.path.join(base_dir, 'outputs', 'graphs')
    metrics_dir = os.path.join(base_dir, 'outputs', 'metrics')
    
    # Ensure output directories exist
    os.makedirs(graphs_dir, exist_ok=True)
    os.makedirs(metrics_dir, exist_ok=True)
    
    # Step 1: Create base supply chain graph
    print("\n[Step 1] Creating base supply chain graph...")
    G_base = create_graph()
    print(f"Created graph with {G_base.number_of_nodes()} nodes and {G_base.number_of_edges()} edges")
    
    # Step 2: Visualize base network
    print("\n[Step 2] Visualizing base supply chain network...")
    base_graph_path = os.path.join(graphs_dir, 'base_supply_chain_network.png')
    plot_graph(G_base, base_graph_path, "Base Supply Chain Network")
    
    # Step 3: Compute base case metrics
    print("\n[Step 3] Computing base case metrics...")
    base_metrics = compute_metrics(G_base, "Base Case")
    
    # Save base case metrics
    base_metrics_path = os.path.join(metrics_dir, 'base_case_metrics.txt')
    save_metrics_to_file(base_metrics, base_metrics_path, "Base Case")
    
    # Step 4: Simulate disruption
    print("\n[Step 4] Simulating supply chain disruption...")
    node_to_disrupt = "Optical Calibration"
    G_disrupted = simulate_disruption(G_base, node_to_disrupt)
    
    # Step 5: Visualize disrupted network
    print("\n[Step 5] Visualizing disrupted supply chain network...")
    disrupted_graph_path = os.path.join(graphs_dir, 'disrupted_supply_chain_network.png')
    plot_graph(G_disrupted, disrupted_graph_path, 
              f"Disrupted Supply Chain Network\n(Removed: {node_to_disrupt})")
    
    # Step 6: Compute disrupted case metrics
    print("\n[Step 6] Computing disrupted case metrics...")
    disrupted_metrics = compute_metrics(G_disrupted, "Disrupted Case")
    
    # Step 7: Compare results
    print("\n[Step 7] Comparing base case and disrupted case...")
    comparison_path = os.path.join(metrics_dir, 'disruption_comparison.txt')
    compare_results(base_metrics, disrupted_metrics, comparison_path)
    
    # Summary
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print("\nGenerated outputs:")
    print(f"  • {base_graph_path}")
    print(f"  • {disrupted_graph_path}")
    print(f"  • {base_metrics_path}")
    print(f"  • {comparison_path}")
    print("\nThese files can be used in your academic report to demonstrate")
    print("the impact of localized disruptions on supply chain performance.")
    print("="*70 + "\n")

# Run the analysis
if __name__ == "__main__":
    main()
