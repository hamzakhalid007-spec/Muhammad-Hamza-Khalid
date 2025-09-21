package main;

import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

public class KeyHandler implements KeyListener {
    GamePanel gp;
    public boolean upPressed, downPressed, leftPressed, rightPressed, enterPressed, shotKeyPressed;

    //Debug
    boolean checkDrawTime = false;

    public KeyHandler(GamePanel gp){
        this.gp = gp;
    }

    @Override
    public void keyTyped(KeyEvent e) {
    }

    @Override
    public void keyPressed(KeyEvent e) {
        int code = e.getKeyCode();
        //Title Screen
        if(gp.gameState == gp.titleState){
            titleState(code);
        }
        //Play State
        else if(gp.gameState == gp.playState){
            playState(code);
        }
        //Pause State
        else if(gp.gameState == gp.pauseState){
            pauseState(code);
        }
        //Dialogue State
        else if(gp.gameState == gp.dialogueState){
            dialogueState(code);
        }
        //Character State
        else if (gp.gameState == gp.characterState){
            characterState(code);
        }
        //Option State
        else if (gp.gameState == gp.optionState){
            optionState(code);
        }
        //Game Over state
        else if (gp.gameState == gp.gameOverstate){
            gameOverState(code);
        }
        //Trade state
        else if (gp.gameState == gp.tradeState){
            tradeState(code);
        }
    }
    public void titleState(int code){
        if(gp.ui.titleScreenState == 0){
                if(code == KeyEvent.VK_W){
                    gp.ui.commandNum--;
                    if(gp.ui.commandNum < 0){
                        gp.ui.commandNum = 2;
                    }
                }
                if(code == KeyEvent.VK_S){
                    gp.ui.commandNum++;
                    if(gp.ui.commandNum > 2){
                        gp.ui.commandNum = 0;
                    }
                }
                if(code == KeyEvent.VK_ENTER){
                    if(gp.ui.commandNum == 0){
                        gp.ui.titleScreenState = 1;
                    }
                    if(gp.ui.commandNum == 1){
                        //Add later
                    }
                    if(gp.ui.commandNum == 2){
                        System.exit(0);
                    }
                }
            }
            else if(gp.ui.titleScreenState == 1){
                if(code == KeyEvent.VK_W){
                    gp.ui.commandNum--;
                    if(gp.ui.commandNum < 0){
                        gp.ui.commandNum = 3;
                    }
                }
                if(code == KeyEvent.VK_S){
                    gp.ui.commandNum++;
                    if(gp.ui.commandNum > 3){
                        gp.ui.commandNum = 0;
                    }
                }
                if(code == KeyEvent.VK_ENTER){
                    if(gp.ui.commandNum == 0){
                        System.out.println("Do some fighter stuff!");
                        gp.gameState = gp.playState;
                        gp.playMusic(0);
                    }
                    if(gp.ui.commandNum == 1){
                        System.out.println("Do some theif stuff!");
                        gp.gameState = gp.playState;
                        gp.playMusic(0);
                    }
                    if(gp.ui.commandNum == 2){
                        System.out.println("Do some sorcerer stuff!");
                        gp.gameState = gp.playState;
                        gp.playMusic(0);
                    }
                    if(gp.ui.commandNum == 3){
                        gp.ui.titleScreenState = 0;
                        gp.ui.commandNum = 0;
                    }
                }
            }
    }
    public void playState(int code){
        switch (code) {
            case KeyEvent.VK_W:
                upPressed = true;
                break;
            case KeyEvent.VK_S:
                downPressed = true;
                break;
            case KeyEvent.VK_A:
                leftPressed = true;
                break;
            case KeyEvent.VK_D:
                rightPressed = true;
                break;
            case KeyEvent.VK_P:
                gp.gameState = gp.pauseState;
                break;
            case KeyEvent.VK_C:
                gp.gameState = gp.characterState;
                break;
            default:
                break;
        }
        if (code == KeyEvent.VK_ENTER){
            enterPressed = true;
        }
        if (code == KeyEvent.VK_F){
            shotKeyPressed = true;
        }
        if (code == KeyEvent.VK_ESCAPE){
            gp.gameState = gp.optionState;
        }
        //Debug
        if(code == KeyEvent.VK_T){
            if(checkDrawTime == false){
                checkDrawTime = true;
            } else if(checkDrawTime == true){
                checkDrawTime = false;
            }
        }
        if(code == KeyEvent.VK_R){
            switch(gp.currentMap){
                case 0: gp.tileM.loadMap("/res/maps/worldV3.txt", 0); break;
                case 1: gp.tileM.loadMap("/res/maps/interior01.txt", 1); break;
            }
        }
    }
    public void pauseState(int code){
        if (code == KeyEvent.VK_P){
            gp.gameState = gp.playState;
        }
    }
    public void dialogueState(int code){
        if(code == KeyEvent.VK_ENTER){
            gp.gameState = gp.playState;
        }
    }
    public void characterState(int code){
        if(code == KeyEvent.VK_C){
            gp.gameState = gp.playState;
        }
        if(code == KeyEvent.VK_ENTER){
            gp.player.selectItem();
        }
        playerInventory(code);
    }
    public void optionState(int code){
        if(code == KeyEvent.VK_ESCAPE){
            gp.gameState = gp.playState;
        }
        if(code == KeyEvent.VK_ENTER){
            enterPressed = true;
        }
        int maxCommandNum = 0;
        switch(gp.ui.subState){
            case 0: maxCommandNum = 5; break;
            case 3: maxCommandNum = 1; break;

        }
        if(code == KeyEvent.VK_W){
            gp.ui.commandNum--;
            gp.playSE(8);
            if(gp.ui.commandNum < 0){
                gp.ui.commandNum = maxCommandNum;
            }
        }
        if(code == KeyEvent.VK_S){
            gp.ui.commandNum++;
            gp.playSE(8);
            if(gp.ui.commandNum > maxCommandNum){
                gp.ui.commandNum = 0;
            }
        }
        if(code == KeyEvent.VK_A) {
            if(gp.ui.subState == 0) {
                if(gp.ui.commandNum == 1 && gp.music.volumeScale > 0) {
                    gp.music.volumeScale--;
                    gp.music.checkVolume();
                    gp.playSE(8);
                }
                if(gp.ui.commandNum == 2 && gp.se.volumeScale > 0) {
                    gp.se.volumeScale--;
                    gp.se.checkVolume();
                    gp.playSE(8);
                }
            }
        }
        if(code == KeyEvent.VK_D) {
            if(gp.ui.subState == 0) {
                if(gp.ui.commandNum == 1 && gp.music.volumeScale < 5) {
                    gp.music.volumeScale++;
                    gp.music.checkVolume();
                    gp.playSE(8);
                }
                if(gp.ui.commandNum == 2 && gp.se.volumeScale < 5) {
                    gp.se.volumeScale++;
                    gp.se.checkVolume();
                    gp.playSE(8);
                }
            }
        }
    }
    public void gameOverState(int code){
        if(code == KeyEvent.VK_W){
            gp.ui.commandNum--;
            if(gp.ui.commandNum < 0){
                gp.ui.commandNum = 1;
            }
            gp.playSE(8);
        }
        if(code == KeyEvent.VK_S){
            gp.ui.commandNum++;
            if(gp.ui.commandNum > 1){
                gp.ui.commandNum = 0;
            }
            gp.playSE(8);
        }
        if(code == KeyEvent.VK_ENTER){
            if(gp.ui.commandNum == 0){
                gp.gameState = gp.playState;
                gp.retry();
                gp.playMusic(0);
            } else if(gp.ui.commandNum == 1){
                gp.gameState = gp.titleState;
                gp.restart();
            }
        }
    }
    public void tradeState(int code){
        if(code == KeyEvent.VK_ENTER){
            enterPressed = true;
        }
        if(gp.ui.subState == 0){
            if(code == KeyEvent.VK_W){
                gp.ui.commandNum--;
                if(gp.ui.commandNum < 0){
                    gp.ui.commandNum = 2;
                }
                gp.playSE(8);
            }
            if(code == KeyEvent.VK_S){
                gp.ui.commandNum++;
                if(gp.ui.commandNum > 2){
                    gp.ui.commandNum = 0;
                }
                gp.playSE(8);
            }
        }
        if(gp.ui.subState == 1){
            npcInventory(code);
            if(code == KeyEvent.VK_ESCAPE){
                gp.ui.subState = 0;
            }
        }
        if(gp.ui.subState == 2){
            playerInventory(code);
            if(code == KeyEvent.VK_ESCAPE){
                gp.ui.subState = 0;
            }
        }
    }
    public void playerInventory(int code){
        if(code == KeyEvent.VK_W){
            if(gp.ui.playerSlotRow != 0){
                gp.ui.playerSlotRow--;
                gp.playSE(8);
            }
        }
        if(code == KeyEvent.VK_A){
            if(gp.ui.playerSlotCol != 0){
                gp.ui.playerSlotCol--;
                gp.playSE(8);
            }
        }
        if(code == KeyEvent.VK_S){
            if(gp.ui.playerSlotRow != 3){
                gp.ui.playerSlotRow++;
                gp.playSE(8);
            }
        }
        if(code == KeyEvent.VK_D){
            if(gp.ui.playerSlotCol != 4){
                gp.ui.playerSlotCol++;
                gp.playSE(8);
            }
        }
    }
    public void npcInventory(int code){
        if(code == KeyEvent.VK_W){
            if(gp.ui.npcSlotRow != 0){
                gp.ui.npcSlotRow--;
                gp.playSE(8);
            }
        }
        if(code == KeyEvent.VK_A){
            if(gp.ui.npcSlotCol != 0){
                gp.ui.npcSlotCol--;
                gp.playSE(8);
            }
        }
        if(code == KeyEvent.VK_S){
            if(gp.ui.npcSlotRow != 3){
                gp.ui.npcSlotRow++;
                gp.playSE(8);
            }
        }
        if(code == KeyEvent.VK_D){
            if(gp.ui.npcSlotCol != 4){
                gp.ui.npcSlotCol++;
                gp.playSE(8);
            }
        }
    }
    @Override
    public void keyReleased(KeyEvent e) {
        int code = e.getKeyCode();
        if (code == KeyEvent.VK_W){
            upPressed = false;
        }
        else if (code == KeyEvent.VK_S){
            downPressed = false;
        }
        else if (code == KeyEvent.VK_A){
            leftPressed = false;
        }
        else if (code == KeyEvent.VK_D){
            rightPressed = false;
        }
        else if (code == KeyEvent.VK_F){
            shotKeyPressed = false;
        }
    }
}