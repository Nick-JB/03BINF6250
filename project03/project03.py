import random
import numpy as np
import bamnostic as bs
import seqlogo as sl

#Import function for building sequence motif & identifying seqs matching to motif
from data_readers import get_fasta, get_gff
from seq_ops import get_seq
from motif_ops import build_pfm, build_pwm, score_kmer, pfm_ic

bam_path = "data/SRR9090854.subsampled_5pct.bam"

seqs = [read.seq for read in bs.AlignmentFile(bam_path)]

# --- DATA PREPARATION CELL ---

# Define paths
fasta_file = "data/GCF_000009045.1_ASM904v1_genomic.fna"
gff_file = "data/GCF_000009045.1_ASM904v1_genomic.gff"

# Extract the chromosome sequence
header, genome_seq = next(get_fasta(fasta_file))

# extract the 50bp promoter sequences for every gene
seqs = []
for entry in get_gff(gff_file):
    if entry.type == 'gene':
        # get_seq comes from your seq_ops.py module
        promoter = get_seq(genome_seq, entry.start, entry.end, entry.strand, size=50)

        #only add if we got a valid 50bp sequence
        if promoter and len(promoter) == 50:
            seqs.append(promoter)

print(f"Successfully loaded {len(seqs)} sequences into the 'seqs' variable.")

def GibbsMotifFinder (seqs, k, seed=42):
    '''
    Function to find a pfm from a list of strings using a Gibbs sampler

    Args:
        seqs (str list): a list of sequences, not necessarily in same lengths
        k (int): the length of motif to find
        seed (int, default=None): seed for np.random

    Returns:
        pfm (numpy array): dimensions are 4xlength
    '''
    # Use rng to make random samples/selections/numbers
    # Example: randint = rng.integer(1, 10)

    # random.seed(seed)
    # rng = np.random.default_rng(seed)

    rng = np.random.default_rng(seed)
    n_seqs = len(seqs)

    # Initialization: picking random start positions
    current_indices = [rng.integers(0, len(s) - k + 1) for s in seqs]

    best_pfm = None
    max_ic = -float('inf')

    # Main Loop: Run for a set number of iterations
    for _ in range(100): 
        # pick a random sequence to leave out
        i = rng.integers(0, n_seqs)

        # build model from all other sequences
        other_kmers = []
        for idx, s in enumerate(seqs):
            if idx != i:
                start = current_indices[idx]
                other_kmers.append(s[start : start + k])

        pfm = build_pfm(other_kmers, k)
        pwm = build_pwm(pfm)

        # Score & Sample for the left-out sequence
        seq_i = seqs[i]
        weights = []
        for j in range(len(seq_i) - k + 1):
            kmer = seq_i[j : j + k]
            score = score_kmer(kmer, pwm)
            weights.append(2.0 ** score) # Convert log2 score back to weight

        # Normalize weights into probabilities
        weights = np.array(weights)
        probs = weights / weights.sum()

        # Choose new index based on probability distribution
        current_indices[i] = rng.choice(len(probs), p=probs)

        # Evaluate
        all_kmers = [seqs[idx][pos : pos + k] for idx, pos in enumerate(current_indices)]
        current_pfm = build_pfm(all_kmers, k)
        current_ic = pfm_ic(current_pfm)

        if current_ic > max_ic:
            max_ic = current_ic
            best_pfm = current_pfm

    return best_pfm

    pass

# Run the gibbs sampler:
promoter_pfm = GibbsMotifFinder(seqs,10 )

# Plot the final pfm that is generated

# Create the logo data
logo_data = sl.CompletePm(pfm=promoter_pfm.T)

# Save the logo to a file instead of trying to display it
sl.seqlogo(logo_data, filename='motif_results.pdf', format='pdf')

print("Success! Your motif logo has been saved as 'motif_results.pdf'")

