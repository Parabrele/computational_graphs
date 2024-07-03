# Computational Graphs

This project contains functions to build and run computational graphs that abstract a language model into disantangled atomic components.

## Ablation

The `ablation` directory contains functions to run computational graph in stead of the original model.

- **Node ablation** sets all nodes to some reference value, using mean ablation, zero ablation, or any function you might give it, except for the specified nodes. The computational graph is then effectively the complete graph between these nodes.

- **Edge ablation** runs the actual specified graph. It is slower than its simpler counterpart as now, each node is computed individually with a different input. The number of forward passes through the model is effectively very high. There might be some room for optimization here.

## Circuit

The `circuit` directory contains functions to build the computational graph on some input, based on given feature dictionaries. The graph is built using integrated gradient to approximate the causal effect of each feature on its successors.

## Data

The `data` directory contains functions to load and preprocess data to be used in the experiments.

## Evaluation

The `evaluation` directory contains functions to evaluate the performance of the computational graph. It measures it's faithfulness to the original model given some metric function, as well as some basic graph properties, like the number of nodes and edges.

## Experiments

The `experiments` directory contains tests and experiments you can run

We ran experiments using pythia-70m-deduped and the dictionaries provided by Marks et al. The code is compatible with any other nnsight LanguageModel and any dictionaries so long as they contain at least a `forward`, an `encode`, and a `decode` method.

## Utils

This directory contains utility functions that are used in the other directories.

Please note that a minimal implementation of MLP and linear dictionaries is provided. You can use your own instead so long as it has `forward`, `encode`, and `decode` methods.

# Installation

Some requirements are provided in the `requirements.txt` file. It might not be up to date.

# Usage

A minimal example is provided in `experiments/test_correctness.py`. You can run it with `python -m experiments.test_correctness`.

Please note that in this example, I load model and dictionaries using some utility functions that are specific to my machine. You will need to modify this file to load your own dictionaries.

### TODOs

- aggregation function to aggregate graphs across examples.
- data : only wikipedia is currently supported, add task specific datasets.