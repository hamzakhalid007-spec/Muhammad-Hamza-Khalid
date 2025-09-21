#include <iostream>
using namespace std;

double binaryToDeci(int biNum)
{
	double ans = 0, power = 1;
	while (biNum > 0)
	{
		int rem = biNum % 10;
		ans += rem * power;
		power *= 2;
		biNum = biNum / 10;
	}
		
	return ans;
}

void main()
{
	double biNum;
	cout << "Enter your number: ";
	cin >> biNum;
	cout << endl;

	double deci = binaryToDeci(biNum);
	cout << "Your number is " << deci << endl;


}