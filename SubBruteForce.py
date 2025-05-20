#!/usr/bin/env python3
import socket
import sys
import os


def main():
    # Prompt for the base domain and wordlist path
    base_domain = input("Enter the base domain (e.g., example.com): ")
    base_domain = base_domain.strip().strip('"').strip("'")

    wordlist_path = input("Enter the path to the wordlist file: ")
    # Remove surrounding quotes and expand user tilde
    wordlist_path = wordlist_path.strip().strip('"').strip("'")
    wordlist_path = os.path.expanduser(wordlist_path)

    # Validate the file exists
    if not os.path.isfile(wordlist_path):
        print(f"Error: File not found: {wordlist_path}")
        sys.exit(1)

    # Read the wordlist with fallback encoding
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
    except UnicodeDecodeError:
        try:
            with open(wordlist_path, 'r', encoding='latin-1') as f:
                lines = f.read().splitlines()
        except Exception as e:
            print(f"Error reading wordlist file with fallback encoding: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"Error reading wordlist file: {e}")
        sys.exit(1)

    # Strip and filter empty lines
    words = [line.strip() for line in lines if line.strip()]

    print(f"Starting brute force of subdomains for: {base_domain}\n")

    # Iterate and attempt DNS resolution
    for word in words:
        # Clean up the word to avoid empty labels
        cleaned = word.strip().strip('.')
        if not cleaned:
            continue

        subdomain = f"{cleaned}.{base_domain}"

        # Skip subdomains that exceed DNS length limits
        if len(subdomain) > 253:
            continue
        labels = subdomain.split('.')
        if any(len(label) > 63 for label in labels):
            continue

        try:
            # Attempt DNS resolution, catching Unicode/domain errors
            ip = socket.gethostbyname(subdomain)
            print(f"[+] Found: {subdomain} -> {ip}")
        except (socket.gaierror, UnicodeError):
            # Skip non-existent or invalid subdomains
            continue


if __name__ == "__main__":
    main()
