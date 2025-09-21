#include <iostream>
using namespace std;

double BMI(double weight, double height)
{
	double BMI = weight * 703 / (height * height);
	cout << "Your BMI is " << BMI << endl;

	if (BMI < 20)
	{
		cout << "You are underweight\n";
		cout << "Have a milkshake\n";
	}
	else if (BMI >= 20 && BMI <= 25)
	{
		cout << "Your weight is normal\n";
		cout << "Have a glass of milk\n";
	}
	else if (BMI > 25 && BMI <= 30)
	{
		cout << "You are overweight\n";
		cout << "Have a glass of iced tea\n";
	}
	else
	{
		cout << "You are obese\n";
		cout << "See a doctor\n";
	}
	return 0;
}

int main()
{
	double weight, height;
	cout << "Enter your weight in pounds: ";
	cin >> weight;
	cout << "Enter your height in inches: ";
	cin >> height;
	cout << endl;

	if (height <= 0 || weight <= 0)
	{
		cout << "Invalid data, weight and height must be positive\n";
	}
	else
	{
		BMI(weight, height);
	}

	
	return 0;
}