import pygame
pygame.init()

x = 768
y = 576
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('Gladiator Battle')

unscaledbackground = pygame.image.load("Arena.png")
background = pygame.transform.scale(unscaledbackground, (unscaledbackground.get_width() * 3, unscaledbackground.get_height() * 3))

class Spritesheet:
    def __init__(self, filename):
        print(filename)
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0,0),(x, y, w, h))
        return sprite

class Player:
    def __init__(self, screen, armor, sword, initialXPosition = 0, initialYPosition = 0, defaultCoinAmount = 0):
        self.screen = screen
        self.x = initialXPosition
        self.y = initialYPosition
        self.orientation = "Right"
        self.moving_left = False
        self.moving_right = False
        self.attacking = False
        self.attacked = False
        self.dead = True
        self.attackingAnimationFrameCounter = 0
        self.deathAnimationFrameCounter = 0
        self.deathAnimationFrameCooldownCounter = 0
        self.deathAnimationFrameCooldownValue = 10
        self.attackingAnimationFrameCooldownCounter = 0
        self.attackingAnimationFrameCooldownValue = 10
        self.attackCooldownCounter = 0
        self.attackCooldownValue = 50
        self.armor = armor
        self.sword = sword
        self.fullHealth = 0
        self.health = 1
        self.damage = 0
        self.coinAmount = defaultCoinAmount
        self.coinReduction = 0
        self.coinGainOnEnemyDeath = 15
        self.movementSpeed = 2
        self.spritesheetImageName = self.getSpriteSheetImageName(armor, sword)
        self.getHealthAndDamage(self.spritesheetImageName)

        self.deathSpritesheetName = "death.png"
        playerdeathspritesheet = Spritesheet(self.deathSpritesheetName)
        self.fullPlayerDeathAnimation = [playerdeathspritesheet.get_sprite(0, 0, 128, 128), playerdeathspritesheet.get_sprite(128, 0, 128, 128), playerdeathspritesheet.get_sprite(256, 0, 128, 128)]

        playerspritesheet = Spritesheet(self.spritesheetImageName)
        self.fullPlayerAnimation = [playerspritesheet.get_sprite(0, 0, 128, 128), playerspritesheet.get_sprite(128, 0, 128, 128), playerspritesheet.get_sprite(256, 0, 128, 128), playerspritesheet.get_sprite(384, 0, 128, 128)]
        
        self.imageright = self.fullPlayerAnimation[self.attackingAnimationFrameCounter]
        self.imageleft = pygame.transform.flip(self.fullPlayerAnimation[self.attackingAnimationFrameCounter], True, False)

    def update(self):
        self.coinManagement()
        self.deathAnimation()
        if not self.dead and not enemy.dead:
            self.move()
            self.attack()
            self.healthReduction()
            self.death()

    def blitme(self):
        if not self.dead:
            if self.orientation == "Right" and not self.attacking:
                self.screen.blit(self.imageright, (self.x, self.y))
            elif self.orientation == "Left" and not self.attacking:
                self.screen.blit(self.imageleft, (self.x, self.y))

    def move(self):
        if self.moving_left and self.x - self.movementSpeed >= 0:
            self.x -= self.movementSpeed
            self.orientation = "Left"
        elif self.moving_right and self.x + self.movementSpeed <= 675:
            self.x += self.movementSpeed
            self.orientation = "Right"

    def attack(self):
        if self.attackCooldownCounter < self.attackCooldownValue:
            self.attackCooldownCounter += 1
        
        if self.attackingAnimationFrameCooldownCounter < self.attackingAnimationFrameCooldownValue:
            self.attackingAnimationFrameCooldownCounter += 1

        if self.attackingAnimationFrameCounter > 3:
            self.attacking = False
            self.attacked = True
            self.attackingAnimationFrameCounter = 0
            self.attackCooldownCounter = 0
            currentAttackingAnimation = self.fullPlayerAnimation[0]
            if self.orientation == "Left":
                currentAttackingAnimation = pygame.transform.flip(self.fullPlayerAnimation[0], True, False)
            screen.blit(currentAttackingAnimation, (self.x, self.y))
            return

        if self.attacking and self.attackingAnimationFrameCounter <= 3:
            self.moving_left = False
            self.moving_right = False
            currentAttackingAnimation = self.fullPlayerAnimation[self.attackingAnimationFrameCounter]
            if self.orientation == "Left":
                    currentAttackingAnimation = pygame.transform.flip(self.fullPlayerAnimation[self.attackingAnimationFrameCounter], True, False)
            if self.attackingAnimationFrameCooldownCounter == self.attackingAnimationFrameCooldownValue:
                currentAttackingAnimation = self.fullPlayerAnimation[self.attackingAnimationFrameCounter]
                if self.orientation == "Left":
                    currentAttackingAnimation = pygame.transform.flip(self.fullPlayerAnimation[self.attackingAnimationFrameCounter], True, False)
                self.attackingAnimationFrameCooldownCounter = 0
                self.attackingAnimationFrameCounter += 1
            screen.blit(currentAttackingAnimation, (self.x, self.y))
    
    def healthReduction(self):
        if 0 <= self.x - enemy.x <= 50 and enemy.attacked:
            self.health -= enemy.damage
            print("Player health =", self.health) 
            enemy.attacked = False
        elif 0 <= enemy.x - self.x <= 50 and enemy.attacked:
            self.health -= enemy.damage
            print("Player health =", self.health) 
            enemy.attacked = False
        
    def death(self):
        if self.health <= 0:
            self.moving_left = False
            self.moving_right = False
            self.attacking = False
            self.attacked = False
            self.attackingAnimationFrameCounter = 0
            self.attackingAnimationFrameCooldownCounter = 0
            self.attackCooldownCounter = 0
            self.health = 0
            self.damage = 0
            self.dead = True
    
    def deathAnimation(self):
        if self.dead and self.deathAnimationFrameCounter <= 2 and roundNumber >= 1:
            currentDeathAnimation = self.fullPlayerDeathAnimation[self.deathAnimationFrameCounter]
            if self.deathAnimationFrameCooldownCounter == self.deathAnimationFrameCooldownValue:
                currentDeathAnimation = self.fullPlayerDeathAnimation[self.attackingAnimationFrameCounter]
                self.deathAnimationFrameCooldownCounter = 0
                self.deathAnimationFrameCounter += 1
            self.deathAnimationFrameCooldownCounter += 1
            screen.blit(currentDeathAnimation, (self.x, self.y- 5))
        elif self.dead and self.deathAnimationFrameCounter >= 2 and roundNumber >= 1:
            screen.blit(self.fullPlayerDeathAnimation[2], (self.x, self.y - 5))
 
    def coinManagement(self):
        if self.coinReduction > 0 and self.coinAmount - self.coinReduction >= 0:
            self.coinAmount -= self.coinReduction
            self.coinReduction = 0
            print("Player coin amount = ", self.coinAmount)
        
        if enemy.playerCoinGain:
            self.coinAmount += self.coinGainOnEnemyDeath
            enemy.playerCoinGain = False
            print("Player coin amount = ", self.coinAmount)

    def equipItem(self, armor, sword):
        self.armor = armor
        self.sword = sword
        self.spritesheetImageName = self.getSpriteSheetImageName(armor, sword)
        self.getHealthAndDamage(self.spritesheetImageName)
        
        playerspritesheet = Spritesheet(self.spritesheetImageName)
        self.fullPlayerAnimation = [playerspritesheet.get_sprite(0, 0, 128, 128), playerspritesheet.get_sprite(128, 0, 128, 128), playerspritesheet.get_sprite(256, 0, 128, 128), playerspritesheet.get_sprite(384, 0, 128, 128)]
        
        self.imageright = self.fullPlayerAnimation[self.attackingAnimationFrameCounter]
        self.imageleft = pygame.transform.flip(self.fullPlayerAnimation[self.attackingAnimationFrameCounter], True, False)
        
        
    def getSpriteSheetImageName(self, armor, sword):
        if armor == "la" and sword == "ws":
            return "LA WS.png"
        elif armor == "la" and sword == "is":
            return "LA IS.png"
        elif armor == "la" and sword == "gs":
            return "LA GS.png"
        elif armor == "ia" and sword == "ws":
            return "IA WS.png"
        elif armor == "ia" and sword == "is":
            return "IA IS.png"
        elif armor == "ia" and sword == "gs":
            return "IA GS.png"
        elif armor == "ga" and sword == "ws":
            return "GA WS.png"
        elif armor == "ga" and sword == "is":
            return "GA IS.png"
        elif armor == "ga" and sword == "gs":
            return "GA GS.png"
    
    def getHealthAndDamage(self, spritesheetImageName):
        if spritesheetImageName == "LA WS.png":
            self.fullHealth = 35
            self.health = 35
            self.damage = 5
        elif spritesheetImageName == "LA IS.png":
            self.fullHealth = 35
            self.health = 35
            self.damage = 10
        elif spritesheetImageName == "LA GS.png":
            self.fullHealth = 35
            self.health = 35
            self.damage = 15
        elif spritesheetImageName == "IA WS.png":
            self.fullHealth = 55
            self.health = 55
            self.damage = 5
        elif spritesheetImageName == "IA IS.png":
            self.fullHealth = 55
            self.health = 55
            self.damage = 10
        elif spritesheetImageName == "IA GS.png":
            self.fullHealth = 55
            self.health = 55
            self.damage = 15
        elif spritesheetImageName == "GA WS.png":
            self.fullHealth = 80
            self.health = 80
            self.damage = 5
        elif spritesheetImageName == "GA IS.png":
            self.fullHealth = 80
            self.health = 80
            self.damage = 10
        elif spritesheetImageName == "GA GS.png":
            self.fullHealth = 80
            self.health = 80
            self.damage = 15

class Enemy:
    def __init__(self, screen, armor, sword, initialXPosition = 0, initialYPosition = 0):
        self.screen = screen
        self.x = initialXPosition
        self.y = initialYPosition
        self.orientation = "Left"
        self.moving_left = False
        self.moving_right = False
        self.attacking = False
        self.attacked = False
        self.dead = True
        self.deathAnimationFrameCounter = 0
        self.deathAnimationFrameCooldownCounter = 0
        self.deathAnimationFrameCooldownValue = 10
        self.attackingAnimationFrameCounter = 0
        self.attackCooldownCounter = 0
        self.attackCooldownValue = 50
        self.attackingAnimationFrameCooldownCounter = 0
        self.attackingAnimationFrameCooldownValue = 10
        self.armor = armor
        self.sword = sword
        self.health = 1
        self.damage = 0
        self.playerCoinGain = False
        self.movementSpeed = 1.3
        self.spritesheetImageName = self.getSpriteSheetImageName(armor, sword)
        self.getHealthAndDamage(self.spritesheetImageName)

        self.deathSpritesheetName = "death.png"
        enemydeathspritesheet = Spritesheet(self.deathSpritesheetName)
        self.fullEnemyDeathAnimation = [enemydeathspritesheet.get_sprite(0, 0, 128, 128), enemydeathspritesheet.get_sprite(128, 0, 128, 128), enemydeathspritesheet.get_sprite(256, 0, 128, 128)]

        enemySpritesheet = Spritesheet(self.spritesheetImageName)
        self.fullEnemyAnimation = [enemySpritesheet.get_sprite(0, 0, 128, 128), enemySpritesheet.get_sprite(128, 0, 128, 128), enemySpritesheet.get_sprite(256, 0, 128, 128), enemySpritesheet.get_sprite(384, 0, 128, 128)]
        
        self.imageright = self.fullEnemyAnimation[self.attackingAnimationFrameCounter]
        self.imageleft = pygame.transform.flip(self.imageright, True, False)

    def update(self):
        self.deathAnimation()
        if not self.dead and not player.dead:
            self.move()
            self.followPlayer()
            self.attack()
            self.healthReduction()
            self.death()

    def blitme(self):
        if not self.dead:
            if self.orientation == "Right" and not self.attacking:
                self.screen.blit(self.imageright, (self.x, self.y))
            elif self.orientation == "Left" and not self.attacking:
                self.screen.blit(self.imageleft, (self.x, self.y))
    
    def followPlayer(self):
        if player.x + 40 < self.x:
            self.moving_left = True
            self.moving_right = False
            self.attacking = False
        elif player.x - 40 > self.x:
            self.moving_left = False
            self.moving_right = True
            self.attacking = False
        elif player.x + 40 >= self.x or player.x - 40 <= self.x and self.attackCooldownCounter == self.attackCooldownValue:
            self.moving_left = False
            self.moving_right = False
            self.attacking = True        

    def move(self):
        if self.moving_left and self.x - self.movementSpeed >= 0:
            self.x -= self.movementSpeed
            self.orientation = "Left"
        elif self.moving_right and self.x + self.movementSpeed <= 675:
            self.x += self.movementSpeed
            self.orientation = "Right"

    def attack(self):
            if self.attackCooldownCounter < self.attackCooldownValue:
                self.attackCooldownCounter += 1
                self.attacking = False

            if self.attackingAnimationFrameCooldownCounter < self.attackingAnimationFrameCooldownValue:
                self.attackingAnimationFrameCooldownCounter += 1

            if self.attackingAnimationFrameCounter > 3:
                self.attacking = False
                self.attacked = True
                self.attackingAnimationFrameCounter = 0
                self.attackCooldownCounter = 0
                currentAttackingAnimation = self.fullEnemyAnimation[0]
                if self.orientation == "Left":
                    currentAttackingAnimation = pygame.transform.flip(self.fullEnemyAnimation[0], True, False)
                screen.blit(currentAttackingAnimation, (self.x, self.y))
                return

            if self.attacking and self.attackingAnimationFrameCounter <= 3:
                currentAttackingAnimation = self.fullEnemyAnimation[self.attackingAnimationFrameCounter]
                if self.orientation == "Left":
                        currentAttackingAnimation = pygame.transform.flip(self.fullEnemyAnimation[self.attackingAnimationFrameCounter], True, False)
                if self.attackingAnimationFrameCooldownCounter == self.attackingAnimationFrameCooldownValue:
                    currentAttackingAnimation = self.fullEnemyAnimation[self.attackingAnimationFrameCounter]
                    if self.orientation == "Left":
                        currentAttackingAnimation = pygame.transform.flip(self.fullEnemyAnimation[self.attackingAnimationFrameCounter], True, False)
                    self.attackingAnimationFrameCooldownCounter = 0
                    self.attackingAnimationFrameCounter += 1
                screen.blit(currentAttackingAnimation, (self.x, self.y))
    
    def healthReduction(self):
        if 0 <= self.x - player.x <= 50 and player.orientation == "Right" and player.attacked:
            self.health -= player.damage
            print("Enemy health =", self.health)
            player.attacked = False 
        elif 0 <= player.x - self.x <= 50 and player.orientation == "Left" and player.attacked :
            self.health -= player.damage
            print("Enemy health =", self.health) 
            player.attacked = False
        
    def death(self):
        if self.health <= 0:
            self.moving_left = False
            self.moving_right = False
            self.attacking = False
            self.attacked = False
            self.attackingAnimationFrameCounter = 0
            self.attackingAnimationFrameCooldownCounter = 0
            self.attackCooldownCounter = 0
            self.health = 0
            self.damage = 0
            self.dead = True
            self.playerCoinGain = True

    def deathAnimation(self):
        if self.dead and self.deathAnimationFrameCounter <= 2 and roundNumber >= 1:
            currentDeathAnimation = self.fullEnemyDeathAnimation[self.deathAnimationFrameCounter]
            if self.deathAnimationFrameCooldownCounter == self.deathAnimationFrameCooldownValue:
                currentDeathAnimation = self.fullEnemyDeathAnimation[self.attackingAnimationFrameCounter]
                self.deathAnimationFrameCooldownCounter = 0
                self.deathAnimationFrameCounter += 1
            self.deathAnimationFrameCooldownCounter += 1
            screen.blit(currentDeathAnimation, (self.x + 25, self.y - 5))
        elif self.dead and self.deathAnimationFrameCounter >= 2 and roundNumber >= 1:
            screen.blit(self.fullEnemyDeathAnimation[2], (self.x + 25, self.y - 5))
            
    def getSpriteSheetImageName(self, armor, sword):
        if armor == "la" and sword == "ws":
            return "LA WS.png"
        elif armor == "la" and sword == "is":
            return "LA IS.png"
        elif armor == "la" and sword == "gs":
            return "LA GS.png"
        elif armor == "ia" and sword == "ws":
            return "IA WS.png"
        elif armor == "ia" and sword == "is":
            return "IA IS.png"
        elif armor == "ia" and sword == "gs":
            return "IA GS.png"
        elif armor == "ga" and sword == "ws":
            return "GA WS.png"
        elif armor == "ga" and sword == "is":
            return "GA IS.png"
        elif armor == "ga" and sword == "gs":
            return "GA GS.png"
        
    def getHealthAndDamage(self, spritesheetImageName):
        if spritesheetImageName == "LA WS.png":
            self.health = 25
            self.damage = 5
        elif spritesheetImageName == "LA IS.png":
            self.health = 25
            self.damage = 10
        elif spritesheetImageName == "LA GS.png":
            self.health = 25
            self.damage = 15
        elif spritesheetImageName == "IA WS.png":
            self.health = 40
            self.damage = 5
        elif spritesheetImageName == "IA IS.png":
            self.health = 40
            self.damage = 10
        elif spritesheetImageName == "IA GS.png":
            self.health = 40
            self.damage = 15
        elif spritesheetImageName == "GA WS.png":
            self.health = 60
            self.damage = 5
        elif spritesheetImageName == "GA IS.png":
            self.health = 60
            self.damage = 10
        elif spritesheetImageName == "GA GS.png":
            self.health = 60
            self.damage = 15

class Shop:
    def __init__(self, screen, currentArmour, currentSword, x = 192, y = 168):
        self.screen = screen
        self.x = x
        self.y = y
        self.sprite = pygame.image.load("Shop.png")
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.brown = (5, 0, 0)

        self.isOpened = False
        self.boughtItems = [currentArmour, currentSword]
        self.ownedItems = []

    def sellItem(self, player, event):
        if event.key == pygame.K_1:
            self.performTransaction(player, 30, "ia")
        elif event.key == pygame.K_2:
            self.performTransaction(player, 15, "is")
        elif event.key == pygame.K_3:
            self.performTransaction(player, 60, "ga")
        elif event.key == pygame.K_4:
            self.performTransaction(player, 45, "gs")
            
    def performTransaction(self, player, amount, newItemName):
        if newItemName in self.ownedItems:
            self.checkAndEquipPlayerEquipment(player, newItemName)
                
        elif newItemName not in self.boughtItems and player.coinAmount >= amount and newItemName not in self.ownedItems:
            player.coinAmount -= amount
            self.checkAndEquipPlayerEquipment(player, newItemName)
            self.ownedItems.append(newItemName)

    def checkAndEquipPlayerEquipment(self, player, newItemName):
        if newItemName == "ia":
            player.equipItem("ia", player.sword)
        if newItemName == "is":
            player.equipItem(player.armor, "is")
        if newItemName == "ga":
            player.equipItem("ga", player.sword)
        if newItemName == "gs":
            player.equipItem(player.armor, "gs")
                

    def openShop(self):
        self.isOpened = True
        self.blitme()

    def closeShop(self):
        self.isOpened = False

    def blitme(self):
        if self.isOpened:
            self.screen.blit(self.sprite, (self.x, self.y))
            self.displayedNumber = str(player.coinAmount)
            self.text = self.font.render(self.displayedNumber, True, self.brown)
            self.screen.blit(self.text, (self.x + 40, self.y + 13))

playerCoinAmount = 0  
playerArmor = "la"
playerSword = "ws"
enemyArmor = "la"
enemySword = "ws"
initialArmor = "la"
initialSword = "ws"

shop = Shop(screen, initialArmor, initialSword)
player = Player(screen, playerArmor, playerSword, 10, 450, playerCoinAmount)
enemy = Enemy(screen, enemyArmor, enemySword, 650, 450)

enemyArmorNumber = -2
enemySwordNumber = -1
roundEnemyEquipment = ["la", "ws", "la", "is", "la", "is", "ia", "is", "ia", "is", "ia", "is", "ia", "gs", "ia", "gs", "ia", "gs", "ia", "gs", "ga", "gs"]
roundNumber = 0

font = pygame.font.Font('freesansbold.ttf', 32)
red = (255,0,0)
black = (0, 0, 0)
green = (8, 143, 143)

battle = False
lost = False
running = True

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
    
    screen.blit(background, (0, 0))

    if roundNumber == 0 and not battle:
        displayedText = "Press enter to start"
        text = font.render(displayedText, True, green, black)
        screen.blit(text, (235, 320))

    if roundNumber == 11 and not battle:
        player.blitme()
        displayedText = "Victory"
        text = font.render(displayedText, True, green, black)
        screen.blit(text, (320, 320))

    if not battle and roundNumber != 11 and roundNumber != 0 and not lost:
        player.blitme()
        shop.openShop()
        shop.blitme()
    elif battle:
        player.blitme()
        enemy.blitme()

        if enemy.dead:
            battle = False
    
    if player.dead and battle:
        lost = True
        displayedText = "Defeat"
        text = font.render(displayedText, True, red, black)
        screen.blit(text, (320, 320))

    for event in pygame.event.get(): 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and battle:
                player.moving_right = True
                player.moving_left = False

            if event.key == pygame.K_LEFT:
                player.moving_left = True
                player.moving_right = False

            if event.key == pygame.K_UP and player.attackCooldownCounter == player.attackCooldownValue and battle:
                player.attacking = True

            if event.key == pygame.K_KP_ENTER and not battle and roundNumber != 11 and not lost:
                shop.closeShop()
                battle = True
                roundNumber += 1
                enemyArmorNumber += 2
                enemySwordNumber += 2
                enemyArmor = roundEnemyEquipment[enemyArmorNumber]
                enemySword = roundEnemyEquipment[enemySwordNumber]
                enemy.dead = False
                player.dead = False
                if roundNumber > 1:
                    enemy.sword = enemySword
                    enemy.armor = enemyArmor
                    enemy.spritesheetImageName = enemy.getSpriteSheetImageName(enemy.armor, enemy.sword)
                    enemy.getHealthAndDamage(enemy.spritesheetImageName)
                    enemySpritesheet = Spritesheet(enemy.spritesheetImageName)
                    enemy.fullEnemyAnimation = [enemySpritesheet.get_sprite(0, 0, 128, 128), enemySpritesheet.get_sprite(128, 0, 128, 128), enemySpritesheet.get_sprite(256, 0, 128, 128), enemySpritesheet.get_sprite(384, 0, 128, 128)]
                    enemy.imageright = enemy.fullEnemyAnimation[enemy.attackingAnimationFrameCounter]
                    enemy.imageleft = pygame.transform.flip(enemy.imageright, True, False)
                    player.deathAnimationFrameCounter = 0
                    player.health = player.fullHealth
                    player.x = 10
                    player.y = 450
                    player.orientation = "Right"
                    enemy.deathAnimationFrameCounter = 0
                    enemy.x = 650
                    enemy.y = 450
                    enemy.orientation = "Left"

            if shop.isOpened and (event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4) and not battle:
                shop.sellItem(player, event)

        if event.type == pygame.KEYUP and battle:
            if event.key == pygame.K_RIGHT:
                player.moving_right = False

            if event.key == pygame.K_LEFT and battle:
                player.moving_left = False

    player.update()
    enemy.update()
    pygame.display.flip()