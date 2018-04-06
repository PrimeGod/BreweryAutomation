import RPi.GPIO as GPIO
import spidev as spidev

import pygame

#############--INIT--##########################
spi = spidev.SpiDev()

pygame.init()
mode_ecran = 0
#############--Constantes--########################
# Boucle jusqu a la fermeture du clavier
done = False    #valeur determinant la fin du programme
transparence = 255  #transparence des touches

#Texte d'affichage du menu principal
textjeu = "Jeu"
textmessage = "Messagerie"
textsettings = "Parametres"
textquit = "Quitter"

#Texte d'affichage du menu jeu
textback = "Retour"
textchanger = "Couleurs"
textqui = "Joueur"
textgo = "Go"

#Texte d'affichage du menu messagerie
textopen = "Clavier"
textclavier = ""
textefface = "Effacer"

#############--FONCTIONS--##########################
def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.SETUP(22, gpio.IN) #input pour le pull a la pin 22

    #SPI setup
    CLK = 40
    MISO = 35
    MOSI = 38
    CS = 36

    spi.open(1,2) #bus 1 device 0
    spi.max_speed_hz = 7629

def write_msg(msg):
    for current in range(len(msg)):
        readDummy = spi.xfer2(msg[current])

def receive():
    global readData
    for current in range(4):
        readData[current] = spi.xfer2([0x55])
    for current in range(readData[3]):
        readData[current+4] = spi.xfer2([0x55])
        return readData

def msg_format():
    global msg_to_send
    msg_to_send[0] = source
    msg_to_send[1] = destination
    msg_to_send[2] = len(Message)
    msg_to_send[3] = msg_type

    for i in (len(Message)):
        msg_to_send[i+4] = hex(Message[i])

    return msg_to_send

def key_locking(master):
    pic_key = spi.xfer2(master)
    if pic_key == 0xa6 or pic_key == 0x06:
        return True, pic_key
    else:
        return False, pic_key
def action():
    global mode_ecran
    global fond
    global selection1
    global selection2
    global selection3
    global selection4
    global selection5
    global selection6
    global selection7
    global selection8
    global destination
    global Message

    if mode_ecran == 1:                                 #actions effectuees a l'ecran jeu
        if (position >= 0 and position <= 4):
            mode_ecran = 0  #menu principal

        if (position >= 55 and position <= 64):
            game_data = hex(position -55)
            #data to send
        elif (position >= 81 and position <= 90):
            game_data = hex(position -71)
            #data to send
        else:
            game_data = None

        if position == 71:              #selection joueur 1
            if selection1 == black:
                selection1 = white
                selection2 = black
                selection3 = black
                selection4 = black
                destination = 0xA1
            elif selection1 == white:
                selection1 = black
                selection2 = black
                selection3 = black
                selection4 = black
                destination = None
        elif position == 97:            #selection joueur 2
            if selection2 == black:
                selection1 = black
                selection2 = white
                selection3 = black
                selection4 = black
                destination = 0xA2
            elif selection2 == white:
                selection1 = black
                selection2 = black
                selection3 = black
                selection4 = black
                destination = None
        elif position == 123:           #selection joueur 3
            if selection3 == black:
                selection1 = black
                selection2 = black
                selection3 = white
                selection4 = black
                destination = 0xA3
            elif selection3 == white:
                selection1 = black
                selection2 = black
                selection3 = black
                selection4 = black
                destination = None
        elif position == 149:           #selection joueur 4
            if selection4 == black:
                selection1 = black
                selection2 = black
                selection3 = black
                selection4 = white
                destination = 0xA4
            elif selection4 == white:
                selection1 = black
                selection2 = black
                selection3 = black
                selection4 = black
                destination = None
        else:
            destination = None

        if (position >= 181 and position <= 182):               #go -> send message
            msg_type = 0x00         #gamedata
            msg_format()
            selection1 = black
            selection2 = black
            selection3 = black
            selection4 = black
            

    if mode_ecran == 2:       
        if (position >= 0 and position <= 4):
            mode_ecran = 0  #menu principal

        if (position >= 27 and position <= 31):
            mode_ecran = 4

        if (position >= 157 and position <= 161):
            Message = ""

        if position == 76:
            if selection5 == black:
                selection5 = white
                selection6 = black
                selection3 = black
                selection4 = black
                destination = 0xA1
            elif selection5 == white:
                selection5 = black
                selection6 = black
                selection7 = black
                selection8 = black
                destination = None
        elif position == 102:
            if selection6 == black:
                selection5 = black
                selection6 = white
                selection7 = black
                selection8 = black
                destination = 0xA2
            elif selection6 == white:
                selection5 = black
                selection6 = black
                selection7 = black
                selection8 = black
                destination = None
        elif position == 128:
            if selection7 == black:
                selection5 = black
                selection6 = black
                selection7 = white
                selection8 = black
                destination = 0xA3
            elif selection7 == white:
                selection5 = black
                selection6 = black
                selection7 = black
                selection8 = black
                destination = None
        elif position == 154:
            if selection8 == black:
                selection5 = black
                selection6 = black
                selection7 = black
                selection8 = white
                destination = 0xA4
            elif selection8 == white:
                selection5 = black
                selection6 = black
                selection7 = black
                selection8 = black
                destination = None
        else:
            destination = None

        if (position >= 181 and position <= 182):
            msg_type = 0x01         #textdata
            msg_format()
            selection5 = black
            selection6 = black
            selection7 = black
            selection8 = black
            Message = ""

    if mode_ecran == 3:
        if (position >= 0 and position <= 4):
            mode_ecran = 0  #menu principal

        if (position >= 55 and position <= 74):
            fond = couleurs[position - 55]

    if mode_ecran == 4:
        clavier()


    return mode_ecran, fond, selection1, selection2, selection3, selection4,selection5, selection6, selection7, selection8, Message, destination, msg_type

def affichage():
    global mode_ecran
    global fond
    global selection1
    global selection2
    global selection3
    global selection4
    global selection5
    global selection6
    global selection7
    global selection8
    global Message
        
    if mode_ecran == 0:
        screen.fill(fond)
            
        text = font.render(textjeu, True, white)
        text2 = font.render(textmessage, True, white)
        text3 = font.render(textsettings, True, white)
        text4 = font.render(textquit, True, white)
                
        screen.blit(text,[50,15])
        screen.blit(text2,[50,55])
        screen.blit(text3,[50,95])
        screen.blit(text4,[50,135])

    if mode_ecran == 1:
        screen.fill(fond)

        text = font.render(textback, True, white)    
        text2 = font.render(textchanger, True, white)
        text3 = font.render(textqui, True, white)
        text4 = font.render(textgo, True, white)
        text5 = font.render("1", True, white)    
        text6 = font.render("2", True, white)
        text7 = font.render("3", True, white)
        text8 = font.render("4", True, white)
                
        screen.blit(text,[0,0])
        screen.blit(text2,[115,55])
        screen.blit(text3,[300,55])
        screen.blit(text4,[485,255])
        screen.blit(text5,[335,90])
        screen.blit(text6,[335,130])
        screen.blit(text7,[335,170])
        screen.blit(text8,[335,210])
        
        for i in range(0,len(couleurs)):
            if i >= 10 :
                posy = 130
                posx = 50 + (i-10)*20
            else:
                posx = 50 + i*20
                posy = 100
            pygame.draw.circle(screen,couleurs[i],[posx,posy],10)
            pygame.draw.circle(screen,white,[posx,posy],10,1)

        pygame.draw.circle(screen,selection1,[365,100],10)
        pygame.draw.circle(screen,white,[365,100],10,4)

        pygame.draw.circle(screen,selection2,[365,140],10)
        pygame.draw.circle(screen,white,[365,140],10,4)

        pygame.draw.circle(screen,selection3,[365,180],10)
        pygame.draw.circle(screen,white,[365,180],10,4)

        pygame.draw.circle(screen,selection4,[365,220],10)
        pygame.draw.circle(screen,white,[365,220],10,4)

    if mode_ecran == 2:
        screen.fill(fond)

        text = font.render(textback, True, white)    
        text2 = font.render(textopen, True, white)
        
        text4 = font.render(textqui, True, white)
        text5 = font.render(textgo, True, white)
        text6 = font.render(textefface, True, white)
        text7 = font.render("1", True, white)    
        text8 = font.render("2", True, white)
        text9 = font.render("3", True, white)
        text10 = font.render("4", True, white)
        
        text11 = fontmessage.render(Message[0:27], True, black)
        text12 = fontmessage.render(Message[27:54], True, black)
        text13 = fontmessage.render(Message[54:81], True, black)
        text14 = fontmessage.render(Message[81:108], True, black)
        text15 = fontmessage.render(Message[108:135], True, black)
        text16 = fontmessage.render(Message[135:162], True, black)
        text17 = fontmessage.render(Message[162:189], True, black)
        text18 = fontmessage.render(Message[189:216], True, black)
        text19 = fontmessage.render(Message[216:240], True, black)
          
        pygame.draw.rect(screen, white, [5, 70, 440, 180])
        
        pygame.draw.circle(screen,selection5,[475,102],10)
        pygame.draw.circle(screen,white,[475,102],10,4)

        pygame.draw.circle(screen,selection6,[475,142],10)
        pygame.draw.circle(screen,white,[475,142],10,4)

        pygame.draw.circle(screen,selection7,[475,182],10)
        pygame.draw.circle(screen,white,[475,182],10,4)

        pygame.draw.circle(screen,selection8,[475,222],10)
        pygame.draw.circle(screen,white,[475,222],10,4)
        
        screen.blit(text,[0,0])
        screen.blit(text2,[1,40])
        
        screen.blit(text11,[6,71])
        screen.blit(text12,[6,91])
        screen.blit(text13,[6,111])
        screen.blit(text14,[6,131])
        screen.blit(text15,[6,151])
        screen.blit(text16,[6,171])
        screen.blit(text17,[6,191])
        screen.blit(text18,[6,211])
        screen.blit(text19,[6,231])
        
        screen.blit(text4,[430,40])
        screen.blit(text5,[485,255])
        screen.blit(text6,[1,255])
        screen.blit(text7,[450,90])
        screen.blit(text8,[450,130])
        screen.blit(text9,[450,170])
        screen.blit(text10,[450,210])


    if mode_ecran == 3:
        screen.fill(fond)

        text = font.render(textback, True, white)    
        text2 = font.render(textchanger, True, white)
                
        screen.blit(text,[0,0])
        screen.blit(text2,[0,55])

        
        
        for i in range(0,len(couleurs)):
            posx = 50 + i*20
            pygame.draw.circle(screen,couleurs[i],[posx,100],10)
            pygame.draw.circle(screen,white,[posx,100],10,1)

    return Message
        

def clavier():
    global donekb
    global tabposkb
    global couleur
    global shift
    global maj
    global symbol
    global couleurclavier
    global mode_ecran
    global Message
    global Message1
    global Message2
    global Message3
    global Message4
    global Message5
    global Message6
    global Message7
    global Message8
    

    ################--Taille de la fenetre--############################
    sizeclaviery = 240
    size = [516,sizeclaviery]        #environ la moitie de l'ecran tactile
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
 
    #############--Constantes--########################
    # Boucle jusqu a la fermeture du clavier
    donekb = False    #valeur determinant la fin du programme
    transparence = 255  #transparence des touches

    #valeurs de base des touches de traitement
    maj = False #allcaps
    shift = False
    tabposkb = None   #tab
    espace = False
    symbol =  0   #pour l appui des touches en extra
    
    #Message = ""    #string du message qu on print
    text = ""       #string du message qui apparait pendant l ecriture

    #Array
    TABW = 42       #largeur des cases du tableau graphique
    TABH = 42       #hauteur
    MARGIN = 1      #1 pixel entre chaque case

    GRID = []       #declaration du tableau graphique

    for row in range(5):    #ici on dessine le tableau
        GRID.append([])
        for column in range (12):
            GRID[row].append(0)

    #background = pygame.image.load("lion.jpg")

    ##############--Touches du clavier--###############################
    touches = ('','1','2','3','4','5','6','7','8','9','0','-',
               'q','w','e','r','t','y','u','i','o','p',chr(8),chr(8),#backspace
               'a','s','d','f','g','h','j','k','l',';','^',chr(13),#return
               'St','z','x','c','v','b','n','m',chr(91),chr(93),'.',chr(13),#bracketg,d,backslash
               'SYM','CAP','TAB',chr(32),chr(32),chr(32),chr(32),chr(44),chr(123),chr(125),chr(126),chr(13))#space, virgule, crochetg,

    #touches en extra quand on appuie sur SYM
    symkeys = ('!','@','/','$','%','?','&','*','(',')','_','+',
                 '','','','','','','','','','=',chr(8),chr(8),
                 '','','','','','','','','',':','|',chr(13),
                 '','','','','','','','','<','>',chr(92),chr(13),
                 'abc','','',chr(32),chr(32),chr(32),chr(32),chr(39),'','','',chr(13))

    ############--Programme principal--######################
    while mode_ecran == 4:        #on observe si la valeur de fin du programme est toujours a false avant de continuer

        # -----Boucle principale
        try:
            for event in pygame.event.get():    #lutilisateur fait quelque chose
                if event.type == pygame.QUIT: #si lutilisateur clique pour fermer la page
                    mode_ecran = 2
                elif event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_ESCAPE:    #sortie avec esc s'il y a un bug
                        mode_ecran = 2

            # -----Logique des appuis de touches
            
                elif event.type == pygame.MOUSEBUTTONDOWN:  #evenement d appui de la souris
                    mouseposx = pygame.mouse.get_pos()[0]   #position de la souris en x
                    mouseposy = pygame.mouse.get_pos()[1]   #et en y
                    column = mouseposx // (TABW + MARGIN)   #ici on distribue les positions de la souris selon le tableau graphique
                    row = mouseposy // (TABH + MARGIN)
                    tabposkb = ((column)+((row*12)+1))-1      #comme ca, on a la position de la case associee a une lettre
                    
                    if tabposkb == 0:
                        size = [520,280]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        Message = ""
                        mode_ecran = 2

                    #--- Gestion de Message
                    if tabposkb == 36:    #position de shift
                        shift = True
                        break;

                    elif tabposkb == 48:  #position de SYM
                        symbol = not symbol

                    elif tabposkb == 49:  #position de CAP pour all caps
                        maj = not maj

                    if symbol == 0:     #selon si on est avec le clavier des touches supplementaires ou non
                        if maj == True: #ALLCAPS
                            if shift == False:      #gestion de shift quand on est en mode all caps
                                if (tabposkb == 48) or (tabposkb == 49):
                                    char = ""
                                else:
                                    char = (str(touches[tabposkb])).upper()
                            elif shift == True:
                                char = (str(touches[tabposkb]))

                            
                            elif tabposkb == 50:    #Tab => apparait comme une case sur clavier, mais print reellement une tabulation horizontale
                                char = "\t"

                            elif char == "SYM":     #pour ne pas ecrire SYM et CAP dans la barre de texte du clavier
                                char = ""
                                
                            Message = Message + char
                        else:
                            if shift == False:  #gestion de shift
                                char = (str(touches[tabposkb]))
                            elif shift == True:
                                char = (str(touches[tabposkb])).upper()
                            
                            if tabposkb == 50:    #tab
                                char = "\t"

                            elif char == "SYM": 
                                char = ""

                            elif char == "CAP":
                                char = ""
                                
                            Message = Message + char
                            
                    if symbol == 1:     #gestion du clavier symboles
                            char = (str(symkeys[tabposkb]))

                            if tabposkb == 50:    #tab
                                char = "\t"

                            elif char == "abc": #pour ne pas ecrire le abc qui ramene au clavier principal
                                char = ""

                            elif char == "CAP": #pour ne pas ecrire CAP
                                char = ""
                                
                            Message = Message + char

                #Traitement texte
                        
                    if tabposkb == 22 or tabposkb == 23:    #backspace
                        Message = Message[:-2]

                    if tabposkb == 35 or tabposkb == 47 or tabposkb == 59:    #return le message
                        Message = Message [:-1]
                        size = [520,280]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        mode_ecran = 2
                        #Message = ""
                        
                    shift = False
                # --------------------------------- 


                # ----- Logique de dessin du clavier            
                screen.fill(black)  #fond noir
                #screen.blit(background,[0,0])  #uncomment la ligne si on a une image de background
                posx = 0    #les positions des carres representants les touches
                posy = 0
                space = 0

                Message1 = Message[0:30]
                Message2 = Message[30:60]
                Message3 = Message[60:90]
                Message4 = Message[90:120]
                Message5 = Message[120:150]
                Message6 = Message[150:180]
                Message7 = Message[180:210]
                Message8 = Message[210:240]

                if (len(Message)>=0) and (len(Message)<30):
                    if sizeclaviery > 240:
                        sizeclaviery = 240
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        
                    textboite1 = fontcouleur.render(""+ str(Message1),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite1,[5,220])

                if (len(Message)>=30) and (len(Message)<60):
                    if sizeclaviery < 260:
                        sizeclaviery = 260
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                    if sizeclaviery > 260:
                        sizeclaviery = 260
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        
                    textboite1 = fontcouleur.render(""+ str(Message1),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite1,[5,220])
                    textboite2 = fontcouleur.render(""+ str(Message2),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite2,[5,240])
                    
                if (len(Message)>=60) and (len(Message)<90):
                    if sizeclaviery < 280:
                        sizeclaviery = 280
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                    if sizeclaviery > 280:
                        sizeclaviery = 280
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        
                    textboite1 = fontcouleur.render(""+ str(Message1),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite1,[5,220])
                    textboite2 = fontcouleur.render(""+ str(Message2),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite2,[5,240])
                    textboite3 = fontcouleur.render(""+ str(Message3),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite3,[5,260])
                    
                if (len(Message)>=90) and (len(Message)<120):
                    if sizeclaviery < 300:
                        sizeclaviery = 300
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                    if sizeclaviery > 300:
                        sizeclaviery = 300
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        
                    textboite1 = fontcouleur.render(""+ str(Message1),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite1,[5,220])
                    textboite2 = fontcouleur.render(""+ str(Message2),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite2,[5,240])
                    textboite3 = fontcouleur.render(""+ str(Message3),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite3,[5,260])
                    textboite4 = fontcouleur.render(""+ str(Message4),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite4,[5,280])
                    
                if (len(Message)>=120) and (len(Message)<150):
                    if sizeclaviery < 320:
                        sizeclaviery = 320
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                    if sizeclaviery > 320:
                        sizeclaviery = 320
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        
                    textboite1 = fontcouleur.render(""+ str(Message1),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite1,[5,220])
                    textboite2 = fontcouleur.render(""+ str(Message2),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite2,[5,240])
                    textboite3 = fontcouleur.render(""+ str(Message3),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite3,[5,260])
                    textboite4 = fontcouleur.render(""+ str(Message4),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite4,[5,280])
                    textboite5 = fontcouleur.render(""+ str(Message5),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite5,[5,300])
                    
                if (len(Message)>=150) and (len(Message)<180):
                    if sizeclaviery < 340:
                        sizeclaviery = 340
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                    if sizeclaviery > 340:
                        sizeclaviery = 340
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        
                    textboite1 = fontcouleur.render(""+ str(Message1),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite1,[5,220])
                    textboite2 = fontcouleur.render(""+ str(Message2),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite2,[5,240])
                    textboite3 = fontcouleur.render(""+ str(Message3),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite3,[5,260])
                    textboite4 = fontcouleur.render(""+ str(Message4),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite4,[5,280])
                    textboite5 = fontcouleur.render(""+ str(Message5),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite5,[5,300])
                    textboite6 = fontcouleur.render(""+ str(Message6),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite6,[5,320])

                if (len(Message)>=180) and (len(Message)<210):
                    if sizeclaviery < 360:
                        sizeclaviery = 360
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                    if sizeclaviery > 360:
                        sizeclaviery = 360
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        
                    textboite1 = fontcouleur.render(""+ str(Message1),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite1,[5,220])
                    textboite2 = fontcouleur.render(""+ str(Message2),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite2,[5,240])
                    textboite3 = fontcouleur.render(""+ str(Message3),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite3,[5,260])
                    textboite4 = fontcouleur.render(""+ str(Message4),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite4,[5,280])
                    textboite5 = fontcouleur.render(""+ str(Message5),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite5,[5,300])
                    textboite6 = fontcouleur.render(""+ str(Message6),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite6,[5,320])
                    textboite7 = fontcouleur.render(""+ str(Message7),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite7,[5,340])

                if (len(Message)>=210) and (len(Message)<240):
                    if sizeclaviery < 380:
                        sizeclaviery = 380
                        size = [516,sizeclaviery]
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                        
                    textboite1 = fontcouleur.render(""+ str(Message1),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite1,[5,220])
                    textboite2 = fontcouleur.render(""+ str(Message2),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite2,[5,240])
                    textboite3 = fontcouleur.render(""+ str(Message3),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite3,[5,260])
                    textboite4 = fontcouleur.render(""+ str(Message4),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite4,[5,280])
                    textboite5 = fontcouleur.render(""+ str(Message5),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite5,[5,300])
                    textboite6 = fontcouleur.render(""+ str(Message6),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite6,[5,320])
                    textboite7 = fontcouleur.render(""+ str(Message7),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite7,[5,340])
                    textboite8 = fontcouleur.render(""+ str(Message8),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite8,[5,360])        

                if len(Message)>= 239:
                    textboite1 = fontcouleur.render(""+ str(Message1),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite1,[5,220])
                    textboite2 = fontcouleur.render(""+ str(Message2),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite2,[5,240])
                    textboite3 = fontcouleur.render(""+ str(Message3),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite3,[5,260])
                    textboite4 = fontcouleur.render(""+ str(Message4),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite4,[5,280])
                    textboite5 = fontcouleur.render(""+ str(Message5),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite5,[5,300])
                    textboite6 = fontcouleur.render(""+ str(Message6),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite6,[5,320])
                    textboite7 = fontcouleur.render(""+ str(Message7),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite7,[5,340])
                    textboite8 = fontcouleur.render(""+ str(Message8),True,white) #affichage du message qu on ecrit dans la barre de texte
                    screen.blit(textboite8,[5,360])              




                for i in range(0,5):                    #ici on dessine les touches de clavier et on controle la couleur
                    for j in range(0,12):
                        coulpos = ((j)+((i*12)+1))-1
                        if coulpos == tabposkb:
                            couleurclavier = persianred
                            
                        if posx == 129 and posx <= 258 and posy > 171:   #space
                            s = pygame.Surface((171,42)) 
                            s.set_alpha(transparence)       #transparence des touches, si on a un background par exemple
                            s.fill(couleurspace)
                            screen.blit(s,(posx,posy))
                            space = 1
                            
                        elif posx == 0 and posy == 129:     #shift
                            if shift == True:
                                if symbol != 1:
                                    couleurshift = persianred
                            else: couleurshift = white
                            s = pygame.Surface((42,42))
                            s.set_alpha(transparence)
                            s.fill(couleurshift)
                            screen.blit(s,(posx,posy))
                            
                        elif posx == 43 and posy == 172:    #allcaps
                            if maj == True:
                                couleurmaj = persianred
                            else: couleurmaj = white
                            s = pygame.Surface((42,42))
                            s.set_alpha(transparence)
                            s.fill(couleurmaj)
                            screen.blit(s,(posx,posy))
                            
                        elif posx >= 430 and posy >= 43 and posy < 86:  #backspace
                            s = pygame.Surface((43,42))
                            s.set_alpha(transparence)
                            s.fill(couleurclavier)
                            screen.blit(s,(posx,posy))
                            
                        elif posx >= 473 and posy >= 86 and posy <= 129:    #return
                            s = pygame.Surface((42,43))
                            s.set_alpha(transparence)
                            s.fill(couleurclavier)
                            screen.blit(s,(posx,posy))
                            
                        else:
                            if space == 1:
                                if posx >= 258:
                                    space = 0
                            else:                           #toutes les autres touches
                                s = pygame.Surface((42,42)) 
                                s.set_alpha(transparence)
                                s.fill(couleurclavier)
                                screen.blit(s,(posx,posy))
                            
                        couleurclavier = white
                        posx += 43  #distance de 43 px entre les carres
                        
                    posx = 0
                    
                    posy += 43 #43 px mais en hauteur
                    
                space = 0
                tabposkb = None
                posy = 0
                
                textx = 16  #positions des lettres
                texty = 16
                k = 0
                x = 0
                y = 12

                #--------Caracteres sur clavier
                if symbol == 0:
                    for i in range(0,5):        
                        for k in range(x,y):
                            if k >= len(touches):break
                            if (k == 22 or k == 23 or k == 35 or k == 47 or k == 59):   #on ne dessine pas ce qu'il y a dans la case pour ne pas afficher les symboles non-necessaires
                                m = "Il ne se passe rien"
                            else:
                                text2 = fontcouleur.render(touches[k], True,black)     #ici on dessine les symboles des caracteres sur le clavier
                                screen.blit(text2,[textx,texty])
                                textx += 43
                        x += 12
                        y += 12
                        textx = 16
                        texty += 43
                        
                if symbol == 1:                     #meme logique de dessin des caracteres, mais avec les symboles
                    for i in range(0,5):        
                        for k in range(x,y):
                            if k >= len(symkeys):break
                            if (k == 22 or k == 23 or k == 35 or k == 47 or k == 59):
                                m = "Il ne se passe rien"
                            else:
                                text2 = fontcouleur.render(symkeys[k], True,black)
                                screen.blit(text2,[textx,texty])
                                textx += 43
                        x += 12
                        y += 12
                        textx = 16
                        texty += 43        

                pygame.display.flip()       #update l'image de la fenetre
                # --------------------------------- #
                clock.tick(120)             #refresh l'image 120x par seconde
        
        except IndexError:                  #gestion d'erreur si on clique dans la case de texte du clavier
            print "en dehors du clavier"

    return mode_ecran, Message, couleurclavier, couleurspace, couleurshift,couleurmaj,Message1,Message2,Message3,Message4,Message5,Message6,Message7,Message8


#######################--DEBUT DU PROGRAMME--############################
init()
MY_ADDR = 0xA

#############--COULEURS--##########################
#base
black = (0,0,0)
white = (255,255,255)

#rouges
red = (255,0,0)
lightred = (255,51,51)
persianred = (204,51,51)
hotpink = (255,105,180)
bloodorange = (255,102,51)
orange = (255,153,51)
ocre = (255,204,51)
jaune = (255,255,51)

#verts
lightgreen = (153,255,51)
green = (0,255,0)
aquamarine = (51,255,153)
turquoise = (48,213,200)
lezard = (20,204,133)


#bleus
paleblue = (51,153,255)
blue = (0,0,255)
lila = (218,211,255)
violet =(153,51,255)
mauve = (102,0,204)
marin = (19,63,104)

couleurs = {0:red, 1:lightred,2:persianred,
            3:hotpink,4:bloodorange,
            5:orange,6:ocre,7:jaune,8:lightgreen,
            9:green,10:aquamarine,11:turquoise,12:lezard,
            13:paleblue,14:blue,15:marin,16:lila,17:violet,18:mauve,19:black}

fond = black
selection1 = fond
selection2 = fond
selection3 = fond
selection4 = fond
selection5 = fond
selection6 = fond
selection7 = fond
selection8 = fond


couleurclavier = white
couleurspace = white
couleurshift = white
couleurmaj = white

################--Taille de la fenetre--############################
size = [520,280]
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

pygame.display.set_caption("Test Communication")  #nom de la fenetre

###############--Technicalites--####################################
dest = None

#Controle de refresh de l'ecran
clock = pygame.time.Clock()

#Police
font = pygame.font.Font(None, 35) #exemple, taille de la police, police doit etre mis
                                                             #dans le meme dossier que le programme
fontmessage = pygame.font.Font(None, 25)

fontcouleur = pygame.font.Font(None, 25)

Message = ""
Message1 = ""
Message2 = ""
Message3 = ""
Message4 = ""
Message5 = ""
Message6 = ""
Message7 = ""
Message8 = ""

global msg_to_send
global source
global msg_type
msg_to_send = []    #message que l'on envoie
source = MY_ADDR


#Array
TABW = 20       #largeur des cases du tableau graphique
TABH = 40       #hauteur
GRID = []       #declaration du tableau graphique

for row in range(5):    #ici on dessine le tableau
    GRID.append([])
    for column in range (26):
        GRID[row].append(0)
        

############--Programme principal--######################
while done == False:        #on observe si la valeur de fin du programme est toujours a false avant de continuer

    if(GPIO.input(22) == True):
        msg_status, pic_is = key_locking([0x6F])
        if msg_status == True:
            if pic_is == 0xa6:
                Msg = receive()
                print Msg
            if pic_is == 0x06:
                write_msg(msg_to_send)
                del msg_to_send[:]
        else:
            pass

    # -----Boucle principale
    try:
        for event in pygame.event.get():    #lutilisateur fait quelque chose
            if event.type == pygame.QUIT: #si lutilisateur clique pour fermer la page
                done = True
            elif event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_ESCAPE:    #sortie avec esc s'il y a un bug
                    done = True

        # -----Logique des appuis de touches
        
            elif event.type == pygame.MOUSEBUTTONDOWN:  #evenement d appui de la souris
                mouseposx = pygame.mouse.get_pos()[0]   #position de la souris en x
                mouseposy = pygame.mouse.get_pos()[1]   #et en y
                column = mouseposx // (TABW)   #ici on distribue les positions de la souris selon le tableau graphique
                row = mouseposy // (TABH)
                position = ((column)+(row*26))+1
                #print position

                if mode_ecran == 0 :
                    if (position >= 3 and position <= 5):
                        mode_ecran = 1  #jeu

                    if (position >= 30 and position <= 38):
                        mode_ecran = 2  #messagerie

                    if (position >= 55 and position <= 62):
                        mode_ecran = 3  #parametres

                    if (position >= 82 and position <= 85):
                        done = True  #quitter

                else:
                    action()

            # --------------------------------- 


            # ----- Logique de dessin du clavier
            affichage()
            
            pygame.display.flip()       #update l'image de la fenetre
            # --------------------------------- #
            clock.tick(120)             #refresh l'image 120x par seconde
    
    except IndexError:                  #gestion d'erreur si on clique dans la case de texte du clavier
        print "en dehors de la zone"
pygame.quit()
