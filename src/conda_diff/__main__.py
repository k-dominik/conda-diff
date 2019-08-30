import sh


def main():
    print(sh.conda("--version"))


if __name__ == "__main__":
    main()
