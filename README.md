# Scale-Free Blockchain Project

## Overview
This repository contains an approach to blockchain technology, incorporating scale-free network properties to investigate their effects on performance. By integrating the Barabasi-Albert model, known for its scale-free network characteristics, we examine how the topology of network connections influences blockchain efficiency, specifically focusing on throughput and latency.

## Features
- **Simple Blockchain Implementation**: A basic blockchain structure to serve as a control group in performance analysis.
- **Scale-Free Blockchain**: An enhanced blockchain model that incorporates scale-free network properties based on the Barabási-Albert model.
- **Performance Analysis**: Comparative metrics between the simple and scale-free blockchain implementations, focusing on throughput and latency.

## Performance Comparison
We compared the Simple Blockchain and Scale-Free Blockchain on two key performance metrics: throughput (transactions per second) and latency (seconds per transaction).

### Results
  ![performance](https://github.com/MohsinRasheed9112/Integrating-Scale-Free-Networks-into-Blockchain/assets/101352612/c0d4be3d-d26e-4064-b250-50e72817e253)

- **Simple Blockchain**
  - Throughput: `234.76 tx/s`
  - Latency: `0.004260 s/tx`
- **Scale-Free Blockchain**
  - Throughput: `284.95 tx/s`
  - Latency: `0.003509 s/tx`

Scale-Free Blockchain demonstrates superior performance with higher throughput and lower latency, indicating its efficiency and responsiveness in processing transactions.

## Getting Started
To run this project, ensure you have Python 3.x installed on your machine.
