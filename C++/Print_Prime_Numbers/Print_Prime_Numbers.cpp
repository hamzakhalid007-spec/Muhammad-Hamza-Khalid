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

	cout << "2" << endl;
	for (int i = 2; i <= n; i++)
	{
		if (checkPrime(i) == true)
		{
			cout << i << endl;
		}
	}
	
	return 0;
}