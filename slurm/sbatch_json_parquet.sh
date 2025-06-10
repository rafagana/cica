#!/bin/bash
#SBATCH --job-name=json_parquet   # Job name
#SBATCH --output=/home/LQL3227/phd/data-engineering/slurm/json_parquet-%j.out  # Output file
#SBATCH --error=/home/LQL3227/phd/data-engineering/slurm/json_parquet-%j.err   # Error file
#SBATCH --nodes=1                   # Number of nodes
#SBATCH --ntasks=1                  # Number of tasks (1 CPU)
#SBATCH --cpus-per-task=1           # Number of CPU cores per task
#SBATCH --mem=64G                   # Memory allocation (64GB)
#SBATCH --time=72:00:00             # Maximum runtime (3 days)

# Load system-wide environment variables
source /etc/profile

# Activate the Python virtual environment
source /home/LQL3227/phd/bin/activate

# Navigate to the directory containing the Python script
cd /home/LQL3227/phd/data-engineering

# Run the Python script
python3 json_flatenning_parquet_cica.py

# Deactivate the virtual environment (optional, but good practice)
deactivate

echo "Slurm job finished!"