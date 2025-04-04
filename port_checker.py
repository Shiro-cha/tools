#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import argparse
import logging
from datetime import datetime
import sys

def check_port(host, port, timeout=5):
    """Check if a port is open on a given host."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0
    except Exception as e:
        logging.error("Connection error: %s" % str(e))
        return False

def setup_logging():
    """Configure logging system."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('port_checker.log'),
            logging.StreamHandler()
        ]
    )

def print_usage_and_exit(parser):
    """Print usage help and exit."""
    parser.print_help()
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Port Checker Tool')
    parser.add_argument('host', nargs='?', help='IP address or hostname')
    parser.add_argument('port', nargs='?', type=int, help='Port number to check')
    parser.add_argument('--timeout', type=float, default=5, help='Timeout in seconds')
    
    if len(sys.argv) == 1:  # No arguments provided
        print_usage_and_exit(parser)
    
    args = parser.parse_args()
    
    if not args.host or not args.port:  # Missing required arguments
        print_usage_and_exit(parser)
    
    setup_logging()
    
    start_time = datetime.now()
    status = check_port(args.host, args.port, args.timeout)
    end_time = datetime.now()
    
    # Manual calculation for Python 2.6
    delta = end_time - start_time
    elapsed = (delta.days * 86400 + delta.seconds) + delta.microseconds / 1e6
    
    if status:
        logging.info("[SUCCESS] Port %d OPEN on %s (time: %.2fs)" % (args.port, args.host, elapsed))
    else:
        logging.error("[FAILURE] Port %d CLOSED/UNREACHABLE on %s (time: %.2fs)" % (args.port, args.host, elapsed))

if __name__ == "__main__":
    main()