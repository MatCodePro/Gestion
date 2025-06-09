#TODO:
"""
-Completar la funcion turnTracker
-Completar la función onePlusVerifier
-activar imput en playerName
"""


import random
import time
from collections import Counter
from classes import *

### FUNCTIONS ###

# La función new_deck construye el mazo de cartas y lo entrega como recién salido de la caja
def new_deck():
    newDeck = []
    colours = ["Rojo", "Verde", "Amarillo", "Azul"]
    values = [0,1,2,3,4,5,6,7,8,9,"+2","Saltear","Giro"]
    wilds = ["Comodín","+4"]
    for colour in colours:
        for value in values:
            cardVal = f"{value} {colour}"
            newDeck.append(cardVal)
            if value != 0:
                newDeck.append(cardVal)
    for i in range(4):
        newDeck.append(wilds[0])
        newDeck.append(wilds[1])
    return newDeck

# La función shuffle recibe como parámetro el mazo, lo mezcla y entrega las cartas mezcladas
def shuffle(cards):
    random.shuffle(cards)
    return (cards)

# La función draw recibe como parámetro una cantidad de cartas y entrega esa cantidad de cartas
def draw(amount):
    cardsDrawn = []
    if amount < len(gameDeck):
        for i in range(amount):
            cardsDrawn.append(gameDeck.pop(0))
        return (cardsDrawn)
    elif amount == len(gameDeck):
        for i in range(amount):
            cardsDrawn.append(gameDeck.pop(0))
            shuffle(discardPile)
        return (cardsDrawn)
    else:
        shuffle(discardPile)
        gameDeck.extend(discardPile)
        for i in range(amount):
            cardsDrawn.append(gameDeck.pop(0))
        return (cardsDrawn)

# La función lottery sortea el jugador que inicia la partida, según el valor de su carta.
def lottery():
    print("-------------------------")
    print("")
    print("Sorteo para ver quién juega primero:")
    print("")
    #time.sleep(2)
    for player in players:
        player.cards = draw(1)
        if len(player.name) < 9:
            spaces = " " * (9 - len(player.name))
            print(f"{spaces}{player.name} --> " + "".join(player.cards))
        else:
            print(f"{player.name} --> " + "".join(player.cards))
    print("")
    cardValues = []
    for player in players:
        card = player.cards[0].split(' ',1)
        cardValues.append(card[0])
    values = ["+4","Comodín","+2","Saltear","Giro","9","8","7","6","5","4","3","2","1","0"]
    for value in values:
        if value in cardValues:
            onPlay = cardValues.index(value)
            #time.sleep(2)
            print(f"{players[onPlay]} va a empezar porque sacó un {cardValues[onPlay]}")
            print("")
            print("-------------------------")
            print("")
            for player in players:
                player.cards = []
            return onPlay

# La función choose_colour elije un color basándose en la mano del bot que elije o el input.
def choose_colour(chooser):
    if chooser != 0:
        cardClours = []
        for card in players[chooser].cards:
            try:
                cardValue = card.split(' ',1)[1]
                cardClours.append(cardValue)
            except IndexError:
                pass
        try:
            colorChoosed = Counter(cardClours).most_common(1)[0][0]
            return colorChoosed
        except IndexError:
            colours = ["Rojo", "Verde", "Amarillo", "Azul"]
            return random.choice(colours)
    else:
        while True:
            try:
                colour = int(input("Elegí un color: 1=Rojo 2=Verde 3=Amarillo 4=Azul "))
            except ValueError:
                print("Tenés que elegir un número del 1 al 4")
                print("")
                continue
            except UnboundLocalError:
                print("Tenés que elegir un número del 1 al 4")
                print("")
                continue
            if colour > 4 or colour < 1:
                print("Tenés que elegir un número del 1 al 4")
                print("")
                continue
            else:
                break
        if colour == 1:
            return "Rojo"
        elif colour == 2:
            return "Verde"
        elif colour == 3:
            return "Amarillo"
        elif colour == 4:
            return "Azul"

# La función first_move verifica el estado inicial de la partida.
def first_move():
    global gameDeck
    global discardPile
    global onPlay
    global direction
    card_on_play()
    if currentValue == "+4":
        gameDeck.insert(random.randrange(len(gameDeck)+1), discardPile.pop(0))
        discardPile = draw(1)
        first_move()
    elif currentValue == "Comodín":
        print_COP()
        card_on_play(choose_colour(onPlay -1))
        print(f"{players[onPlay-1]} eligió el color {currentColour} porque el juego empezó con un Comodín")
        print("")
    elif currentValue == "Saltear":
        print_COP()
        print(f"{players[onPlay]} es salteado porque el juego empezó con un Saltear")
        print("")
        next_turn()
    elif currentValue == "+2":
        print_COP()
        print(f"{players[onPlay]} recibe cartas porque el juego empezó con un +2")
        print("")
        players[onPlay].cards.extend(draw(2))
        next_turn()
    elif currentValue == "Giro":
        direction = -1
        next_turn()
        print_COP()
        print(f"Ahora juega {players[onPlay]} porque el juego empezó con un Giro")
        print("")

# La función turn_tracker se encarga de verificar de quién es el turno actualmente y la dirección de juego
# def turnTracker():

# La función card_on_play actualiza los valores de color y valor en juego
def card_on_play(*colour):
    global currentColour
    global currentValue
    cardOnPlay = str(discardPile[-1])
    cardColour = str(cardOnPlay.split(" ", 1)[-1])
    cardNumber = str(cardOnPlay.split(" ", 1)[0])
    if cardNumber == "+4" or cardNumber == "Comodín":
        currentValue = cardNumber
        if colour:
            currentColour = colour[0]
    else:
        currentValue = cardNumber
        currentColour = cardColour

# La función print_playing_card imprime la carta en juego
def print_COP():
    if currentValue == "+4" or currentValue == "Comodín":
        print(f"La carta en juego es {currentValue} con el color {currentColour}")
        print("")
    else:
        print(f"La carta en juego es: {currentValue} {currentColour}")
        print("")

# La función can_play() recibe como parámetro una carte y determina si se puede jugar
def can_play(card):
    selectedCard = card[0].split(" ", 1)
    if "+4" in card or "Comodín" in card:
        return True
    if currentValue in selectedCard or currentColour in selectedCard:
        return True
    else:
        return False

# La función show_hand muestra las cartas que actualmente tiene el jugador
def show_hand():
    print(f"{pOne.name}, tus opciones son:")
    print("")
    print(f"0 -> Levantar una carta")
    i = 1
    for card in pOne.cards:
        print(f"{i} -> {card}")
        i += 1
    if len(pOne.cards) == 2 :
        print("3 -> Cantar UNO!")
    print("")
    def select():
        saidUno = False
        while True:
            try:
                selection = int(input("Qué carta querés jugar? "))
                print("")
            except ValueError:
                if len(pOne.cards) == 2:
                    print("Tenés que elegir un número entre 0 y 3")
                    continue
                else:
                    print(f"Tenés que elegir un número del 0 al {len(pOne.cards)}")
                    print("")
                    continue
            except UnboundLocalError:
                if len(pOne.cards) == 2:
                    print("Tenés que elegir un número entre 0 y 3")
                    continue
                else:
                    print(f"Tenés que elegir un número del 0 al {len(pOne.cards)}")
                    print("")
                    continue
            if selection < 0 or selection > len(pOne.cards):
                if selection == 3:
                    pOne.say_uno()
                    saidUno = True
                    continue
                else:
                    print(f"Tenés que elegir un número del 0 al {len(pOne.cards)}")
                    print("")
                    continue
            elif selection == 0:
                newCard = draw(1)
                if can_play(newCard):
                    print(f"Levantaste {newCard}")
                    print("")
                    pOne.cards.extend(newCard)
                    while True:
                        try:
                            if len(pOne.cards) == 2:
                                print(f"Mati, tus opciones son: \n1 -> Jugar {newCard} \n2 -> Pasar \n3 -> Cantar UNO \n")
                            else:
                                print(f"Mati, tus opciones son: \n1 -> Jugar {newCard} \n2 -> Pasar \n")
                            afterPick = int(input("Qué querés hacer?"))
                            print("")
                        except ValueError:
                            if len(pOne.cards) == 2:
                                print(f"Tenés que elegir 1, 2 ó 3")
                                continue
                            else:
                                print(f"Tenés que elegir 1 ó 2")
                                print("")
                                continue
                        except UnboundLocalError:
                            if len(pOne.cards) == 2:
                                print(f"Tenés que elegir 1, 2 ó 3")
                                continue
                            else:
                                print(f"Tenés que elegir 1 ó 2")
                                print("")
                                continue
                        if afterPick < 1 or afterPick > 2:
                            if afterPick == 3:
                                pOne.say_uno()
                                print("")
                                continue
                            else:
                                print(f"Tenés que elegir 1 ó 2")
                                print("")
                                continue
                        elif afterPick == 1:
                            if len(pOne.cards) == 2:
                                pOne.cards.extend(draw(2))
                                print("Te olvidaste cantar UNO!!! Ahora tenés que levantar 2 cartas")
                                print("")
                                break
                            else:
                                print(f"Jugaste el {pOne.cards[-1]}")
                                print("")
                                discardPile.extend(pOne.cards.pop(-1))
                                card_on_play()
                                break
                        elif afterPick == 2:
                            print("Pasaste")
                            print("")
                            next_turn()
                            break
                    break
                else:
                    print(f"Levantaste un {newCard[0]} y pasaste porque no se puede jugar")
                    print("")
                    pOne.cards.extend(newCard)
                    next_turn()
                    break
            else:
                selectedCard = [pOne.cards[selection -1]]
                if len(pOne.cards) == 2 and saidUno == False:
                        pOne.cards.extend(draw(2))
                        print("Te olvidaste cantar UNO!!! Ahora tenés que levantar 2 cartas")
                        print("")
                        break
                if can_play(selectedCard):
                        print(f"Has jugado el {selectedCard[0]}")
                        print("")
                        discardPile.extend(pOne.cards.pop(selection -1))
                        card_played(selectedCard[0])
                        break
                else:
                    print(saidUno)
                    print(f"No puedes jugar el {selectedCard[0]}")
                    print("")
                    continue
    select()

# La funcion card_played verifica si se ha jugado alguna carta especial
def card_played(card):
    global cardDrawCounter
    if type(currentValue) != int:
        if currentValue == "+4":
            cardDrawCounter = cardDrawCounter + 4
            if cardDrawCounter < 5:
                choose_colour()
                next_turn()
            elif cardDrawCounter > 5:
                choose_colour
                next_turn()
                if onPlay == 0:
                    print("Tus opciones son:")
                    print(f"1 -> Levantar {cardDrawCounter} cartas")
                    print(f"2 -> Desconfiar de {players[onPlay + (direction * -1)]}")
                    if "+4" in players[onPlay]:
                        print ("3 -> Jugar un +4")
                    try:
                        desition = int(input("Que querés hacer?"))
# Por acá
    else:
        next_turn()



# La función next_turn avanza un turno segun el valor de direction
def next_turn():
    global onPlay
    global direction
    onPlay += direction
    if onPlay == 3:
        onPlay = 0
    if onPlay == -1:
        onPlay = 3

# La función one_plus_verifier verifica que todos los jugadores tengan 1 o más cartas

### GAME ###

print("Bienvenido!")
print("")
#time.sleep(1)
print("Mezclando las cartas...")
print("")
#time.sleep(3)
# Primero definimos el mazo de juego, mezclando un nuevo mazo
gameDeck = shuffle(new_deck())

# Definimos el mazo de descarte vacío
discardPile = []

# Definimos el color en juego
currentColour = ""

# Definimos el valor en juego
currentValue = ""

# Definimos el orden por defecto
onPlay = 0

# Definimos la dirección de juego
direction = 1

# Definimos los jugadores incluyendo tanto a los bots como al jugador real

#playerName = input("Escribí tu nombre acá")
playerName = ("Mati")
pOne = PLAYER(playerName)
pTwo = PLAYER("Jugador 2")
pTree = PLAYER("Jugador 3")
pFour = PLAYER("Jugador 4")
players = [pOne, pTwo, pTree, pFour]

# Definimos el contador para levantar de cartas
cardDrawCounter = 0

# Sorteamos el turno inicial y volvemos a barajar.
onPlay = lottery()
#time.sleep(4)

# Barajamos y repartimos las cartas
print("Barajamos y repartimos 7 cartas a cada uno")
print("")
gameDeck = shuffle(new_deck())
print("-------------------------")
print("")
#time.sleep(4)
for player in players:
    player.cards = draw(1)
""" carta = "Comodín"
discardPile = [carta] """
discardPile = draw(1)
first_move()
print_COP()
show_hand()