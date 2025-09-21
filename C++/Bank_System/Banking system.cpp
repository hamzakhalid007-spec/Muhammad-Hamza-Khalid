#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <filesystem>
#include <iomanip>
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <SFML/Window.hpp>

using namespace std;
using namespace sf;

const string DATA_FILE = "D:/Accounts";

struct Account {
    int pin, account_number, balance;
    string full_name, address, phone_number;
};

void options_window(RenderWindow& window, Font& font);
void create_account(RenderWindow& window, Font& font, const string& folder_path);
void deposit_cash(RenderWindow& window, Font& font, const string& folder_path);
void withdraw_cash(RenderWindow& window, Font& font, const string& folder_path);
void view_account_details(RenderWindow& window, Font& font, const string& folder_path);
void pay_utility_bill(RenderWindow& window, Font& font, const string& folder_path);
void show_transaction_history(RenderWindow& window, Font& font, const string& folder_path);

int main() {
    RenderWindow window(VideoMode(1920, 1080), "Banking Management System");
    Font font;
    if (!font.loadFromFile("D:/Coding/ConsoleApplication2/x64/Debug/arial.ttf")) {
        cout << "Error loading font!";
        return -1;
    }

    // Welcome screen text
    Text welcome("Welcome to Online Banking System", font, 70);
    welcome.setPosition(420, 450);
    welcome.setFillColor(Color::Black);

    Text enter("Press Enter to continue", font, 33);
    enter.setPosition(800, 700);
    enter.setFillColor(Color::Black);

    bool blinking_text = true;
    Clock clock;

    while (window.isOpen()) {
        Event evnt;
        while (window.pollEvent(evnt)) {
            if (evnt.type == Event::Closed)
                window.close();

            if (evnt.type == Event::KeyPressed && evnt.key.code == Keyboard::Enter) {
                options_window(window, font);
                return 0;
            }
        }

        // Blinking text logic
        if (clock.getElapsedTime().asSeconds() >= 0.5f) {
            blinking_text = !blinking_text;
            clock.restart();
        }

        // Drawing welcome screen
        window.clear(Color::White);
        window.draw(welcome);
        if (blinking_text) {
            window.draw(enter);
        }
        window.display();
    }

    return 0;
}

void options_window(RenderWindow& window, Font& font) {
    Text options(
        "Welcome to the options screen!\n\n"
        "Press appropriate number key for respective task:\n\n"
        "1. Create a new account\n"
        "2. Deposit money\n"
        "3. Withdraw money\n"
        "4. Check account details\n"
        "5. Bill payment\n"
        "6. Transaction history\n"
        "7. Exit",
        font, 40
    );
    options.setFillColor(Color::Black);
    options.setPosition(550, 250);

    while (window.isOpen()) {
        Event evnt;
        while (window.pollEvent(evnt)) {
            if (evnt.type == Event::Closed) {
                window.close();
            }

            // Handle input for the options screen
            if (evnt.type == Event::KeyPressed) {
                if (evnt.key.code == Keyboard::Num7) {
                    window.close(); // Close the program on pressing '7'
                }
                else if (evnt.key.code == Keyboard::Num1)
                {
                    create_account(window, font, DATA_FILE);
                    continue;
                }
                else if (evnt.key.code == Keyboard::Num2)
                {
                    deposit_cash(window, font, DATA_FILE);
                    continue;
                }
                else if (evnt.key.code == Keyboard::Num3)
                {
                    withdraw_cash(window, font, DATA_FILE);
                    continue;
                }
                else if (evnt.key.code == Keyboard::Num4)
                {
                    view_account_details(window, font, DATA_FILE);
                    continue;
                }
                else if (evnt.key.code == Keyboard::Num5)
                {
                    pay_utility_bill(window, font, DATA_FILE);
                    continue;
                }
                else if (evnt.key.code == Keyboard::Num6)
                {
                    show_transaction_history(window, font, DATA_FILE);
                    continue;
                }
            }
        }

        // Drawing the options screen
        window.clear(Color::White);
        window.draw(options);
        window.display();
    }
}


void create_account(RenderWindow& window, Font& font, const string& folder_path) {
    // Ensure the folder exists
    if (!filesystem::exists(folder_path)) {
        filesystem::create_directories(folder_path);
    }

    // Text objects
    Text instructions("Enter account details (Press Enter after each field):", font, 30);
    instructions.setFillColor(Color::Black);
    instructions.setPosition(550, 300);

    Text input_field("", font, 30);
    input_field.setFillColor(Color::Black);
    input_field.setPosition(550, 350);

    Text feedback("", font, 25);
    feedback.setFillColor(Color::Red);
    feedback.setPosition(550, 600);

    // Variables to store input
    Account new_account;
    string current_input = "";
    int step = 0;

    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
            }

            // Handle text input
            if (event.type == Event::TextEntered) {
                if (event.text.unicode == '\b' && !current_input.empty()) { // Backspace
                    current_input.pop_back();
                }
                else if (event.text.unicode < 128 && event.text.unicode != '\b') {
                    current_input += static_cast<char>(event.text.unicode);
                }
            }

            // Handle Enter key to move to the next step
            if (event.type == Event::KeyPressed && event.key.code == Keyboard::Enter) {
                switch (step) {
                case 0: { // Enter account number
                    new_account.account_number = stoi(current_input);

                    // Check if account file already exists
                    string file_path = folder_path + "/" + to_string(new_account.account_number) + ".txt";
                    if (filesystem::exists(file_path)) {
                        feedback.setString("Account number already exists! Enter a different account number.");
                        continue;
                    }
                    else {
                        feedback.setString("Account Number saved!");
                        step++;
                    }
                    break;
                }
                case 1: // Enter full name
                    new_account.full_name = current_input;
                    feedback.setString("Full Name saved!");
                    step++;
                    break;
                case 2: // Enter address
                    new_account.address = current_input;
                    feedback.setString("Address saved!");
                    step++;
                    break;
                case 3: // Enter phone number
                    new_account.phone_number = current_input;
                    feedback.setString("Phone Number saved!");
                    step++;
                    break;
                case 4: // Enter PIN
                    new_account.pin = stoi(current_input);
                    feedback.setString("PIN saved!");
                    step++;
                    break;
                case 5: // Enter initial balance
                    new_account.balance = stoi(current_input);
                    feedback.setString("Initial balance saved! Saving account...");
                    step++;
                    break;
                case 6: // Save the account
                {
                    string file_path = folder_path + "/" + to_string(new_account.account_number) + ".txt";
                    ofstream account_file(file_path);
                    if (account_file) {
                        // Ensure that account information is written just once
                        account_file << "Account Number: " << new_account.account_number << endl;
                        account_file << "Full Name: " << new_account.full_name << endl;
                        account_file << "Address: " << new_account.address << endl;
                        account_file << "Phone Number: " << new_account.phone_number << endl;
                        account_file << "PIN: " << new_account.pin << endl;
                        account_file << "Balance: " << new_account.balance << endl;

                        feedback.setString("Account saved successfully!");
                    }
                    else {
                        feedback.setString("Error saving account file.");
                    }
                    account_file.close();
                }
                step++;
                break;
                default:
                    return; // Exit the account creation screen
                }
                current_input = ""; // Reset input for the next field
            }
        }

        // Update input field text
        input_field.setString(current_input);

        // Update instructions
        switch (step) {
        case 0: instructions.setString("Enter Account Number (10 digits):"); break;
        case 1: instructions.setString("Enter Full Name:"); break;
        case 2: instructions.setString("Enter Address:"); break;
        case 3: instructions.setString("Enter Phone Number:"); break;
        case 4: instructions.setString("Enter PIN (4 digits):"); break;
        case 5: instructions.setString("Enter Initial Balance:"); break;
        case 6: instructions.setString("Saving account... Press Enter to continue."); break;
        default: instructions.setString("Account creation complete!"); break;
        }

        // Render the screen
        window.clear(Color::White);
        window.draw(instructions);
        window.draw(input_field);
        window.draw(feedback);
        window.display();
    }
}


// Function to load account data from file
bool load_account_from_file(const string& file_path, Account& account) {
    ifstream account_file(file_path);
    if (account_file) {
        string line;
        while (getline(account_file, line)) {
            stringstream ss(line);
            string key;
            ss >> key;
            if (key == "Account") ss >> key >> account.account_number;
            else if (key == "Full") {
                ss.ignore(6); // Skip "Full Name:"
                getline(ss, account.full_name);
            }
            else if (key == "Address:") getline(ss, account.address);
            else if (key == "Phone") getline(ss, account.phone_number);
            else if (key == "PIN:") ss >> account.pin;
            else if (key == "Balance:") ss >> account.balance;
        }
        return true;
    }
    return false;
}

// Function to save account data to file
void save_account_to_file(const string& file_path, const Account& account) {
    ofstream account_file(file_path);
    if (account_file) {
        account_file << "Account Number: " << account.account_number << endl;
        account_file << "Full Name: " << account.full_name << endl;
        account_file << "Address: " << account.address << endl;
        account_file << "Phone Number: " << account.phone_number << endl;
        account_file << "PIN: " << account.pin << endl;
        account_file << "Balance: " << account.balance << endl;
    }
}

// Function to deposit cash into an existing account
void deposit_cash(RenderWindow& window, Font& font, const string& folder_path) {
    // Text objects for account number input
    Text instructions("Enter account number to deposit cash:", font, 40);
    instructions.setFillColor(Color::Black);
    instructions.setPosition(550, 350);

    Text input_field("", font, 40);
    input_field.setFillColor(Color::Black);
    input_field.setPosition(550, 450);

    Text feedback("", font, 30);
    feedback.setFillColor(Color::Red);
    feedback.setPosition(550, 700);

    string current_input = "";
    int account_number = 0;
    Account account;
    bool account_found = false;

    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
            }

            // Handle text input for account number
            if (event.type == Event::TextEntered) {
                if (event.text.unicode == '\b' && !current_input.empty()) { // Backspace
                    current_input.pop_back();
                }
                else if (event.text.unicode < 128 && event.text.unicode != '\b') {
                    current_input += static_cast<char>(event.text.unicode);
                }
            }

            // Handle Enter key to verify account number
            if (event.type == Event::KeyPressed && event.key.code == Keyboard::Enter) {
                if (!current_input.empty()) { // Allow any account number
                    account_number = stoi(current_input);

                    // Check if account exists
                    string file_path = folder_path + "/" + to_string(account_number) + ".txt";
                    if (filesystem::exists(file_path)) {
                        if (load_account_from_file(file_path, account)) {
                            account_found = true;
                            feedback.setString("Account found! Enter amount to deposit.");
                        }
                    }
                    else {
                        feedback.setString("Account number does not exist! Try again.");
                        continue;
                    }
                }
                else {
                    feedback.setString("Please enter a valid account number.");
                    continue;
                }
                current_input = ""; // Reset input for the next step
            }

            // Handle deposit amount input
            if (account_found && event.type == Event::KeyPressed && event.key.code == Keyboard::Enter) {
                Text deposit_instructions("Enter deposit amount:", font, 40);
                deposit_instructions.setFillColor(Color::Black);
                deposit_instructions.setPosition(550, 350);

                Text deposit_input_field("", font, 40);
                deposit_input_field.setFillColor(Color::Black);
                deposit_input_field.setPosition(550, 450);

                string deposit_input = "";

                // Wait for deposit amount input
                while (window.isOpen()) {
                    Event deposit_event;
                    while (window.pollEvent(deposit_event)) {
                        if (deposit_event.type == Event::Closed) {
                            window.close();
                        }

                        // Handle deposit input (amount)
                        if (deposit_event.type == Event::TextEntered) {
                            if (deposit_event.text.unicode == '\b' && !deposit_input.empty()) { // Backspace
                                deposit_input.pop_back();
                            }
                            else if (deposit_event.text.unicode < 128 && deposit_event.text.unicode != '\b') {
                                deposit_input += static_cast<char>(deposit_event.text.unicode);
                            }
                        }

                        // If Enter is pressed, process deposit
                        if (deposit_event.type == Event::KeyPressed && deposit_event.key.code == Keyboard::Enter) {
                            try {
                                int deposit_amount = stoi(deposit_input);
                                if (deposit_amount > 0) {
                                    account.balance += deposit_amount;  // Update the account balance

                                    // Open the file to append the deposit transaction and update balance
                                    string file_path = folder_path + "/" + to_string(account.account_number) + ".txt";
                                    ofstream account_file(file_path, ios::app); // Open file in append mode
                                    if (account_file) {
                                        // Append deposit details
                                        time_t now = time(0);
                                        tm local_time;
                                        localtime_s(&local_time, &now);

                                        char time_buffer[100];
                                        strftime(time_buffer, sizeof(time_buffer), "%Y-%m-%d %H:%M:%S", &local_time);

                                        account_file << "Deposited Amount: " << deposit_amount
                                            << " on Date and Time: " << time_buffer << endl;

                                        // After deposit, update balance (overwrite balance line)
                                        // Read the whole file, then overwrite balance and other details
                                        ifstream read_account_file(file_path);
                                        stringstream updated_file_content;
                                        string line;
                                        while (getline(read_account_file, line)) {
                                            // Overwrite balance line with updated balance
                                            if (line.find("Balance:") != string::npos) {
                                                line = "Balance: " + to_string(account.balance);
                                            }
                                            updated_file_content << line << endl;
                                        }
                                        read_account_file.close();

                                        // Rewrite the file with updated balance
                                        ofstream write_account_file(file_path);
                                        write_account_file << updated_file_content.str();

                                        account_file.close();
                                    }

                                    // Show "Amount Deposited" message for 3 seconds
                                    Text success_message("Amount deposited successfully!", font, 40);
                                    success_message.setFillColor(Color::Green);
                                    success_message.setPosition(550, 550);

                                    window.clear(Color::White);
                                    window.draw(success_message);
                                    window.display();

                                    // Wait for 3 seconds before returning
                                    Clock clock;
                                    while (clock.getElapsedTime().asSeconds() < 3.f) {
                                        Event e;
                                        while (window.pollEvent(e)) {
                                            if (e.type == Event::Closed)
                                                window.close();
                                        }
                                    }
                                    return; // Exit function after 3 seconds
                                }
                                else {
                                    feedback.setString("Deposit amount must be greater than 0!");
                                    continue;
                                }
                            }
                            catch (const invalid_argument&) {
                                feedback.setString("Invalid deposit amount!");
                                continue;
                            }
                        }
                    }

                    // Render the deposit screen
                    window.clear(Color::White);
                    window.draw(deposit_instructions);
                    deposit_input_field.setString(deposit_input); // Update deposit input field text
                    window.draw(deposit_input_field);
                    window.draw(feedback);
                    window.display();
                }
            }
        }

        // Update input field text for account number
        input_field.setString(current_input);

        // Render the screen
        window.clear(Color::White);
        window.draw(instructions);
        window.draw(input_field);
        window.draw(feedback);
        window.display();
    }
}




void view_account_details(RenderWindow& window, Font& font, const string& folder_path) {
    // Text objects for account number input
    Text instructions("Enter account number to view details:", font, 30);
    instructions.setFillColor(Color::Black);
    instructions.setPosition(100, 50);

    Text input_field("", font, 30);
    input_field.setFillColor(Color::Black);
    input_field.setPosition(100, 150);

    Text feedback("", font, 25);
    feedback.setFillColor(Color::Red);
    feedback.setPosition(100, 600);

    string current_input = "";
    int account_number = 0;
    Account account;
    bool account_found = false;

    // Step 1: Enter account number
    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
            }

            // Handle text input for account number
            if (event.type == Event::TextEntered) {
                if (event.text.unicode == '\b' && !current_input.empty()) { // Backspace
                    current_input.pop_back();
                }
                else if (event.text.unicode < 128 && event.text.unicode != '\b') {
                    current_input += static_cast<char>(event.text.unicode);
                }
            }

            // Handle Enter key to verify account number
            if (event.type == Event::KeyPressed && event.key.code == Keyboard::Enter) {
                if (!current_input.empty()) { // Allow any account number
                    account_number = stoi(current_input);

                    // Check if account exists
                    string file_path = folder_path + "/" + to_string(account_number) + ".txt";
                    if (filesystem::exists(file_path)) {
                        if (load_account_from_file(file_path, account)) {
                            account_found = true;
                            feedback.setString("Account found! Enter PIN to view details.");
                        }
                    }
                    else {
                        feedback.setString("Account number does not exist! Try again.");
                        continue;
                    }
                }
                else {
                    feedback.setString("Please enter a valid account number.");
                    continue;
                }
                current_input = ""; // Reset input for next step
            }
        }

        // Render the account number input screen
        window.clear(Color::White);
        window.draw(instructions);
        input_field.setString(current_input); // Update account number input field text
        window.draw(input_field);
        window.draw(feedback);
        window.display();

        // Once account is found, proceed to PIN input
        if (account_found) {
            break;
        }
    }

    // Step 2: Enter PIN for account verification
    string pin_input = "";
    bool pin_verified = false;

    Text pin_instructions("Enter PIN to view account details:", font, 30);
    pin_instructions.setFillColor(Color::Black);
    pin_instructions.setPosition(100, 200);

    Text pin_input_field("", font, 30);
    pin_input_field.setFillColor(Color::Black);
    pin_input_field.setPosition(100, 250);

    while (window.isOpen()) {
        Event pin_event;
        while (window.pollEvent(pin_event)) {
            if (pin_event.type == Event::Closed) {
                window.close();
            }

            // Handle PIN input (numbers only)
            if (pin_event.type == Event::TextEntered) {
                if (pin_event.text.unicode == '\b' && !pin_input.empty()) { // Backspace
                    pin_input.pop_back();
                }
                else if (pin_event.text.unicode < 128 && pin_event.text.unicode != '\b') {
                    pin_input += static_cast<char>(pin_event.text.unicode);
                }
            }

            // If Enter is pressed, verify PIN
            if (pin_event.type == Event::KeyPressed && pin_event.key.code == Keyboard::Enter) {
                if (pin_input == to_string(account.pin)) {
                    pin_verified = true;
                    feedback.setString("PIN verified! Showing account details.");
                    break; // PIN is verified, proceed to show account details
                }
                else {
                    feedback.setString("Invalid PIN! Try again.");
                    
                }
                pin_input = ""; // Reset input for next step
            }
        }

        // Render PIN input screen
        window.clear(Color::White);
        window.draw(pin_instructions);
        pin_input_field.setString(pin_input); // Update PIN input field text
        window.draw(pin_input_field);
        window.draw(feedback);
        window.display();

        if (pin_verified) {
            break; // Proceed to show account details
        }
    }

    // Step 3: Display Account Details
    Text account_details("Account Number: " + to_string(account.account_number) + "\n" +
        "Full Name: " + account.full_name + "\n" +
        "Address: " + account.address + "\n" +
        "Phone Number: " + account.phone_number + "\n" +
        "Balance: $" + to_string(account.balance), font, 30);
    account_details.setFillColor(Color::Black);
    account_details.setPosition(100, 300);

    // Wait for a key press to exit the details view
    while (window.isOpen()) {
        Event detail_event;
        while (window.pollEvent(detail_event)) {
            if (detail_event.type == Event::Closed) {
                window.close();
            }

            // Allow the user to exit after viewing details
            if (detail_event.type == Event::KeyPressed) {
                return; // Exit the details view after pressing any key
            }
        }

        // Render the account details
        window.clear(Color::White);
        window.draw(account_details);
        window.display();
    }
}



void withdraw_cash(RenderWindow& window, Font& font, const string& folder_path) {
    // Text objects for account number input
    Text instructions("Enter account number to withdraw cash:", font, 30);
    instructions.setFillColor(Color::Black);
    instructions.setPosition(100, 50);

    Text input_field("", font, 30);
    input_field.setFillColor(Color::Black);
    input_field.setPosition(100, 150);

    Text feedback("", font, 25);
    feedback.setFillColor(Color::Red);
    feedback.setPosition(100, 600);

    string current_input = "";
    int account_number = 0;
    Account account;
    bool account_found = false;

    // Step 1: Enter account number
    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
            }

            // Handle text input for account number
            if (event.type == Event::TextEntered) {
                if (event.text.unicode == '\b' && !current_input.empty()) { // Backspace
                    current_input.pop_back();
                }
                else if (event.text.unicode < 128 && event.text.unicode != '\b') {
                    current_input += static_cast<char>(event.text.unicode);
                }
            }

            // Handle Enter key to verify account number
            if (event.type == Event::KeyPressed && event.key.code == Keyboard::Enter) {
                if (!current_input.empty()) { // Allow any account number
                    account_number = stoi(current_input);

                    // Check if account exists
                    string file_path = folder_path + "/" + to_string(account_number) + ".txt";
                    if (filesystem::exists(file_path)) {
                        if (load_account_from_file(file_path, account)) {
                            account_found = true;
                            feedback.setString("Account found! Enter PIN to proceed.");
                        }
                    }
                    else {
                        feedback.setString("Account number does not exist! Try again.");
                        continue;
                    }
                }
                else {
                    feedback.setString("Please enter a valid account number.");
                    continue;
                }
                current_input = ""; // Reset input for next step
            }
        }

        // Render the account number input screen
        window.clear(Color::White);
        window.draw(instructions);
        input_field.setString(current_input); // Update account number input field text
        window.draw(input_field);
        window.draw(feedback);
        window.display();

        // Once account is found, proceed to PIN input
        if (account_found) {
            break;
        }
    }

    // Step 2: Enter PIN for account verification
    string pin_input = "";
    bool pin_verified = false;

    Text pin_instructions("Enter PIN to withdraw cash:", font, 30);
    pin_instructions.setFillColor(Color::Black);
    pin_instructions.setPosition(100, 200);

    Text pin_input_field("", font, 30);
    pin_input_field.setFillColor(Color::Black);
    pin_input_field.setPosition(100, 250);

    while (window.isOpen()) {
        Event pin_event;
        while (window.pollEvent(pin_event)) {
            if (pin_event.type == Event::Closed) {
                window.close();
            }

            // Handle PIN input (numbers only)
            if (pin_event.type == Event::TextEntered) {
                if (pin_event.text.unicode == '\b' && !pin_input.empty()) { // Backspace
                    pin_input.pop_back();
                }
                else if (pin_event.text.unicode < 128 && pin_event.text.unicode != '\b') {
                    pin_input += static_cast<char>(pin_event.text.unicode);
                }
            }

            // If Enter is pressed, verify PIN
            if (pin_event.type == Event::KeyPressed && pin_event.key.code == Keyboard::Enter) {
                if (pin_input == to_string(account.pin)) {
                    pin_verified = true;
                    feedback.setString("PIN verified! Enter amount to withdraw.");
                    break; // PIN is verified, proceed to withdrawal
                }
                else {
                    feedback.setString("Invalid PIN! Try again.");
                    continue;
                }
                pin_input = ""; // Reset input for next step
            }
        }

        // Render PIN input screen
        window.clear(Color::White);
        window.draw(pin_instructions);
        pin_input_field.setString(pin_input); // Update PIN input field text
        window.draw(pin_input_field);
        window.draw(feedback);
        window.display();

        if (pin_verified) {
            break; // Proceed to withdrawal
        }
    }

    // Step 3: Withdrawal Amount Input
    string withdraw_input = "";
    Text withdraw_instructions("Enter withdrawal amount:", font, 30);
    withdraw_instructions.setFillColor(Color::Black);
    withdraw_instructions.setPosition(100, 350);

    Text withdraw_input_field("", font, 30);
    withdraw_input_field.setFillColor(Color::Black);
    withdraw_input_field.setPosition(100, 400);

    Text withdraw_feedback("", font, 25);
    withdraw_feedback.setFillColor(Color::Red);
    withdraw_feedback.setPosition(100, 500);

    while (window.isOpen()) {
        Event withdraw_event;
        while (window.pollEvent(withdraw_event)) {
            if (withdraw_event.type == Event::Closed) {
                window.close();
            }

            // Handle withdrawal amount input
            if (withdraw_event.type == Event::TextEntered) {
                if (withdraw_event.text.unicode == '\b' && !withdraw_input.empty()) { // Backspace
                    withdraw_input.pop_back();
                }
                else if (withdraw_event.text.unicode < 128 && withdraw_event.text.unicode != '\b') {
                    withdraw_input += static_cast<char>(withdraw_event.text.unicode);
                }
            }

            // If Enter is pressed, process withdrawal
            if (withdraw_event.type == Event::KeyPressed && withdraw_event.key.code == Keyboard::Enter) {
                try {
                    int withdraw_amount = stoi(withdraw_input);
                    if (withdraw_amount > 0) {
                        if (withdraw_amount <= account.balance) {
                            // Update the balance by subtracting the withdrawal amount
                            account.balance -= withdraw_amount;

                            // Get the current date and time
                            auto now = chrono::system_clock::now();
                            auto time = chrono::system_clock::to_time_t(now);
                            struct tm time_info;
                            localtime_s(&time_info, &time);

                            // Format the withdrawal transaction details
                            stringstream withdrawal_details;
                            withdrawal_details << "Withdrawn Amount: " << withdraw_amount
                                << " on " << put_time(&time_info, "%Y-%m-%d %H:%M:%S") << "\n";

                            // Open the file in append mode to add new data at the end without overwriting
                            ofstream file(folder_path + "/" + to_string(account.account_number) + ".txt", ios::app);
                            if (file) {
                                // Only add a newline if the file already contains data.
                                file.seekp(0, ios::end); // Go to the end of the file
                                if (file.tellp() > 0) { // Check if file is not empty
                                    file << "\n"; // Append a newline before writing new transaction
                                }
                                file << withdrawal_details.str(); // Log withdrawn amount details
                            }

                            // Save updated account information with the new balance
                            save_account_to_file(folder_path + "/" + to_string(account.account_number) + ".txt", account);

                            // Show "Amount Withdrawn" message for 3 seconds
                            Text success_message("Amount withdrawn successfully!", font, 30);
                            success_message.setFillColor(Color::Green);
                            success_message.setPosition(100, 450);

                            window.clear(Color::White);
                            window.draw(success_message);
                            window.display();

                            // Wait for 3 seconds before returning
                            Clock clock;
                            while (clock.getElapsedTime().asSeconds() < 3.f) {
                                // Keep the window open for 3 seconds
                                Event e;
                                while (window.pollEvent(e)) {
                                    if (e.type == Event::Closed)
                                        window.close();
                                }
                            }
                            return; // Exit function after 3 seconds
                        }
                        else {
                            withdraw_feedback.setString("Insufficient balance!");
                            continue;
                        }
                    }
                    else {
                        withdraw_feedback.setString("Withdrawal amount must be greater than 0!");
                        continue;
                    }
                }
                catch (const invalid_argument&) {
                    withdraw_feedback.setString("Invalid withdrawal amount!");
                    continue;
                }
            }
        }

        // Render withdrawal screen
        window.clear(Color::White);
        window.draw(withdraw_instructions);
        withdraw_input_field.setString(withdraw_input); // Update withdrawal input field text
        window.draw(withdraw_input_field);
        window.draw(withdraw_feedback);
        window.display();
    }
}




void pay_utility_bill(RenderWindow& window, Font& font, const string& folder_path) {
    // Text objects for account number input
    Text instructions("Enter account number to pay a utility bill:", font, 30);
    instructions.setFillColor(Color::Black);
    instructions.setPosition(100, 50);

    Text input_field("", font, 30);
    input_field.setFillColor(Color::Black);
    input_field.setPosition(100, 150);

    Text feedback("", font, 25);
    feedback.setFillColor(Color::Red);
    feedback.setPosition(100, 600);

    string current_input = "";
    int account_number = 0;
    Account account;
    bool account_found = false;

    // Step 1: Enter account number
    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
            }

            // Handle text input for account number
            if (event.type == Event::TextEntered) {
                if (event.text.unicode == '\b' && !current_input.empty()) { // Backspace
                    current_input.pop_back();
                }
                else if (event.text.unicode < 128 && event.text.unicode != '\b') {
                    current_input += static_cast<char>(event.text.unicode);
                }
            }

            // Handle Enter key to verify account number
            if (event.type == Event::KeyPressed && event.key.code == Keyboard::Enter) {
                if (!current_input.empty()) {
                    account_number = stoi(current_input);

                    // Check if account exists
                    string file_path = folder_path + "/" + to_string(account_number) + ".txt";
                    if (filesystem::exists(file_path)) {
                        if (load_account_from_file(file_path, account)) {
                            account_found = true;
                            feedback.setString("Account found! Enter your PIN.");
                        }
                    }
                    else {
                        feedback.setString("Account number does not exist! Try again.");
                        continue;
                    }
                }
                else {
                    feedback.setString("Please enter a valid account number.");
                    continue;
                }
                current_input = ""; // Reset input for next step
            }
        }

        // Render the account number input screen
        window.clear(Color::White);
        window.draw(instructions);
        input_field.setString(current_input); // Update account number input field text
        window.draw(input_field);
        window.draw(feedback);
        window.display();

        // Once account is found, proceed to PIN input
        if (account_found) {
            break;
        }
    }

    // Step 2: PIN verification
    string pin_input = "";
    bool pin_verified = false;

    Text pin_instructions("Enter your PIN:", font, 30);
    pin_instructions.setFillColor(Color::Black);
    pin_instructions.setPosition(100, 200);

    Text pin_input_field("", font, 30);
    pin_input_field.setFillColor(Color::Black);
    pin_input_field.setPosition(100, 250);

    while (window.isOpen()) {
        Event pin_event;
        while (window.pollEvent(pin_event)) {
            if (pin_event.type == Event::Closed) {
                window.close();
            }

            // Handle PIN input
            if (pin_event.type == Event::TextEntered) {
                if (pin_event.text.unicode == '\b' && !pin_input.empty()) { // Backspace
                    pin_input.pop_back();
                }
                else if (pin_event.text.unicode < 128 && pin_event.text.unicode != '\b') {
                    pin_input += static_cast<char>(pin_event.text.unicode);
                }
            }

            // Verify PIN when Enter is pressed
            if (pin_event.type == Event::KeyPressed && pin_event.key.code == Keyboard::Enter) {
                if (pin_input == to_string(account.pin)) {
                    pin_verified = true;
                    feedback.setString("PIN verified! Proceeding to bill payment.");
                    break;
                }
                else {
                    feedback.setString("Invalid PIN! Try again.");
                    pin_input = ""; // Reset input
                    continue;
                }
            }
        }

        // Render PIN input screen
        window.clear(Color::White);
        window.draw(pin_instructions);
        pin_input_field.setString(pin_input); // Update PIN input field text
        window.draw(pin_input_field);
        window.draw(feedback);
        window.display();

        if (pin_verified) {
            break; // Proceed to bill payment
        }
    }

    // Step 3: Utility bill payment
    string utility_name = "";
    string amount_input = "";
    bool name_entered = false;
    bool transaction_completed = false;

    Text utility_instructions("Enter the name of the utility:", font, 30);
    utility_instructions.setFillColor(Color::Black);
    utility_instructions.setPosition(100, 350);

    Text utility_input_field("", font, 30);
    utility_input_field.setFillColor(Color::Black);
    utility_input_field.setPosition(100, 400);

    Text amount_instructions("Enter amount to pay:", font, 30);
    amount_instructions.setFillColor(Color::Black);
    amount_instructions.setPosition(100, 450);

    Text amount_input_field("", font, 30);
    amount_input_field.setFillColor(Color::Black);
    amount_input_field.setPosition(100, 500);

    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
            }

            // Handle utility name input
            if (!name_entered) {
                if (event.type == Event::TextEntered) {
                    if (event.text.unicode == '\b' && !utility_name.empty()) { // Backspace
                        utility_name.pop_back();
                    }
                    else if (event.text.unicode < 128 && event.text.unicode != '\b') {
                        utility_name += static_cast<char>(event.text.unicode);
                    }
                }
                if (event.type == Event::KeyPressed && event.key.code == Keyboard::Enter) {
                    if (!utility_name.empty()) {
                        name_entered = true; // Move to amount input
                        feedback.setString("Utility name accepted! Enter the amount.");
                    }
                    else {
                        feedback.setString("Utility name cannot be empty!");
                        continue;
                    }
                }
            }
            else {
                // Handle amount input
                if (event.type == Event::TextEntered) {
                    if (event.text.unicode == '\b' && !amount_input.empty()) { // Backspace
                        amount_input.pop_back();
                    }
                    else if (event.text.unicode < 128 && event.text.unicode != '\b') {
                        amount_input += static_cast<char>(event.text.unicode);
                    }
                }

                // Process payment on Enter
                if (event.type == Event::KeyPressed && event.key.code == Keyboard::Enter) {
                    try {
                        int amount = stoi(amount_input);
                        if (amount > 0 && amount <= account.balance) {
                            // Process payment and update account
                            account.balance -= amount;

                            // Prepare transaction details
                            stringstream transaction;
                            auto now = chrono::system_clock::now();
                            auto time = chrono::system_clock::to_time_t(now);

                            // Secure time formatting with ctime_s
                            char time_buffer[26];
                            ctime_s(time_buffer, sizeof(time_buffer), &time);

                            transaction << "Utility Payment: " << utility_name
                                << ", Amount: " << amount
                                << ", Date: " << time_buffer << "\n";

                            // Append transaction details to file (no overwriting)
                            ofstream file(folder_path + "/" + to_string(account.account_number) + ".txt", ios::app);
                            if (file) {
                                file << "\n" << transaction.str(); // Ensure new transaction is appended below previous ones
                            }

                            // Save updated account information with the new balance
                            save_account_to_file(folder_path + "/" + to_string(account.account_number) + ".txt", account);

                            feedback.setString("Payment successful!");
                            transaction_completed = true;
                        }
                        else {
                            feedback.setString("Invalid amount or insufficient balance!");
                            continue;
                        }
                    }
                    catch (...) {
                        feedback.setString("Invalid amount entered!");
                        continue;
                    }
                }
            }
        }

        // Render screen
        window.clear(Color::White);
        if (!name_entered) {
            window.draw(utility_instructions);
            utility_input_field.setString(utility_name);
            window.draw(utility_input_field);
        }
        else {
            window.draw(amount_instructions);
            amount_input_field.setString(amount_input);
            window.draw(amount_input_field);
        }
        window.draw(feedback);
        window.display();

        if (transaction_completed) {
            // Wait and exit
            Clock clock;
            while (clock.getElapsedTime().asSeconds() < 3.f) {}
            return;
        }
    }
}



void display_transaction_details(RenderWindow& window, Font& font, const Account& account, const string& folder_path) {
    // Open the account's file to retrieve transaction history
    string file_path = folder_path + "/" + to_string(account.account_number) + ".txt";
    ifstream account_file(file_path);
    vector<string> deposit_transactions;
    vector<string> withdrawn_transactions;
    vector<string> bill_payments;
    bool found_utility_payment = false;

    if (account_file) {
        string line;
        while (getline(account_file, line)) {
            // Once "Utility Payment" is found, start recording all subsequent lines
            if (found_utility_payment) {
                bill_payments.push_back(line);
            }

            // Check if "Deposit Amount" is found
            if (line.find("Deposit Amount:") != string::npos) {
                deposit_transactions.push_back(line);
            }

            // Check if "Withdrawn Amount" is found
            if (line.find("Withdrawn Amount:") != string::npos) {
                withdrawn_transactions.push_back(line);
            }

            // Check if "Utility Payment" is found
            if (!found_utility_payment && line.find("Utility Payment:") != string::npos) {
                found_utility_payment = true;
                bill_payments.push_back(line);  // Add the line that starts the bill payment history
            }
        }
        account_file.close();
    }
    else {
        cerr << "Error: Unable to open account file." << endl;
        return;
    }

    // Render transaction history screen
    int y_offset = 100;
    Text title("Transaction History for Account: " + to_string(account.account_number), font, 40);
    title.setFillColor(Color::Black);
    title.setPosition(500, y_offset);

    y_offset += 100;
    vector<Text> transactions;

    // Display Deposit Transactions
    if (!deposit_transactions.empty()) {
        Text deposit_title("Deposit Transactions:", font, 30);
        deposit_title.setFillColor(Color::Black);
        deposit_title.setPosition(500, y_offset);
        transactions.push_back(deposit_title);
        y_offset += 50;

        for (const auto& transaction : deposit_transactions) {
            Text transaction_text(transaction, font, 30);
            transaction_text.setFillColor(Color::Black);
            transaction_text.setPosition(500, y_offset);
            transactions.push_back(transaction_text);
            y_offset += 50;
        }
    }

    // Display Withdrawn Transactions
    if (!withdrawn_transactions.empty()) {
        Text withdrawn_title("Withdrawn Transactions:", font, 30);
        withdrawn_title.setFillColor(Color::Black);
        withdrawn_title.setPosition(500, y_offset);
        transactions.push_back(withdrawn_title);
        y_offset += 50;

        for (const auto& transaction : withdrawn_transactions) {
            Text transaction_text(transaction, font, 30);
            transaction_text.setFillColor(Color::Black);
            transaction_text.setPosition(500, y_offset);
            transactions.push_back(transaction_text);
            y_offset += 50;
        }
    }

    // Display Bill Payments (Utility Payments)
    if (!bill_payments.empty()) {
        Text bill_payment_title("Bill Payments (Utility Payments):", font, 30);
        bill_payment_title.setFillColor(Color::Black);
        bill_payment_title.setPosition(500, y_offset);
        transactions.push_back(bill_payment_title);
        y_offset += 50;

        for (const auto& payment : bill_payments) {
            Text transaction_text(payment, font, 30);
            transaction_text.setFillColor(Color::Black);
            transaction_text.setPosition(500, y_offset);
            transactions.push_back(transaction_text);
            y_offset += 50;
        }
    }

    // If there are no transactions, display "None"
    if (transactions.empty()) {
        Text no_transactions("No transactions available.", font, 30);
        no_transactions.setFillColor(Color::Black);
        no_transactions.setPosition(500, y_offset);
        transactions.push_back(no_transactions);
    }

    // Wait for Enter key press to finish viewing
    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
            }

            // Finish and exit on Enter key
            if (event.type == Event::KeyPressed && event.key.code == Keyboard::Enter) {
                return; // Exit the function after displaying transactions
            }
        }

        window.clear(Color::White);
        window.draw(title);
        for (const auto& transaction : transactions) {
            window.draw(transaction);
        }
        window.display();
    }
}




void show_transaction_history(RenderWindow& window, Font& font, const string& folder_path) {
    // Text objects for account number and PIN input
    Text instructions("Enter account number and PIN to view transaction history:", font, 40);
    instructions.setFillColor(Color::Black);
    instructions.setPosition(500, 300);

    Text account_field("", font, 40);
    account_field.setFillColor(Color::Black);
    account_field.setPosition(500, 400);

    Text pin_field("", font, 40);
    pin_field.setFillColor(Color::Black);
    pin_field.setPosition(500, 500);

    Text feedback("", font, 30);
    feedback.setFillColor(Color::Red);
    feedback.setPosition(500, 600);

    string account_input = "";
    string pin_input = "";
    bool entering_pin = false; // Track whether we're entering the PIN
    Account account;
    bool account_found = false;

    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
            }

            // Handle text input for account number or PIN
            if (event.type == Event::TextEntered) {
                if (event.text.unicode == '\b') { // Backspace
                    if (entering_pin && !pin_input.empty()) {
                        pin_input.pop_back();
                    }
                    else if (!entering_pin && !account_input.empty()) {
                        account_input.pop_back();
                    }
                }
                else if (event.text.unicode < 128 && event.text.unicode != '\b') {
                    if (entering_pin) {
                        pin_input += static_cast<char>(event.text.unicode);
                    }
                    else {
                        account_input += static_cast<char>(event.text.unicode);
                    }
                }
            }

            // Handle Enter key to switch between account number and PIN
            if (event.type == Event::KeyPressed && event.key.code == Keyboard::Enter) {
                if (!entering_pin) { // Finished entering account number
                    entering_pin = true;
                }
                else { // Verify account and PIN
                    if (!account_input.empty() && !pin_input.empty()) {
                        int account_number = stoi(account_input);
                        string file_path = folder_path + "/" + to_string(account_number) + ".txt";

                        if (filesystem::exists(file_path)) {
                            if (load_account_from_file(file_path, account) && account.pin == stoi(pin_input)) {
                                account_found = true;
                                feedback.setString("Account verified! Showing transaction history...");
                                display_transaction_details(window, font, account, folder_path);
                                return;
                            }
                            else {
                                feedback.setString("Invalid account number or PIN! Try again.");
                                continue;
                            }
                        }
                        else {
                            feedback.setString("Account does not exist! Try again.");
                            continue;
                        }
                    }
                    else {
                        feedback.setString("Please enter both account number and PIN.");
                    }

                    // Reset input fields
                    account_input = "";
                    pin_input = "";
                    entering_pin = false;

                    if (account_found) break; // Exit loop to display transaction history
                }
            }
        }

        // Render account and PIN input fields
        window.clear(Color::White);
        window.draw(instructions);
        account_field.setString("Account: " + account_input);
        pin_field.setString("PIN: " + pin_input);  // Show PIN as entered
        window.draw(account_field);
        window.draw(pin_field);
        window.draw(feedback);
        window.display();
    }
}