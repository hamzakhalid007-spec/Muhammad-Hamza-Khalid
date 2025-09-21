# 1-import random module
import random as rand

# 2-create subjects, actions and places/things
fake_news_data = {
    "politics": {
        "subjects": {
            "Indian": ["A politician", "The Prime Minister", "A cabinet minister", "An opposition leader"],
            "Pakistani": ["A political leader", "The PM", "A senior politician", "A party chief"]
        },
        "actions": ["declares pizza as national currency", "bans gravity on Tuesdays", "announces marriage to", "starts a dance-off with", 
                   "challenges to a cooking contest", "appoints their pet parrot as", "declares themselves emperor of", "orders everyone to wear pajamas in"],
        "places": ["on Mars", "inside a giant teacup", "at the International Space Station", "during a bollywood dance number",
                  "while riding a unicorn", "in a parallel universe", "at a secret underground disco", "on top of Mount Everest"]
    },
    "sports": {
        "subjects": {
            "Indian": ["A cricket player", "An Olympic athlete", "A football star", "A tennis champion"],
            "Pakistani": ["A sports hero", "An international player", "A cricket legend", "A world champion"]
        },
        "actions": ["scores 500 runs using a banana", "defeats aliens in", "invents a new sport called", "teaches dinosaurs how to play",
                  "wins a match by sneezing loudly", "breaks the sound barrier while", "discovers the secret to", "challenges Superman to"],
        "places": ["on the moon's surface", "inside a volcano", "during a time travel expedition", "while floating in zero gravity",
                  "in Atlantis", "at a medieval castle", "during an earthquake", "in a dream sequence"]
    },
    "celebrity": {
        "subjects": {
            "Indian": ["A Bollywood star", "A famous actor", "A movie legend", "A celebrity"],
            "Pakistani": ["An entertainment icon", "A film star", "A singing sensation", "A drama artist"]
        },
        "actions": ["adopts 100 cats and teaches them to", "builds a house made entirely of", "discovers they are actually", "starts a business selling",
                   "announces they can speak to", "reveals their secret identity as", "opens a restaurant that only serves", "claims to have invented"],
        "places": ["in a chocolate factory", "while skydiving with penguins", "during a meeting with aliens", "inside a giant bubble",
                  "on a deserted island with talking trees", "in a world made of candy", "during a tea party with robots", "at a school for wizards"]
    }
}

# 3-loop
while True:
    category = input("Enter category (politics/sports/celebrity): ").strip().lower()
    
    # Fixed validation loop
    while category not in ["politics", "sports", "celebrity"]:
        category = input("Please enter correct category (politics/sports/celebrity): ").strip().lower()
    
    # Fixed dictionary access - use square brackets instead of parentheses
    data = fake_news_data[category]
    nationality = rand.choice(["Indian", "Pakistani"])
    subject = rand.choice(data["subjects"][nationality])
    action = rand.choice(data["actions"])
    place = rand.choice(data["places"])
    
    headline = f"BREAKING NEWS: {subject} {action} {place}"
    print("\n" + headline)
    
    user_input = input("Do you want to store this news in a text file? (yes/no): ").strip().lower()
    if user_input == "yes":
        with open("headlines.txt", "a") as file:
            file.write(headline + "\n")
        print("Headline saved to headlines.txt")

    user_input = input("\nDo you want another headline? (yes/no): ").strip().lower()
    if user_input == "no":
        break

# 4-print goodbye
print("\nThanks for using Fake News Headline Generator. Have a good day!")