#!/usr/bin/env bash
echo "cleaning recordings, checkpoints and notable_genomes"
echo "This might take a while..."
super-intelligent-mario/results/recordings/clean.sh
echo "Done, exit code=$?"
super-intelligent-mario/results/checkpoints/clean.sh
echo "Done exit code=$?"
super-intelligent-mario/results/notable_genomes/clean.sh
echo "Done exit code=$?"
