from playwright.sync_api import sync_playwright, expect
import re
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
    return(str(recommended_word).upper())

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
    chance = 100/len(words)
    print("Chance: " + str(chance) + "%")
    if chance > 5:
        print(words)

def attempt_wordle(attempt):
    grey = []
    amber = []
    green = []
    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page()
        page.goto("https://www.nytimes.com/games/wordle/index.html")
        page.click("#pz-gdpr-btn-accept")
        page.click("#game")
        for letter in attempt:
            page.press('#game', letter)
        page.press("#game", "Enter")
        locator = page.locator('[data-key="' + attempt[0] + '"]')
        expect(locator).to_have_attribute("data-state",re.compile(r"^(?:absent|present|correct)$"))

        for letter in attempt:
            locator = page.locator('[data-key="' + letter + '"]')
            if locator.get_attribute("data-state") == "absent":
                grey.append(letter)
            elif locator.get_attribute("data-state") == "present":
                amber.append(letter)
            elif locator.get_attribute("data-state") == "correct":
                green.append(letter)
        browser.close()
    return(grey,amber,green)



if __name__ == "__main__":

    with open('wordlist.txt') as file:
        words = file.readlines()
        words = [word.rstrip() for word in words]
    
    recommended_word = recommend_word(words)
    grey,amber,green = attempt_wordle(recommend_word(words).lower())
    # print(recommended_word)
    # print(chance(words))

    bad_letters = []

    for n in range(0,5):
        if len(green) == 5:
            break
        bad_letters += grey
        words = drop_words(bad_letters,words)

        for m in range(0,4):
            if recommended_word[m].lower() in green:
                words = green_words(m,recommended_word[m].lower(),words)
            elif recommended_word[m].lower() in amber:
                words = amber_words(m,recommended_word[m].lower(),words)

        recommended_word = recommend_word(words)
        # print(recommended_word)
        # print(chance(words))
        grey,amber,green = attempt_wordle(recommend_word(words).lower())
    
    print("Victory in " + str(n + 1) + " turns!")