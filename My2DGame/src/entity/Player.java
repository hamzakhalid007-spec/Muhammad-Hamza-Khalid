package entity;

import java.awt.AlphaComposite;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;
import java.io.IOException;
import javax.imageio.ImageIO;
import main.GamePanel;
import main.KeyHandler;
import main.UtilityTool;


public class Player extends Entity {
    KeyHandler keyH;

    public final int screenX;
    public final int screenY;
    int standCounter = 0;

    @SuppressWarnings("OverridableMethodCallInConstructor")
    public Player(GamePanel gp, KeyHandler keyH){
        super(gp);
        this.keyH = keyH;

        screenX = (gp.screenWidth/2) - (gp.tileSize/2);
        screenY = (gp.screenHeight/2) - (gp.tileSize/2);

        solidArea = new Rectangle();
        solidArea.x = 8;
        solidArea.y = 16;
        solidAreaDefaultX = solidArea.x;
        solidAreaDefaultY = solidArea.y;
        solidArea.width = 24;
        solidArea.height = 24;

        attackArea.width = 36;
        attackArea.height = 36;

        setDefaultValues();
        getPlayerImage();
        getPlayerAttackImage();
    } 
    public void setDefaultValues(){
        worldX = gp.tileSize * 23;
        worldY = gp.tileSize * 21;
        speed = 4;
        direction = "down";
        //Player Status
        maxLife = 6;
        life = maxLife;
    }
    public void getPlayerImage() {
        up1 = setup("/res/player/up_1", gp.tileSize, gp.tileSize);
        up2 = setup("/res/player/up_2", gp.tileSize, gp.tileSize);
        down1 = setup("/res/player/down_1", gp.tileSize, gp.tileSize);
        down2 = setup("/res/player/down_2", gp.tileSize, gp.tileSize);
        right1 = setup("/res/player/right_1", gp.tileSize, gp.tileSize);
        right2 = setup("/res/player/right_2", gp.tileSize, gp.tileSize);
        left1 = setup("/res/player/left_1", gp.tileSize, gp.tileSize);
        left2 = setup("/res/player/left_2", gp.tileSize, gp.tileSize);
    }
    public void getPlayerAttackImage(){
        attackUp1 = setup("/res/player/attack_up_1", gp.tileSize, gp.tileSize*2);
        attackUp2 = setup("/res/player/attack_up_2", gp.tileSize, gp.tileSize*2);
        attackDown1 = setup("/res/player/attack_down_1", gp.tileSize, gp.tileSize*2);
        attackDown2 = setup("/res/player/attack_down_2", gp.tileSize, gp.tileSize*2);
        attackLeft1 = setup("/res/player/attack_left_1", gp.tileSize*2, gp.tileSize);
        attackLeft2 = setup("/res/player/attack_left_2", gp.tileSize*2, gp.tileSize);
        attackRight1 = setup("/res/player/attack_right_1", gp.tileSize*2, gp.tileSize);
        attackRight2 = setup("/res/player/attack_right_2", gp.tileSize*2, gp.tileSize);

    }
    public BufferedImage setup(String imageName){
        UtilityTool uTool = new UtilityTool();
        BufferedImage image = null;

        try {
            image = ImageIO.read(getClass().getResourceAsStream(imageName +".png"));
            image = uTool.scaleImage(image, gp.tileSize, gp.tileSize);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return image;
    }
    public void update(){
        if(attacking){
            attacking();
        } 
        else if(keyH.upPressed == true ||  keyH.downPressed == true || keyH.leftPressed == true || keyH.rightPressed == true || keyH.enterPressed == true){
            if(keyH.upPressed == true){
                direction = "up"; }
            else if(keyH.downPressed == true){
                direction = "down"; }
            else if(keyH.leftPressed == true){
                direction = "left"; }
            else if(keyH.rightPressed == true){
                direction = "right"; }

            //Check tile collision
            collisionOn = false;
            gp.cChecker.checkTile(this);
            //Check object collision
            int objectIndex = gp.cChecker.checkObject(this, true);
            pickUpObject(objectIndex);
            //Check NPC collision
            int npcIndex = gp.cChecker.checkEntity(this, gp.npc);
            interactNPC(npcIndex);
            //Check monster collision
            int monsterIndex = gp.cChecker.checkEntity(this, gp.monster);
            contactMonster(monsterIndex);
        
            //Check event
            gp.eHandler.checkEvent();

            //If collision is false, player can move
            if (collisionOn == false && keyH.enterPressed == false){
                switch(direction){
                    case "up" -> worldY -= speed;
                    case "down" -> worldY += speed;
                    case "left" -> worldX -= speed;
                    case "right" -> worldX += speed;
                }
            }
            gp.keyH.enterPressed= false;

            spriteCounter++;
            if(spriteCounter > 12){
                if(spriteNum == 1){
                    spriteNum = 2;
                }
            else if(spriteNum == 2){
                    spriteNum = 1;
                }
                spriteCounter = 0;
            }
        } else {
            standCounter++;
            if(standCounter == 20){
                spriteNum = 1;
                standCounter = 0;
            }
        }
        if(invincible == true){
            invincibleCounter++;
            if(invincibleCounter > 60){
                invincible = false;
                invincibleCounter = 0;
            }
        }
    }
    public void interactNPC(int i){
        if(gp.keyH.enterPressed == true){
            if (i != 999) {
                gp.gameState = gp.dialogueState;
                gp.npc[i].speak();
            }
            else {
                gp.playSE(7);
                attacking = true;
            } 
        }
    }
    public void attacking(){
        spriteCounter++;
        if(spriteCounter < 5){
            spriteNum = 1;
        }
        if(spriteCounter > 5 && spriteCounter <= 25){
            spriteNum = 2;

            //Save current world x, y and solid area
            int currentWorldX = worldX;
            int currentWorldY = worldY;
            int solidAreaWidth = solidArea.width;
            int solidAreaHeigth = solidArea.height;
            //Adjust player's worldX/Y for attacking
            switch (direction) {
                case "up": worldY -= attackArea.height; break;
                case "down": worldY += attackArea.height; break;
                case "left": worldX -= attackArea.width; break;
                case "right": worldX += attackArea.width; break;          
            }
            //Attack area becomes solid area
            solidArea.width = attackArea.width;
            solidArea.height = attackArea.height;
            //Checking monster collision with updated worldX, worldY and solid area
            int monsterIndex = gp.cChecker.checkEntity(this, gp.monster);
            damageMonster(monsterIndex);
            //After checking collision, restoring the original data
            worldX = currentWorldX;
            worldY = currentWorldY;
            solidArea.width = solidAreaWidth;
            solidArea.height = solidAreaHeigth;
        }
        if(spriteCounter > 25){
            spriteNum = 1;
            spriteCounter = 0;
            attacking = false;
        }
    }
    public void pickUpObject(int i) {
        if (i != 999) {
            
        }
    }
    public void contactMonster(int i){
        if(i != 999){
            if(invincible == false){
                gp.playSE(6);
                life -= 1;
                invincible = true;
            }
        }
    }
    public void damageMonster(int i){
        if(i != 999){
            if(gp.monster[i].invincible == false){
                gp.playSE(5);
                gp.monster[i].life -= 1; 
                gp.monster[i].invincible = true;
                if(gp.monster[i].life <= 0){
                    gp.monster[i].dying = true;
                }
            }
        }
    }
    public void draw(Graphics2D g2){
        BufferedImage image = null;
        int tempScreenX = screenX;
        int tempScreenY = screenY;

        switch(direction){
            case "up" -> {
                if(attacking == false){
                    if(spriteNum == 1){image = up1;}
                    if(spriteNum == 2){image = up2;}
                }
                if(attacking == true){
                    tempScreenY = screenY - gp.tileSize;
                    if(spriteNum == 1){image = attackUp1;}
                    if(spriteNum == 2){image = attackUp2;}
                }
            }
            case "down" -> {
                if(attacking == false){
                    if(spriteNum == 1){image = down1;}
                    if(spriteNum == 2){image = down2;}
                }
                if(attacking == true){
                    if(spriteNum == 1){image = attackDown1;}
                    if(spriteNum == 2){image = attackDown2;}
                }
            }
            case "left" -> {
                if(attacking == false){
                    if(spriteNum == 1){image = left1;}
                    if(spriteNum == 2){image = left2;}
                }
                if(attacking == true){
                    tempScreenX = screenX - gp.tileSize;
                    if(spriteNum == 1){image = attackLeft1;}
                    if(spriteNum == 2){image = attackLeft2;}
                }
            }
            case "right" -> {
                if(attacking == false){
                    if(spriteNum == 1){image = right1;}
                    if(spriteNum == 2){image = right2;}
                }
                if(attacking == true){
                    if(spriteNum == 1){image = attackRight1;}
                    if(spriteNum == 2){image = attackRight2;}
                }
            }
        }
        if(invincible == true){
            g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, 0.4f));
        }
        g2.drawImage(image, tempScreenX, tempScreenY, null);

        g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, 1f));
    }
}