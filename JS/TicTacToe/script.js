let boxes = document.querySelectorAll(".box");
let resetButton = document.querySelector("#reset");
let newButton = document.querySelector("#new-btn");
let msgContainer = document.querySelector(".msg-container");
let msg = document.querySelector("#msg");
let buttonsClicked = 0;
let winner = false;
let turn0 = true;

const winPattern = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
];

boxes.forEach((box) => {
    box.addEventListener("click", () => {
        if (turn0) box.innerText = "O";
        else box.innerText = "X";
        
        turn0 = !turn0;
        buttonsClicked++;
        box.disabled = true;
        checkWinner();
    });
});

const resetGame = () => {
    turn0 = true;
    buttonsClicked = 0;
    winner = false;
    enableBtns();
    msgContainer.classList.add("hide");
};

const disableBtns = () => {
    for (let box of boxes) box.disabled = true;
};

const enableBtns = () => {
    for (let box of boxes) {
        box.disabled = false;
        box.innerText = "";
    }
};

const showWinner = (winner) => {
    msg.innerText = `Congratulations, Winner is ${winner}`;
    msgContainer.classList.remove("hide");
    disableBtns();
};

const drawMsg = () => {
    msg.innerText = "Game has been drawn!";
    msgContainer.classList.remove("hide");
    disableBtns();
};

const checkWinner = () => {
    for (let pattern of winPattern) {
        let pos1Val = boxes[pattern[0]].innerText;
        let pos2Val = boxes[pattern[1]].innerText;
        let pos3Val = boxes[pattern[2]].innerText;

        if (pos1Val && pos2Val && pos3Val && pos1Val === pos2Val && pos2Val === pos3Val) {
            showWinner(pos1Val);
            winner = true;
            return;
        }
    }

    if (buttonsClicked === 9 && !winner) drawMsg();
};

newButton.addEventListener("click", resetGame);
resetButton.addEventListener("click", resetGame);