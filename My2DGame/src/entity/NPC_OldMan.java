package entity;

import java.util.Random;
import main.GamePanel;

public class NPC_OldMan extends Entity {
    public NPC_OldMan(GamePanel gp){
        super(gp);
        direction = "down";
        speed = 1;
        getImage();
        setDialogue();
    }
    public void getImage() {
        up1 = setup("/res/oldman_npc/up_1", gp.tileSize, gp.tileSize);
        up2 = setup("/res/oldman_npc/up_2", gp.tileSize, gp.tileSize);
        down1 = setup("/res/oldman_npc/down_1", gp.tileSize, gp.tileSize);
        down2 = setup("/res/oldman_npc/down_2", gp.tileSize, gp.tileSize);
        right1 = setup("/res/oldman_npc/right_1", gp.tileSize, gp.tileSize);
        right2 = setup("/res/oldman_npc/right_2", gp.tileSize, gp.tileSize);
        left1 = setup("/res/oldman_npc/left_1", gp.tileSize, gp.tileSize);
        left2 = setup("/res/oldman_npc/left_2", gp.tileSize, gp.tileSize);
    }
    public void setDialogue(){
        dialogues[0] = "Hello lad.";
        dialogues[1] = "So you have come to this island to\nfind the treasure?";
        dialogues[2] = "I used to be a great wizard but now...\nI'm a bit too old for taking an adventure.";
        dialogues[3] = "Well good luck on you.";
    }
    public void setAction(){
            actionLockCounter++;
            if(actionLockCounter == 30){
                Random random = new Random();
                int i = random.nextInt(100) + 1;
                if(i <= 25){
                    direction = "up";
                } else if(i > 25 && i <= 50){
                    direction = "down";
                } else if(i > 50 && i <= 75){
                    direction = "left";
                } else if(i > 75 && i<= 100){
                    direction = "right";
                }
                actionLockCounter = 0;
            }
        }
    
    public void speak(){
        super.speak();
    }
}