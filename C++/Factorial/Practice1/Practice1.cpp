#include <iostream>
using namespace std;

int main()
{
	int n;
	cout << "Factorial of number:";
	cin >> n;
	cout << "\n";
	double factorial = 1;

	for (int i = n; i > 0; i--)
	{
		factorial = factorial * i;
	}
	cout << "Factorial: " << factorial << "\n";
	return 0;
}