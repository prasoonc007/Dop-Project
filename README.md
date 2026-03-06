# Optoelectronics Supply Chain Network Analysis

## Project Objective

This academic prototype project demonstrates how **small localized inefficiencies** in a supply chain can create **larger system-level impacts** using graph theory and network analysis.

The central research question is:

> **Can small disruptions at structurally important nodes significantly affect the overall performance of a supply chain?**

## Overview

This project models an optoelectronics supply chain as a **directed graph** where:

- **Nodes** represent supply chain entities (suppliers, manufacturing stages, distributors, customers)
- **Edges** represent material flow and process dependencies

By analyzing the network structure and simulating disruptions, we can identify bottlenecks and understand how localized failures propagate through the system.

## Graph Theory Modeling Approach

### Network Structure

The supply chain is modeled as a directed graph with the following components:

#### Suppliers (Upstream)
- Wafer Supplier
- Lens Supplier
- PCB Supplier
- Packaging Supplier

#### Manufacturing Stages (Middle)
- Component Assembly
- Optical Calibration
- Final Testing

#### Downstream Entities
- Distributor
- OEM Customer

### Material Flow

The edges represent the flow of materials and dependencies:

```
Suppliers → Component Assembly → Optical Calibration → Final Testing → Distributor → OEM Customer
```

### Metrics Analyzed

The project computes the following structural metrics:

1. **In-Degree**: Number of incoming connections (dependencies)
2. **Out-Degree**: Number of outgoing connections (downstream impact)
3. **Betweenness Centrality**: Measures how often a node appears on shortest paths (identifies bottlenecks)
4. **Average Shortest Path Length**: Overall network efficiency

## What This Prototype Demonstrates

This project demonstrates:

1. **Structural Vulnerability**: How certain nodes (like "Optical Calibration") are critical bottlenecks
2. **Cascading Effects**: How removing one node can disconnect the entire downstream supply chain
3. **System-Level Impact**: How localized disruptions affect overall network connectivity and efficiency
4. **Quantitative Analysis**: Measurable changes in network metrics before and after disruption

### Key Findings

The simulation shows that removing the **Optical Calibration** manufacturing stage:

- Disconnects the entire downstream supply chain
- Eliminates all paths from suppliers to customers
- Demonstrates the critical importance of manufacturing bottlenecks
- Proves that small localized disruptions can have disproportionate system-level impacts

## Project Structure

```
supply_chain_graph_project/
│
├── data/                          # Reserved for future datasets
│
├── scripts/
│   └── supply_chain_model.py     # Main Python script
│
├── outputs/
│   ├── graphs/                    # Network visualizations
│   │   ├── base_supply_chain_network.png
│   │   └── disrupted_supply_chain_network.png
│   │
│   └── metrics/                   # Computed metrics
│       ├── base_case_metrics.txt
│       └── disruption_comparison.txt
│
└── README.md                      # This file
```

## Requirements

This project requires the following Python libraries:

- `networkx` - For graph creation and analysis
- `matplotlib` - For network visualization

Install dependencies using:

```bash
pip install networkx matplotlib
```

## How to Run

Execute the analysis by running:

```bash
python scripts/supply_chain_model.py
```

The script will automatically:

1. Create the base supply chain graph
2. Visualize the network structure
3. Compute structural metrics
4. Simulate a disruption (remove "Optical Calibration" node)
5. Visualize the disrupted network
6. Compare base case vs. disrupted case metrics
7. Save all outputs to the `outputs/` directory

## Outputs

After running the script, the following files will be generated:

### Visualizations

- **`outputs/graphs/base_supply_chain_network.png`**  
  Shows the complete supply chain network with all nodes and connections

- **`outputs/graphs/disrupted_supply_chain_network.png`**  
  Shows the network after removing the "Optical Calibration" node

### Metrics

- **`outputs/metrics/base_case_metrics.txt`**  
  Contains node-level and network-level metrics for the base case

- **`outputs/metrics/disruption_comparison.txt`**  
  Compares base case and disrupted case, highlighting changes

## Academic Applications

These outputs can be used in academic reports to:

- Illustrate supply chain structure and dependencies
- Identify critical bottlenecks using centrality metrics
- Demonstrate the impact of localized disruptions
- Support arguments about supply chain resilience and risk management
- Provide quantitative evidence for system-level vulnerability

## Methodology

The analysis follows these steps:

1. **Graph Construction**: Build a directed graph representing the supply chain
2. **Baseline Analysis**: Compute metrics for the intact network
3. **Disruption Simulation**: Remove a critical node (Optical Calibration)
4. **Impact Assessment**: Recompute metrics and compare results
5. **Visualization**: Create publication-quality network diagrams
6. **Interpretation**: Analyze how the disruption affects system performance

## Limitations and Future Work

This is a simplified prototype model. Future enhancements could include:

- Multiple disruption scenarios
- Weighted edges representing capacity or cost
- Time-series simulation of disruption propagation
- Recovery strategies and resilience analysis
- Real-world data integration
- Stochastic disruption modeling

## Conclusion

This project successfully demonstrates that **small localized disruptions at structurally important nodes can significantly affect overall supply chain performance**. The graph-based approach provides a clear, quantitative framework for understanding supply chain vulnerabilities and the cascading effects of disruptions.

---

**Author**: Academic Prototype Project  
**Purpose**: Educational demonstration of graph theory in supply chain analysis  
**License**: Open for academic use
