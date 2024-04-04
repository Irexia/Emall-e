def train():
    # train = open("pseudo-main/alpha/chatbot/train.txt", "r")
    train = open("alpha/chatbot/train.txt", "r")

    f = train.readlines()
    train_lis = []

    for line in f:
        train_lis.append(line.strip("\n").strip(" "))

    train.close()
    # print(train_lis)
    return train_lis
