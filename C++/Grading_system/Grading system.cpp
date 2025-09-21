#include <iostream>
using namespace std;

double grades(int marks)
{
	if (marks >= 90)
	{
		cout << "Excellent! You got an A grade\n";
	}
	else if (marks < 90 && marks >= 80)
	{
		cout << "Very good! You got a B grade\n";
	}
	else if (marks < 80 && marks >= 70)
	{
		cout << "Good, you got a C grade\n";
	}
	else if (marks < 70 && marks >= 60)
	{
		cout << "Need improvement, you got a D grade\n";
	}
	else
	{
		cout << "Fail! You got a F grade\n";
	}
	return 0;
}

int main()
{
	int marks;
	cout << "Enter your test marks: ";
	cin >> marks;
	cout << endl;
	if (marks < 0 || marks > 100)
	{
		cout << "Marks entered are invalid. Please type again.\n";
	}
	else
	{
		grades(marks);
	}

	return 0;
}