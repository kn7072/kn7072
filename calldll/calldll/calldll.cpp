#include "calldll.h" // ���������� ���������
using namespace std; // using ��������� ���������� � ��������, �������� std::cout ��� �������� std, �.�. ����� ������ cout


extern "C" __declspec(dllexport) void NumberList() 
{
    cout << "\n\nThis function Number List:" // \n\n � ������ ������� �� ����� ������, ���������� cout << �������� ����� �� �����
    << endl << endl; // endl - �������� endline (����� ������)
    cout << "";
    for(int i=0; i<10; i++) // ���������� ����� �� 1 �� 10 � ����� � ������� �� �����
    {
       cout << i << " ";
    }
    cout << endl << endl;
}


extern "C" __declspec(dllexport) int kvadrat(int number) 
{
    cout << "\n\nkvadrat chisla "
    << number << endl << endl;
    cout << number * number << endl << endl;
return 0;
}