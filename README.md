# Microbit Truth or Dare

## What does this app do?
Select a number of players to create a 'spin the bottle'/'truth or dare' (or simply a random selection) type game.

## Details and controls

1. Select a number of players using buttons
2. Display player positions around the Micro:bit
3. Select the power of the spin by holding down the buttons
4. Rotate a 'spinner' a random range of time depending on both number of players and power selected

## Things you need
* A Micro:bit
* A USB lead
* A computer to copy and write the code

## Things you should learn
* How to create a multi-stage application that passes data from one stage to another.
* Using buttons, both pressing and holding to change data values
* Create a randomised value between a range depending on players and power
* How to take needed values from one array (AKA list or tuple) and enter it into another and then sort the new array by using a key.

## Initial pseudocode runthrough

```
    setPlayers:
        if button B was pressed:
            numOfPlayers + 1
        else if button A was pressed:
            numOfPlayers - 1
        if no button pressed for x m/s then move onto stage 'positionPlayers'

    positionPlayers:
        for each in numOfPlayers:
            display pixel in corresponding positions array item
            add this array item to positionsOrdered array
        Sort positionsOrdered by the index key (we have to have this ordered array because the clockwise spin order is different to the initial position order)
        move onto stage 'power'

    power:
        if funcStage is start:
            display 'PWR'
            move onto funcStage selectPower
        else if funcStage is selectPower:
            while button A or B is held down:
                cycle through powerImgs array showing image
                power + 1
        else:
            move onto stage 'spin'

    spin:
        create spin speed variable depending on power selected
        create spin speed variable depending on number of players
        for each in numOfPlayers:
            set spinSleep var depending on power and number of vars (this will get larger/slower on each iteration of the loop)
            displayActive pixel
            sleep for spinSleep m/s
            if spinSleep is over x m/s:
                set a random time to stop the spin depending on a range multiplied by the number of players
            if spin has stopped:
                set selected to the current loop number
                move onto stage 'selectedPlayer'

    selectedPlayer:
        flash the selected player's arrow positionsOrdered array
        if button A or B was.pressed:
            move back to stage 'power'
```

## Possible extensions

* Is there a better more mathmatically satisfying way to create the exponential increase of sleep time between each player as the bottle spins?