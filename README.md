Subdomain Bruteforce Tool

A simple Python script to brute-force subdomains for a given base domain using a wordlist.

Installation:
    # Clone the repository
    git clone https://github.com/clarkvoss/SubDomain-BruteForcer.git
    cd subdomain-bruteforce

    # (Optional) Create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\\Scripts\\activate

    # Install dependencies (standard library only)
    # If you add dependencies later, list them in requirements.txt and run:
    # pip install -r requirements.txt

Usage:
    # Run with prompts
    python3 subdomain_bruteforce.py

    # Or use command-line arguments
    python3 subdomain_bruteforce.py \
        --domain example.com \
        --wordlist ~/lists/wordlist.txt \
        --threads 20 \
        --output found_subdomains.txt

    # The script will resolve each subdomain in parallel and optionally save results to a file.
