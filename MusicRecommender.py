import os

def enter_preferences(username, file):
    '''takes in a string, username, and a file, file
    uses user input to append the username to the file,
    followed by the list of preferences inputted by user
    until an empty string is inputted.
    '''

    file.seek(0)
    lines = file.readlines()
    
    preferences = []
    while True:
        preference = input("Enter an artist that you like ( Enter to finish ): ")
        if preference == '':
            break
        if preference.title() not in preferences:
            preferences.append(preference.title())
    preferences.sort()

    updated = False
    for i, line in enumerate(lines):
        if line.startswith(username + ":"):
            lines[i] = (f"{username}:{','.join(preferences)}\n")
            updated = True
            break

    if not updated:
        lines.append(f"{username}:{','.join(preferences)}\n")

    new_lines = sorted(lines)
    file.seek(0)
    file.truncate()
    file.writelines(new_lines)


def get_recommendations(username, file):
    '''takes in a string, username, and a file, file
    creates a dictionary for user data and loops through file to fill it
    sets variable user_artists to the value of the key
    in the dictionary matching username
    checks all other items in the dictionary
    to find the one with the greatest overlap
    returns a list of said recommendations properly formatted
    checks for if there's only one user in the dictionary, 
    meaning recommendations cannot be made
    and returns an error message in that case.
    '''

    file.seek(0)
    lines = file.readlines()

    user_data = {}
    for line in lines:
        (name, artists) = line.strip().split(":")
        user_data[name] = set(artists.split(","))

    public_users = [name for name in user_data if not name.endswith("$")]
    if len(public_users) <= 1:
        return "Only one user, no recommendations available at this time."

    user_artists = user_data.get(username, set())

    best_match = None
    max_overlap = 0

    for other_user, other_artists in user_data.items():
        if other_user == username or other_user.endswith("$"):
            continue

        common_artists = user_artists & other_artists
        unique_recommendations = other_artists - user_artists

        if not unique_recommendations:
            continue

        if len(common_artists) > max_overlap:
            best_match = unique_recommendations
            max_overlap = len(common_artists)

    if best_match:
        return "\n".join(sorted(best_match))
    else:
        return "No recommendations available at this time."


def mostPop(file):
    '''takes in a file, file
    creates a dictionary that stores the names of the artists in file
    if not already in the dictionary, creates an entry
    the "Key" is the artist name and the "Value" is the number of times it appears
    prints the 3 most popular artists in the file
    '''

    file.seek(0)
    newC = {}
    content = (" ".join(file.readlines())).split("\n")
    for line in content:
        artists = line.split(":")[-1].split(",")
        for artist in artists:
            if artist in newC:
                newC[artist] += 1
            elif artist:
                newC[artist] = 1
    print("The most popular artist, in ranked order, are: \n" +
          "\n".join(sorted(newC, key=newC.get, reverse=True)[:3]))


def mostPopNum(file):
    '''takes in a file, file
    creates a dictionary that stores the names of the artist in the file
    if it is not already in the dictionary it will create the entry
    the "Key" is the artist name and the "Value" is the number of times it appears
    prints the number of times the most popular artist appears in the file
    '''

    file.seek(0)
    newC = {}
    content = (" ".join(file.readlines())).split("\n")
    for line in content:
        artists = line.split(":")[-1].split(",")
        for artist in artists:
            if artist in newC:
                newC[artist] += 1
            elif artist:
                newC[artist] = 1
    print("The most popular artist appears " + str(newC[max(newC, key=newC.get)]) + " times")


def mostLiked(file):
    '''creates an empty list, and helper list
    takes in a file, file
    goes through the each line in the file
    the username of the largest line is recorded and printed
    '''
    
    file.seek(0)
    list = []
    helper = []
    content = (" ".join(file.readlines())).split("\n")
    for line in content:
        user_data = ", ".join(line.split(":")).split(",")
        list.append(user_data)
    for user_data in list:
        if len(helper) < len(user_data):
            helper = user_data
    print("The user with the most liked artists is " + helper[0])


def saveQuit():
    '''ends the loop of the menu by setting the global variable,
    use, to be False while printing an exit message
    saving to the file is done in other files that modify it
    '''
    
    global use
    print("Exiting program")
    use = False

def main():
    '''checks if the text file musicrecplus.txt exists,
    creating one if it does not,
    then iterates through the file to create a list of usernames
    then asks for an input, username, which is checked against the list
    if username is in usernames, opens the menu for other functions
    if not, prompts the enter_preferences function for a first time user
    also checks if a user is in private mode
    '''

    try:
        open("musicrecplus.txt", "r").close()
    except FileNotFoundError:
        open("musicrecplus.txt", "w").close()
    
    with open("musicrecplus.txt", "r+") as file:
        file.seek(0)
        usernames = [line.split(':')[0] for line in file.readlines()]
        username = input(
            "Enter your name (add $ for your preferences to remain private: ")
        
        if username not in usernames:
            enter_preferences(username, file)

        global use
        use = True
        
        while use:
            file.seek(0)
            print(
                "Enter a letter to choose an option: \n"
                "e - Enter preferences \n"
                "r - Get recommendations \n"
                "p - Show most popular artists \n"
                "h - How popular is the most popular \n"
                "m - Which user has the most likes \n"
                "q - Save and quit"
            )

            choices = ["e", "r", "p", "h", "m", "q"]
            choice = input("Enter a letter to choose an option: ")
            while choice not in choices:
                print("Invalid input, try again")
                choice = input("Enter a letter to choose an option: ")
                
            if choice == "e":
                enter_preferences(username, file)
            if choice == "r":
                print(get_recommendations(username, file))
            if choice == "p":
                mostPop(file)
            if choice == "h":
                mostPopNum(file)
            if choice == "m":
                mostLiked(file)
            if choice == "q":
                saveQuit()

if __name__ == "__main__":
    main()
