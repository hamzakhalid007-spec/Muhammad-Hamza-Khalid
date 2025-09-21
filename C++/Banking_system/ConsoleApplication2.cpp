#include <iostream>
using namespace std;

int main()
{
	int bank_balance = 985000;
	cout << "Press 1 to check your bank balance\n" << "Press 2 to deposit money\n" << "Press 3 to withdraw money\n";
	cout << "Press 4 to exit\n";
	int n;
	cout << "Number: ";
	cin >> n;
	while (n != 4)
	{
		if (n <= 0 || n > 4)
		{
			cout << "Error!" << endl;
			return 0;
		}
		if (n == 1)
		{
			cout << "Your current bank balance: " << bank_balance << endl;
		}
		if (n == 2)
		{
			int i;
			cout << "How much money you want to depsoit: ";
			cin >> i;
			if (i < 0)
			{
				cout << "Error! Please enter a positive number." << endl;
			}
			bank_balance += i;
			cout << "Thanks for using our services!"<< endl;
		}
		if (n == 3)
		{
			int j;
			cout << "How much money you want to withdraw: ";
			cin >> j;
			if (j < 0)
			{
				cout << "Error! Please enter a positive number\n";
			}
			else if (j > 50000)
			{
				cout << "You have reached your withrawal limit. Please try againg.\n";
			}
			bank_balance -= j;
			cout << "Thanks for using our services!" << endl;
		}
		cout << "Number: ";
		cin >> n;
	}
	if (n == 4)
	{
		cout << "Thanks for using our services, have a great day!\n";
	}

	return 0;
}