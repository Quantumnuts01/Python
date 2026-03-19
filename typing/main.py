import typer_trainer

def main():
    stop = False
    while not stop:
        print("""1) Train easy
2) Train medium
3) Train Hard
4) View scores
q) Quit""")

        choice = input("--> ")

        if choice == "q":
            print("Bye, bye!")
            stop = True

        elif choice == "1":
            typer_trainer.train_typing_words_from_file("texts/easy.txt","easy")
        elif choice == "2":
            typer_trainer.train_typing_words_from_file("texts/medium.txt","medium")
        elif choice == "3":
            typer_trainer.train_typing_words_from_file("texts/hard.txt","hard")
        elif choice == "4":
            typer_trainer.read_scores("scores.txt")

        if not stop:
            input("\nPress enter to continue...")


if __name__ =="__main__":
    main()
