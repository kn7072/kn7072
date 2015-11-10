#include "calldll.h" // подключаем заголовок
using namespace std; // using позволяет обращаться к обьектам, например std::cout без префикса std, т.е. пишем просто cout


extern "C" __declspec(dllexport) void NumberList() 
{
    cout << "\n\nThis function Number List:" // \n\n в начале переход на новую строку, инструкция cout << означает вывод на экран
    << endl << endl; // endl - означает endline (конец строки)
    cout << "";
    for(int i=0; i<10; i++) // перебираем числа от 1 до 10 в цикле и выводим на экран
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