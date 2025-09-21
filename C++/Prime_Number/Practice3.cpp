#include <iostream>
#include <string>
using namespace std;

bool checkPrime(int n)
{
	bool prime;
	for (int i = 2; i < n; i++)
	{
		int mode = n % i;
		if (mode == 0)
		{
			return false;
			break;
		}
		else
		{
			return true;
		}
	}
}

int main()
{
	bool checkPrime(int);
	bool isPrime;
	int n;
	cout << "Number = ";
	cin >> n;
	cout << endl;
	isPrime = checkPrime(n);

	if (isPrime == true)
	{
		cout << "Number is prime";
	}
	else
	{
		cout << "Number is non prime";
	}
	return 0;
}