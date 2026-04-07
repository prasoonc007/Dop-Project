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
    
    # Add node parameters (deterministic dataset - NO RANDOMNESS)
    # Manufacturing nodes with specific parameters
    G.nodes["Component Assembly"]["processing_time_min"] = 10
    G.nodes["Component Assembly"]["capacity_uph"] = 120
    G.nodes["Component Assembly"]["defect_rate"] = 0.05
    
    G.nodes["Optical Calibration"]["processing_time_min"] = 15
    G.nodes["Optical Calibration"]["capacity_uph"] = 80
    G.nodes["Optical Calibration"]["defect_rate"] = 0.08
    
    G.nodes["Final Testing"]["processing_time_min"] = 8
    G.nodes["Final Testing"]["capacity_uph"] = 100
    G.nodes["Final Testing"]["defect_rate"] = 0.04
    
    # All suppliers and downstream nodes with standard parameters
    for node in suppliers + downstream:
        G.nodes[node]["processing_time_min"] = 2
        G.nodes[node]["capacity_uph"] = 200
        G.nodes[node]["defect_rate"] = 0.01
    
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
# SECTION 7: KPI CALCULATIONS
# ============================================================================

def compute_kpis(G, path):
    """
    Computes KPIs for a given path through the supply chain.
    
    Parameters:
        G: NetworkX directed graph with node attributes
        path: List of node names representing the path
    
    Returns:
        kpis: Dictionary containing Lead Time, Throughput, and Yield
    """
    # Lead Time: Sum of processing_time_min across path
    lead_time = sum(G.nodes[node]["processing_time_min"] for node in path)
    
    # Throughput: Minimum capacity_uph across path (bottleneck)
    throughput = min(G.nodes[node]["capacity_uph"] for node in path)
    
    # Yield: Product of (1 - defect_rate) across path
    yield_value = 1.0
    for node in path:
        yield_value *= (1 - G.nodes[node]["defect_rate"])
    
    return {
        "lead_time": lead_time,
        "throughput": throughput,
        "yield": yield_value
    }

def apply_standardization(G):
    """
    Applies standardization transformations to manufacturing nodes only.
    
    Parameters:
        G: NetworkX directed graph
    
    Returns:
        G_standardized: New graph with standardized parameters
    """
    # Create a copy to avoid modifying the original
    G_standardized = G.copy()
    
    # Define manufacturing nodes
    manufacturing_nodes = ["Component Assembly", "Optical Calibration", "Final Testing"]
    
    # Apply EXACT transformations to manufacturing nodes only
    for node in manufacturing_nodes:
        if node in G_standardized.nodes():
            # processing_time_min × 0.8
            G_standardized.nodes[node]["processing_time_min"] *= 0.8
            
            # defect_rate × 0.7
            G_standardized.nodes[node]["defect_rate"] *= 0.7
            
            # capacity_uph × 1.1
            G_standardized.nodes[node]["capacity_uph"] *= 1.1
    
    return G_standardized

def plot_kpi_comparison(base_kpis, standardized_kpis, filename):
    """
    Creates a bar chart comparing KPIs between base and standardized cases.
    
    Parameters:
        base_kpis: Dictionary of base case KPIs
        standardized_kpis: Dictionary of standardized case KPIs
        filename: Path where the figure will be saved
    """
    # Create figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Define colors
    base_color = '#3498db'
    standardized_color = '#2ecc71'
    
    # Plot 1: Lead Time
    ax1 = axes[0]
    lead_times = [base_kpis["lead_time"], standardized_kpis["lead_time"]]
    bars1 = ax1.bar(['Base', 'Standardized'], lead_times, color=[base_color, standardized_color], edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Time (minutes)', fontsize=12, fontweight='bold')
    ax1.set_title('Lead Time', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontweight='bold')
    
    # Plot 2: Throughput
    ax2 = axes[1]
    throughputs = [base_kpis["throughput"], standardized_kpis["throughput"]]
    bars2 = ax2.bar(['Base', 'Standardized'], throughputs, color=[base_color, standardized_color], edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Units per Hour', fontsize=12, fontweight='bold')
    ax2.set_title('Throughput', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', fontweight='bold')
    
    # Plot 3: Yield
    ax3 = axes[2]
    yields = [base_kpis["yield"] * 100, standardized_kpis["yield"] * 100]  # Convert to percentage
    bars3 = ax3.bar(['Base', 'Standardized'], yields, color=[base_color, standardized_color], edgecolor='black', linewidth=1.5)
    ax3.set_ylabel('Yield (%)', fontsize=12, fontweight='bold')
    ax3.set_title('Yield', fontsize=14, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%',
                ha='center', va='bottom', fontweight='bold')
    
    # Overall title
    fig.suptitle('KPI Comparison: Base vs Standardized', fontsize=16, fontweight='bold', y=1.02)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nKPI comparison graph saved to: {filename}")
    plt.close()

def save_kpis_to_file(kpis, filename, case_name):
    """
    Saves KPI metrics to a text file.
    
    Parameters:
        kpis: Dictionary containing KPI values
        filename: Path where the metrics will be saved
        case_name: Name of the case (e.g., "Base Case")
    """
    with open(filename, 'w') as f:
        f.write("="*70 + "\n")
        f.write(f"{case_name} - KPI Metrics\n")
        f.write("="*70 + "\n\n")
        
        f.write("Key Performance Indicators:\n")
        f.write("-" * 70 + "\n")
        f.write(f"Lead Time:    {kpis['lead_time']:.2f} minutes\n")
        f.write(f"Throughput:   {kpis['throughput']:.2f} units per hour\n")
        f.write(f"Yield:        {kpis['yield']*100:.2f}%\n")
        f.write("-" * 70 + "\n")
    
    print(f"KPI metrics saved to: {filename}")

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
    print("\nThis analysis demonstrates how small process improvements")
    print("can create measurable system-level impacts in supply chains.")
    print("="*70)
    
    # Define output paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    graphs_dir = os.path.join(base_dir, 'outputs', 'graphs')
    metrics_dir = os.path.join(base_dir, 'outputs', 'metrics')
    
    # Ensure output directories exist
    os.makedirs(graphs_dir, exist_ok=True)
    os.makedirs(metrics_dir, exist_ok=True)
    
    # Step 1: Create base supply chain graph with node parameters
    print("\n[Step 1] Creating base supply chain graph with node parameters...")
    G_base = create_graph()
    print(f"Created graph with {G_base.number_of_nodes()} nodes and {G_base.number_of_edges()} edges")
    print("Node parameters added: processing_time_min, capacity_uph, defect_rate")
    
    # Step 2: Visualize base network
    print("\n[Step 2] Visualizing base supply chain network...")
    base_graph_path = os.path.join(graphs_dir, 'base_network.png')
    plot_graph(G_base, base_graph_path, "Base Supply Chain Network")
    
    # Step 3: Define the main path for KPI calculations
    print("\n[Step 3] Defining main path for KPI calculations...")
    main_path = [
        "Wafer Supplier",
        "Component Assembly",
        "Optical Calibration",
        "Final Testing",
        "Distributor",
        "OEM Customer"
    ]
    print(f"Main path: {' -> '.join(main_path)}")
    
    # Step 4: Compute base case KPIs
    print("\n[Step 4] Computing base case KPIs...")
    base_kpis = compute_kpis(G_base, main_path)
    
    # Print base case KPIs
    print("\n" + "="*70)
    print("=== BASE CASE ===")
    print("="*70)
    print(f"Lead Time:    {base_kpis['lead_time']:.2f} minutes")
    print(f"Throughput:   {base_kpis['throughput']:.2f} units per hour")
    print(f"Yield:        {base_kpis['yield']*100:.2f}%")
    print("="*70)
    
    # Save base case KPIs
    base_kpis_path = os.path.join(metrics_dir, 'base_metrics.txt')
    save_kpis_to_file(base_kpis, base_kpis_path, "Base Case")
    
    # Step 5: Apply standardization
    print("\n[Step 5] Applying standardization to manufacturing nodes...")
    G_standardized = apply_standardization(G_base)
    print("Standardization applied:")
    print("  • processing_time_min × 0.8")
    print("  • defect_rate × 0.7")
    print("  • capacity_uph × 1.1")
    
    # Step 6: Compute standardized case KPIs
    print("\n[Step 6] Computing standardized case KPIs...")
    standardized_kpis = compute_kpis(G_standardized, main_path)
    
    # Print standardized case KPIs
    print("\n" + "="*70)
    print("=== STANDARDIZED CASE ===")
    print("="*70)
    print(f"Lead Time:    {standardized_kpis['lead_time']:.2f} minutes")
    print(f"Throughput:   {standardized_kpis['throughput']:.2f} units per hour")
    print(f"Yield:        {standardized_kpis['yield']*100:.2f}%")
    print("="*70)
    
    # Save standardized case KPIs
    standardized_kpis_path = os.path.join(metrics_dir, 'standardized_metrics.txt')
    save_kpis_to_file(standardized_kpis, standardized_kpis_path, "Standardized Case")
    
    # Step 7: Calculate and print improvements
    print("\n[Step 7] Calculating improvements...")
    print("\n" + "="*70)
    print("=== IMPROVEMENTS ===")
    print("="*70)
    
    # Lead time improvement (reduction is positive)
    lead_time_improvement = ((base_kpis['lead_time'] - standardized_kpis['lead_time']) / base_kpis['lead_time']) * 100
    print(f"Lead Time Improvement:    {lead_time_improvement:.2f}% (reduced)")
    
    # Throughput improvement (increase is positive)
    throughput_improvement = ((standardized_kpis['throughput'] - base_kpis['throughput']) / base_kpis['throughput']) * 100
    print(f"Throughput Improvement:   {throughput_improvement:.2f}% (increased)")
    
    # Yield improvement (increase is positive)
    yield_improvement = ((standardized_kpis['yield'] - base_kpis['yield']) / base_kpis['yield']) * 100
    print(f"Yield Improvement:        {yield_improvement:.2f}% (increased)")
    print("="*70)
    
    # Step 8: Create KPI comparison visualization
    print("\n[Step 8] Creating KPI comparison visualization...")
    kpi_comparison_path = os.path.join(graphs_dir, 'kpi_comparison.png')
    plot_kpi_comparison(base_kpis, standardized_kpis, kpi_comparison_path)
    
    # Summary
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print("\nGenerated outputs:")
    print(f"  • {base_graph_path}")
    print(f"  • {base_kpis_path}")
    print(f"  • {standardized_kpis_path}")
    print(f"  • {kpi_comparison_path}")
    print("\nKey Findings:")
    print("  • Small process improvements create measurable system-level impact")
    print("  • Standardization reduces lead time and defects")
    print("  • Increased capacity improves throughput")
    print("  • Overall yield improvement demonstrates supply chain optimization")
    print("="*70 + "\n")

# Run the analysis
if __name__ == "__main__":
    main()
