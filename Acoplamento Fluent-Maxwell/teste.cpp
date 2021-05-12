#include <iostream>
#include <string>
#include <cmath>
#include <iostream>
#include <fstream>
#include "functions.c"
#include <algorithm>

using namespace std;

#define DEFLEN 10
#define BUFSIZ 512
#define PI 3.14159265358979323846

const string DELIMITER                = "    ";
const string EXTENSAO                 = ".current";
const string INPUT_FILE_NAME          = "input.txt";
const string EXCITACOES_IN_FILE_NAME  = "excitacoes.in";
const string EXCITACOES_OUT_FILE_NAME = "excitacoes.out";
const string LOG_FILE_NAME            = "logs/log_current.txt";
const double CURRENT_TIME             = 1e-5;

typedef struct
{
	string nome;
	int face_id;
	double valor;
} Excitacoes;

char* getPath()
{
    string path, linha, conteudo;
    // char conteudo[5][BUFSIZ];
    int i, j;

    cout << "\nBuscando o caminho do arquivo .current em " << INPUT_FILE_NAME << "\n";
    
    ifstream input_file(INPUT_FILE_NAME.c_str());

    if (!input_file)
    {
        cout << "Arquivo não encontrado.";
    }
    else
    {
        int i=0, j=0;
        while(getline(input_file, linha))
        {
            if (i % 2 != 0)
            {
                linha.erase(std::remove(linha.begin(), linha.end(), '\n'), linha.end());
                linha.erase(std::remove(linha.begin(), linha.end(), '\"'), linha.end());
                conteudo = conteudo + linha + "\n";        
                j++;
            }
            i++;
        }
        
        input_file.close();
    }

    // FILE* arquivo = fopen(INPUT_FILE_NAME, "r");
    
    // if(arquivo == NULL)
    //     return 0;   

    // i = 0; j = 0;
    // while(fgets(linha, sizeof(linha), arquivo) != NULL) 
    // {
    //     if (i % 2 != 0)
    //     {
    //         removeChar(linha, '\n');
    //         removeChar(linha, '\"');
    //         strcpy(conteudo[j], linha);            
    //         j++;
    //     }
	// 	i++;
    // }
    // fclose(arquivo);

    // strcpy(path, conteudo[3]);
    // strcat(path, "\\");
    // strcat(path, conteudo[4]);
    // strcat(path, EXTENSAO);

    // return path;
}

int main(){

    getPath();

    return 0;
}