def recommend_word(words):
    frequency = {}
    for number in range(0,5):
        frequency[number] = {}
        for alphabet in "abcdefghijklmnopqrstuvwxyz":
            frequency[number][alphabet] = 0

    for word in words:
        for letter in range(5):
            frequency[letter][word[letter]] = frequency[letter][word[letter]] + 1

    result = {}
    for word in words:
        n = 0
        duplicates = False
        for letter in range(5):
            if word.count(word[letter]) > 1:
                duplicates = True
            n = n + frequency[letter][word[letter]]
        if duplicates == True:
            result[word] = n * 0.5
        elif duplicates == False:
            result[word] = n

    recommended_word = sorted(result.items(), key=lambda item: item[1], reverse=True)[0][0]
    recommended_word = "Play: " + str(recommended_word).upper()
    return(recommended_word)

def drop_words(letters,words):
    new_words = []
    for word in words:
        matching = False
        for letter in letters:
            if letter in word:
                matching = True
        if matching == False:
            new_words.append(word)
    return(new_words)

def green_words(position,letter,words):
    new_words = []
    for word in words:
        if word[int(position)] == letter:
            new_words.append(word)
    return(new_words)

def amber_words(position,letter,words):
    new_words = []
    for word in words:
        if word[int(position)] == letter:
            continue
        elif letter in word:
            new_words.append(word)
        else:
            continue
    return(new_words)

def chance(words):
    return("Chance: " + str(100/len(words)) + "%")

if __name__ == "__main__":

    with open('wordlist.txt') as file:
        words = file.readlines()
        words = [word.rstrip() for word in words]
    
    print(recommend_word(words))
    print(chance(words))

    bad_letters = ""

    for n in range(0,5):
        print("Enter bad letters:")
        print(bad_letters, end="")
        bad_letters = bad_letters + str(input())
        words = drop_words(bad_letters,words)
        print(chance(words))


        print("Enter new green letters and a position like a0s4. Or press enter to skip.")
        green_input = str(input())
        if green_input != "":
            for n in range(int(len(green_input)/2)):
                words = green_words(green_input[1+ 2*n], green_input[0 + 2*n], words)
        print(chance(words))

        print("Enter new amber letters and a position like a0s4. Or press enter to skip.")
        amber_input = str(input())
        if amber_input != "":
            for n in range(int(len(amber_input)/2)):
                words = amber_words(amber_input[1+ 2*n], amber_input[0 + 2*n], words)
        print(chance(words))

        print(recommend_word(words))
    
    print(words)
