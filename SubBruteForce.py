import socket
import sys
import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed


def parse_args():
    parser = argparse.ArgumentParser(description="Brute force subdomains for a given domain")
    parser.add_argument("-d", "--domain", help="Base domain (e.g., example.com)")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist file")
    parser.add_argument("-o", "--output", help="Output file to save found subdomains")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    return parser.parse_args()


def load_wordlist(path):
    # Read with UTF-8, fallback to Latin-1
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='latin-1') as f:
            lines = f.read().splitlines()
    return [line.strip() for line in lines if line.strip()]


def resolve_subdomain(word, base_domain):
    cleaned = word.strip().strip('.')
    if not cleaned:
        return None
    subdomain = f"{cleaned}.{base_domain}"
    if len(subdomain) > 253:
        return None
    labels = subdomain.split('.')
    if any(len(label) > 63 for label in labels):
        return None
    try:
        ip = socket.gethostbyname(subdomain)
        return subdomain, ip
    except (socket.gaierror, UnicodeError):
        return None


def main():
    args = parse_args()

    # Base domain input
    if args.domain:
        base_domain = args.domain.strip().strip('"').strip("'")
    else:
        base_domain = input("Enter the base domain (e.g., example.com): ").strip()

    # Wordlist path input
    if args.wordlist:
        wordlist_path = args.wordlist.strip().strip('"').strip("'")
    else:
        wordlist_path = input("Enter the path to the wordlist file: ").strip()
    wordlist_path = os.path.expanduser(wordlist_path)

    if not os.path.isfile(wordlist_path):
        print(f"Error: File not found: {wordlist_path}")
        sys.exit(1)

    words = load_wordlist(wordlist_path)
    print(f"Starting brute force of subdomains for: {base_domain} with {len(words)} entries using {args.threads} threads\n")

    results = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(resolve_subdomain, w, base_domain): w for w in words}
        for future in as_completed(futures):
            res = future.result()
            if res:
                sub, ip = res
                print(f"[+] Found: {sub} -> {ip}")
                results.append(f"{sub} -> {ip}")

    if args.output:
        try:
            with open(args.output, 'w') as f:
                for line in results:
                    f.write(line + "\n")
            print(f"\nResults saved to {args.output}")
        except Exception as e:
            print(f"Error writing to output file: {e}")


if __name__ == "__main__":
    main()
    
