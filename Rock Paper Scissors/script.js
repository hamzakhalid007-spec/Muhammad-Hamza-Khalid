let userScore = 0;
let compScore = 0;

const choices = document.querySelectorAll(".choice");
const msg = document.querySelector("#msg");
const userBox = document.querySelector("#user-score");
const compBox = document.querySelector("#comp-score");

const genCompChoice = () =>{
    const options = ["rock", "paper", "scissor"];
    const randId = Math.floor(Math.random() * 3);
    return options[randId];
};

const drawGame = () =>{
    msg.innerText = "Game was drawn. Play again.";
    msg.style.backgroundColor = "#081b31";
};

const capitalizeFirstLetter = (str) =>{
  return str.charAt(0).toUpperCase() + str.slice(1);
};

const showWinner = (userWin, userChoice, compChoice) =>{
    if(userWin){
        userScore++;
        userBox.innerText = userScore;
        msg.innerText = `You win! Your ${userChoice} beats ${compChoice}.`;
        msg.style.backgroundColor = "green";
    } else {
        compScore++;
        compBox.innerText = compScore;
        compChoice = capitalizeFirstLetter(compChoice);
        msg.innerText = `You lose. ${compChoice} beats your ${userChoice}.`;
        msg.style.backgroundColor = "red";
    }
};

const playGame = (userChoice) =>{
    const compChoice = genCompChoice();

    if(userChoice === compChoice){
        drawGame();
    } else {
        let userWin = true;
        if(userChoice === "rock"){
            userWin = compChoice === "paper" ? false : true;  
        } else if(userChoice === "paper"){
            userWin = compChoice === "scissor" ? false : true;
        } else {
            userWin = compChoice === "rock" ? false : true;
        }
        showWinner(userWin, userChoice, compChoice);
    }
};

choices.forEach((choice) => {
    choice.addEventListener("click", () =>{
        const userChoice = choice.getAttribute("id");
        playGame(userChoice);
    })
})