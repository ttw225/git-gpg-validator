import argparse


def main(args: argparse.Namespace) -> bool:
    if args.method == "simple":
        # Compare Fingerprint
        pass
    else:
        # Sign and Verify
        pass
    return True


if __name__ == "__main__":
    PARSER: argparse.ArgumentParser = argparse.ArgumentParser(description="GPG Key Validator")
    PARSER.add_argument(
        "-m",
        "--method",
        type=str,
        choices=["simple", "hard"],
        default="simple",
        help="simple: compare fingerprint; hard: sign and verify",
    )
    PARSER.add_argument("-k", "--key", type=str, help="Use default key or set a Key ID for signing")
    ARGS: argparse.Namespace = PARSER.parse_args()
    main(ARGS)
