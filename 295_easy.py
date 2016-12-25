def main():
    words = [input('First word: '), input('Second word: ')]
    for i in range(len(words[0])+1):
        print(words[1][0:i] + words[0][i:])


if __name__ == '__main__':
    main()
