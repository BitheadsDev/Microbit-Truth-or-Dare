from microbit import *
import random

#GAME VARS
gsTime = 3000
timeCompare = 0
numOfPlayers = 1
maxPlayers = 8
minPlayers = 2
stage = 'start'
minSpinTime = 3000

#POWER VARS
power = 0

#PLAYER VARS
#Which player is currently selected
selected = 0

#BUTTONS VARS
pressed = False

#SPINNER VARS
rdTime = 0
spinSleep = 400
spinSleepOrig = spinSleep

#FUNCTION STAGE VARS
funcStage = 'start'

#Tuple of all X,Y LED positions; spin position order index; and an arrow image to display once spinner stops
positions = [
    ((2, 4), 1, Image.ARROW_S),
    ((2, 0), 5, Image.ARROW_N),
    ((0, 2), 3, Image.ARROW_W),
    ((4, 2), 7, Image.ARROW_E),
    ((0, 4), 2, Image.ARROW_SW),
    ((4, 0), 6, Image.ARROW_NE),
    ((0, 0), 4, Image.ARROW_NW),
    ((4, 4), 8, Image.ARROW_SE)
]
#Store for active players set in order of spin
positionsOrdered = []

#Images that are shown when selecting power.
powerImg1 = Image("00000:00000:00000:00000:99999")
powerImg2 = Image("00000:00000:00000:99999:99999")
powerImg3 = Image("00000:00000:99999:99999:99999")
powerImg4 = Image("00000:99999:99999:99999:99999")
powerImg5 = Image("99999:99999:99999:99999:99999")

powerImgs = (powerImg1, powerImg2, powerImg3, powerImg4, powerImg5)

#UTILITY FUNCTIONS

#Return a random range of numbers
def rdRange(minMult,maxMult,base):
    return random.randint(base*minMult, base*maxMult)

#return sort key of positions list
def getKey(item):
    return item[1]

#Reset the funcStage var for the next stage
def resetFuncStage():
    return 'start'

#Frustratingly we have to add a fake button press call in here as any earlier is_pressed function will automatically set was_pressed to True in subsequent was_pressed calls
def resetButtonPressed():
    if button_a.was_pressed() or button_b.was_pressed():
        print('reset .was_pressed')

#MAIN APP LOOP
while True:

    #STAGE: ASK PLAYER FOR NUMBER OF PLAYERS UP TO MAX PLAYERS
    if stage == 'start':
        #If B is pressed increment by 1 up the max players and cycle back to 1
        if button_b.was_pressed():
            timeCompare = running_time()
            if numOfPlayers >= maxPlayers:
                numOfPlayers = minPlayers
            else:
                numOfPlayers += 1
            display.show(str(numOfPlayers))
            pressed = True
        #If A is pressed decrement by 1 down to 1 and then cycle back to maxPlayers var
        elif button_a.was_pressed():
            timeCompare = running_time()
            if numOfPlayers <= minPlayers:
                numOfPlayers = maxPlayers
            else:
                numOfPlayers -= 1
            display.show(str(numOfPlayers))
            pressed = True
        elif pressed == False:
            #Ask how many players
            display.show('#?')
        else:
            if running_time() - timeCompare >= gsTime:
                stage = 'positionPlayers'

    #STAGE: DISPLAY THE POSITION OF PLAYERS
    elif stage == 'positionPlayers' and pressed == True:
        pressed = False
        display.clear()
        for i in range(numOfPlayers):
            el = positions[i]
            #Add selected number of players to positionsOrdered
            positionsOrdered.append(el)
            x = el[0][0]
            y = el[0][1]
            display.set_pixel(x, y, 9)
        #Sort positionsOrdered by the 2nd sub-item in each list item
        positionsOrdered.sort(key=getKey)
        stage = 'power'

    #STAGE: ASK PLAYER TO SELECT POWER
    elif stage == 'power':
        if funcStage == 'start':
            if button_a.was_pressed() or button_b.was_pressed():
                display.show('PWR')
                funcStage = 'selectPower'
        elif funcStage == 'selectPower':
            i = 0
            numOfPowers = len(powerImgs)
            while button_a.is_pressed() or button_b.is_pressed():
                display.show(powerImgs[i])
                if i + 1 != numOfPowers:
                    i += 1
                    power = i
                else:
                    i = 0
                    power = numOfPowers
                sleep(400)
                funcStage = 'goSpin'
        elif funcStage == 'goSpin':
            resetButtonPressed()
            funcStage = resetFuncStage()
            stage = 'spin'

    #STAGE: START THE SPIN
    elif stage == 'spin':
        #Create a usable value to append to sleep int that changes depending on power selection
        powerFunc = power / 100
        #If more than four players create a value that decreases (speeds up) the sleep int
        if numOfPlayers > 4:
            powerAdjustNOP = numOfPlayers / 4
        else:
            powerAdjustNOP = 1

        if funcStage == 'start':
            #needed as spin needs to be faster when more players.
            spinSleep = (spinSleepOrig / power) / powerAdjustNOP
            funcStage = 'calcSpin'
        for i in range(numOfPlayers):
            spinSleep = spinSleep / (0.9 + powerFunc)
            display.clear()
            el = positionsOrdered[i]
            x = el[0][0]
            y = el[0][1]
            display.set_pixel(x, y, 9)
            sleep(spinSleep)
            if funcStage == 'calcSpin' and spinSleep >= 250:
                timeCompare = running_time()
                rdTime = rdRange(200, 1000, numOfPlayers)
                funcStage = 'setStop'
            elif funcStage == 'setStop':
                if running_time() - timeCompare >= rdTime:
                    funcStage = 'stop'
            elif funcStage == 'stop':
                selected = i
                stage = 'selectedPlayer'
                funcStage = resetFuncStage()
                break

    #STAGE: SHOW THE SELECTED PLAYER
    elif stage == 'selectedPlayer':
        el = positionsOrdered[selected]
        display.clear()
        sleep(300)
        display.show(el[2])
        sleep(300)
        #Reset back to power stage
        if button_a.was_pressed() or button_b.was_pressed():
            display.show('PWR')
            funcStage = 'selectPower'
            stage = 'power'