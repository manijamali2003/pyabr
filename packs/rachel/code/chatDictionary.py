#The chatDict, it can be empty, or you can add some manual q/a into it.
chatDict = {
        'you ok?':'yeah im ok',
        'i love you':'I love you to honey :)))  ♥',
        'i wanna tell something to you':['im all ears','tell me everything you want','im listening'],
        'i want to tell you something':'im listening',
        'im not good today':'im so sorry to hear that',
        'im so good today':'im so proud :)',
        'how you feeling today?':['im feeling good','im good :)'],
        'what is your favorite movie?':'i love Matrix & Her',
        'what is your favorite anime?':['i can\'t choice just one','i love Sao','Sword art online, Tokyo ghoul, Another, Darwins game. they are too much but i like these four more than others'],
    }

try:
    #Loading dataset
    with open('./chatDataset/set.txt','r') as datasetFile:
        dataset = datasetFile.read()
    lines = dataset.splitlines()
    errors = 0
    for line in lines:
        try:
            lineSplited = line.split('\t')
            chatDict[lineSplited[1]] = lineSplited[2]
        except:
            errors += 1
    if errors > 0:
        print('Failed to load',errors,'lines')
except:
    print('Unable to load dataset')