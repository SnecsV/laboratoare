#include <iostream>
#include <string>
#include <clocale>
#include <fcntl.h>
#include <io.h>
#include <windows.h>
using namespace std;

const wstring alfabet=L"AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ";


wchar_t transformarelitere(wchar_t c)
{
    wstring lm=L"aăâbcdefghiîjklmnopqrsștțuvwxyz";
    wstring lM=L"AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ";
    for (int i=0;i<31;i++)
    {
        if (c==lm[i]) 
        {
            c=lM[i];
        }
    }
    return c;
}


wstring pregatirecuvant(wstring cuvant)
{
    wstring rezultat;
    for (int i=0;i<cuvant.length();i++)
    {
            
            if (cuvant[i]==L' ')
            continue;
            
        rezultat += transformarelitere(cuvant[i]);
    }
    return rezultat;
}


wstring criptare(wstring cuvant, wstring alfabet, int cheie, int nl)
{
    wstring rezultat;
    for (int i=0;i<cuvant.length();i++)
    {
        size_t pg=alfabet.find(cuvant[i]);
        if (pg==wstring::npos)
        {
            rezultat+=cuvant[i];
            continue;
        }
        int pozitie=static_cast<int>(pg);
        pozitie=(pozitie+cheie)%nl;
        rezultat+=alfabet[pozitie];
    }
    return rezultat;
}


wstring decriptare(wstring cuvant,wstring alfabet, int cheie,int nl)
{
    wstring rezultat;
    for (int i=0;i<cuvant.length();i++)
    {
       int pozitie=alfabet.find(cuvant[i]);
        pozitie=(pozitie-cheie)%nl;

        if (pozitie<0)
            pozitie+=nl;

        rezultat+=alfabet[pozitie];
    }
    return rezultat;
}


wstring permutare(wstring cuvant)
{
    wstring alfabetpermutat;
    for (wchar_t litera : cuvant)
    {
        if (alfabet.find(litera)!=wstring::npos &&
            alfabetpermutat.find(litera)==wstring::npos)
        {
            alfabetpermutat+=litera;
        }
    }

    for (wchar_t litera : alfabet)
    {
        if (alfabetpermutat.find(litera)==wstring::npos)
        {
            alfabetpermutat+=litera;
        }
    }

    return alfabetpermutat;
}


int main()
{
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);
    _setmode(_fileno(stdin), _O_U16TEXT);
    _setmode(_fileno(stdout), _O_U16TEXT);
    setlocale(LC_ALL, "");

    
    wcout<<L"Introduceti cuvantul: ";
    wstring cuvant;
    getline(wcin, cuvant);
    cuvant=pregatirecuvant(cuvant);
    wcout<<L"Introduceti cheia: ";
    int cheie;
    wcin>>cheie;
    if (cheie<1 || cheie>30)
    {
        wcout<<L"Cheia trebuie sa fie intre 1 si 30! Introduceti o cheie valida."<<endl;
        return 0;
    }
    cuvant=pregatirecuvant(cuvant);
    for (int i=0;i<cuvant.length();i++)
    {
        if (alfabet.find(cuvant[i])==wstring::npos)
        {
            wcout<<L"Cuvantul contine simboluri care nu fac parte din alfabetul limbii romane! Introdu un cuvant valid."<<endl;
            return 0;
        }
    }


    wcout<<L"Alegeti varianta de cifrare:1.Cezar 2.Cezar cu permutare:"; int a;
    wcin>>a;
    if (a==1)
    {
    wcout<<L"Tastati 1 pentru criptare sau 2 pentru decriptare: "; int b;
    wcin>>b;
    if (b==1)
    {
        
        wcout<<L"Cuvantul criptat este: "<<criptare(cuvant, alfabet, cheie, alfabet.length())<<endl;
    }
    else
    {
        wcout<<L"Cuvantul decriptat este: "<<decriptare(cuvant, alfabet, cheie, alfabet.length())<<endl;
    }
    }

    
    else
    {
        wcout<<L"Introduceti cuvantul-cheie pentru permutare: ";
        wstring cheiePermutare;
        wcin>>cheiePermutare;
        cheiePermutare=pregatirecuvant(cheiePermutare);
        wstring alfabetpermutat=permutare(cheiePermutare);

        wcout<<L"Tastati 1 pentru criptare sau 2 pentru decriptare: ";
        int c;
        wcin>>c;
        if (c==1)
        {
            wcout<<L"Cuvantul criptat este: "
                 <<criptare(cuvant, alfabetpermutat, cheie, alfabetpermutat.length())<<endl;
        }
        else
        {
            wcout<<L"Cuvantul decriptat este: "
                 <<decriptare(cuvant, alfabetpermutat, cheie, alfabetpermutat.length())<<endl;
        }
        
    }







}