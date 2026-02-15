# Introduction
Description of the project

# Pseudocode
Put pseudocode in this box:

```
1. Initizalize random number generator

2. Randomly initialize one motif occurence per sequence
- for each sequence, choose a random start position

```

# Successes
Description of the team's learning points

# Struggles
Handling large datasets and determing how to approach testing and building model
Understanding data transformations
Seqlogo dependencies
Installing MACS2
Formatting data after peak calling

This assignment came with many new hurdles that we had not previously had much experience with. The major one being handling large datasets. It became apparent very quickly that it was not feasible to test and build our model if we were to run it on the full dataset every time that we wanted to check how it was behaving. To overcome this, we took a subset of the main dataset, so that we could see how the model would behave in a more reasonable amount of time. Part of building the model was also keeping track of the state of data and what transformations it had undergone in case those transformations had to be reversed, which was the case when converting the pwm-derived scores into weights for determining a new motif to use in the pfm. Once we had a functioning algorithm, we still faced the challenge of how to handle such a large dataset, much of which contained duplicative information. This is where we were introduced to the method of peak calling. Peak calling tools are very useful for this exact purpose because they can simplify broad sets of genomic data into just the regions with the most coverage. There were some difficulties getting MACS2 installed, but it was successfully installed and run after some troubleshooting. It was at this point that we encountered our last major hurdle, trying to get good peaks which would contain the p53 binding sites we were looking for without being overly broad, as that would defeat the purpose of finding the peaks. An unforseen issue that came with this peak calling was AT rich regions around the peaks, which would lead the model to converge to a strong A or T bias, clearly not reflecting the motif that we were searching for. Outside of the computational realm, we also faced issues with properly installing and enabling dependencies for the seqlogo package, with most errors seeming to arise from problems with ghostscript permissions and fonts that are required for creation of a sequence logo.

# Personal Reflections
## Group Leader
Group leader's reflection on the project

## Other member
Other members' reflections on the project

# Generative AI Appendix
As per the syllabus
