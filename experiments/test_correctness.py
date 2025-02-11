import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load metric functions

from utils.metric_fns import *

metric_fn_dict = {
    "logit": metric_fn_logit,
    "KL": metric_fn_KL,
    "accuracy": metric_fn_acc,
    "MRR": metric_fn_MRR,
}

# Load the model and its dictionaries

from utils.experiments_setup import load_model_and_modules, load_saes

print("Loading model and modules...", end="")
pythia70m, pythia70m_embed, pythia70m_resids, pythia70m_attns, pythia70m_mlps, submod_names = load_model_and_modules(device=device)
print("Done.")

print("Loading SAEs...", end="")
dictionaries = load_saes(
    pythia70m,
    pythia70m_embed,
    pythia70m_resids,
    pythia70m_attns,
    pythia70m_mlps,
    device=device,
)
print("Done.")

# define a toy input

clean = "When Mary and John went to the store, John gave a drink to"
trg_idx = torch.tensor([-1]).to(device)
trg_str = " Mary"
trg = torch.tensor([pythia70m.tokenizer.encode(trg_str)[0]], device=device)

print("clean:", clean)
print("trg_str:", trg_str)
print("trg:", trg)
print("trg_idx:", trg_idx)

# get the circuit

from circuit.circuit import get_circuit

print("Getting circuit...")
circuit = get_circuit(
    clean,
    None,
    model=pythia70m,
    embed=pythia70m_embed,
    resids=pythia70m_resids,
    dictionaries=dictionaries,
    metric_fn=metric_fn_logit,
    metric_kwargs={"trg": (trg_idx, trg)},
    edge_threshold=0.01,
)
print("Done.")

# evaluate the circuit

# start at layer : starting from the embedding layer can be surprisingly bad in some cases, so starting a little bit after might help.

start_at_layer = 1

submodules = [pythia70m_embed] if start_at_layer == -1 else []
for i in range(max(start_at_layer, 0), len(pythia70m.gpt_neox.layers)):
    submodules.append(pythia70m_resids[i])

from evaluation.faithfulness import faithfulness

print("Evaluating faithfulness...")
thresholds = torch.logspace(-2, 2, 15, 10).tolist()
faith = faithfulness(
    pythia70m,
    submodules=submodules,
    sae_dict=dictionaries,
    name_dict=submod_names,
    clean=clean,
    circuit=circuit,
    thresholds=thresholds,
    metric_fn=metric_fn_dict,
    metric_fn_kwargs={"trg": (trg_idx, trg)},
    patch=None,
    default_ablation='zero',
    get_graph_info=True,
)
print("Done.")

# Plot the results :

from utils.plotting import plot_faithfulness

save_path = "/scratch/pyllm/dhimoila/test_correctness/" + str(start_at_layer) + "/"
plot_faithfulness(faith, metric_fn_dict, save_path)