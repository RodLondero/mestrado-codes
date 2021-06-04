//#include "udf.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "math.h"
#include "functions.c"

#define I_MAX 10000
#define PHASES 1
#define FREQ 60

#define DEFLEN 10
#define BUFSIZ 512
#define PI 3.14159265358979323846

static char DELIMITER[] = {"    "};
static char EXTENSAO[] = {".current"};
static char INPUT_FILE_NAME[] = {"input.txt"};
static char EXCITACOES_IN_FILE_NAME[] = {"excitacoes.in"};
static char EXCITACOES_OUT_FILE_NAME[] = {"excitacoes.out"};
static char LOG_FILE_NAME[] = {"logs/log_current.txt"};
static double CURRENT_TIME = 1e-5;

typedef struct
{
	char nome[BUFSIZ];
	int face_id;
	double valor;
} Excitacoes;


//****************************************************************************************
// Funções

char* getPath()
{
    static char path[BUFSIZ];
    char linha[BUFSIZ];
    char conteudo[5][BUFSIZ];
    int i, j;

    printf("\nBuscando o caminho do arquivo .current em %s", INPUT_FILE_NAME);

    FILE* arquivo = fopen(INPUT_FILE_NAME, "r");
    
    if(arquivo == NULL)
        return 0;   

    i = 0; j = 0;
    while(fgets(linha, sizeof(linha), arquivo) != NULL) 
    {
        if (i % 2 != 0)
        {
            removeChar(linha, '\n');
            removeChar(linha, '\"');
            strcpy(conteudo[j], linha);            
            j++;
        }
		i++;
    }
    fclose(arquivo);

    strcpy(path, conteudo[3]);
    strcat(path, "\\");
    strcat(path, conteudo[4]);
    strcat(path, EXTENSAO);

    return path;
}

void getExcitacoes(Excitacoes *ex, int in_out)
{
    char linha[BUFSIZ];
    FILE* arquivo;
    int i = 0;

    if (in_out == 0)
        arquivo = fopen(EXCITACOES_IN_FILE_NAME, "r");
    else if(in_out == 1)
        arquivo = fopen(EXCITACOES_OUT_FILE_NAME, "r");

    while(fgets(linha, BUFSIZ, arquivo) != NULL)
    {
        removeChar(linha, '\n');
        removeChar(linha, ' ');
        strcpy(ex[i].nome, linha);    
        i++;
    }
    fclose(arquivo);
}

void calculaCorrente(Excitacoes *excitacao)
{
    double t = CURRENT_TIME;
    double wt = 2 * PI * FREQ * t;
    double corrente[PHASES] = {0};
    char nome[BUFSIZ] = {""}, *token;
    
    printf("\n\nCalculando as novas correntes...");

	excitacao[0].valor = I_MAX * cos(wt);
    if (PHASES == 2)
        excitacao[1].valor = I_MAX * cos(wt - PI);
    if (PHASES == 3)
    {
        excitacao[1].valor = I_MAX * cos(wt - 2*PI/3);
        excitacao[2].valor = I_MAX * cos(wt + 2*PI/3);
    }
}

//DEFINE_ON_DEMAND(ler_current_atual)
void lerCurrentAtual()
{
#if !RP_NODE
    char* path_current = getPath();
    char linha[BUFSIZ] = {""}, conteudo_in_current[DEFLEN][BUFSIZ] = {""};
    char *token;

    printf("\nAbrindo o arquivo %s", path_current);
    FILE* arquivo_current = fopen(path_current, "r");

    if (arquivo_current != NULL)
    {
        printf("\nLendo o arquivo %s", path_current);
        printf("\n setup1.current ATUAL:\n");

        while( fgets(linha, BUFSIZ, arquivo_current) != NULL )
            printf("\t%s", linha);

        fclose(arquivo_current);
    }    
    else
        printf("\nNão foi possível abrir o arquivo %s", path_current);
#endif
}

//****************************************************************************************
// Main
//**************************************************************************************** 
//DEFINE_ON_DEMAND(Atualiza_corrente_Demand)
int main()
{
#if !RP_NODE

    char* path_current;
    char linha[BUFSIZ] = {""}, conteudo_in_current[DEFLEN][BUFSIZ] = {""};
    char *token, buffer[BUFSIZ] = {""}, tmp[BUFSIZ] = {""};
    int n_linhas_in_current = 0, i, j;

    path_current = getPath();

    if(path_current)
    {
        //printf("\nDeclaração das Excitações");
        Excitacoes ex_in[PHASES]  = {"", 0, 0};
        Excitacoes ex_out[PHASES] = {"", 0, 0};
        Excitacoes ex[DEFLEN] = {"", 0, 0};

        printf("\nBuscando excitações de entrada...");
        getExcitacoes(ex_in, 0);

        printf("\nBuscando excitações de saída...");
        getExcitacoes(ex_out, 1);

        printf("\nAbrindo o arquivo\t %s", path_current);

        FILE* arquivo_current = fopen(path_current, "r");

        if (arquivo_current != NULL)
        {
            // Obtém o conteúdo do arquivo Setup1.current
            printf("\nLendo o arquivo\t %s", path_current);
            
            fgets(linha, BUFSIZ, arquivo_current);
            n_linhas_in_current = atoi(linha);
            
            i = 0;
            while( fgets(linha, BUFSIZ, arquivo_current) != NULL )
            {
                removeChar(linha, '\n');                // Remove a quebra de linha do final
                strcpy(conteudo_in_current[i], linha);  // Salva o conteúdo da linha
                i++;   
            }
            fclose(arquivo_current);

            // Exibe o conteúdo do .current atual
            printf("\n\n\tsetup1.current ATUAL:");
            printf("\n\t%d", n_linhas_in_current);

            for(i = 0; i < n_linhas_in_current; i++)
            {			
                token = strtok(conteudo_in_current[i], DELIMITER); // Faz um split da linha
                
                strcpy(ex[i].nome, token);          // Salva o nome 
                strcpy(buffer, ex[i].nome);         // Salva o nome para edição

                token = strtok(NULL, DELIMITER);    // Obtém o ID da face
                ex[i].face_id = atoi(token);        // Converte para inteiro e salva
                
                token = strtok(NULL, DELIMITER);    // Obtém o valor 
                ex[i].valor = strtod(token, NULL);  // Converte para float e salva
                
                printf("\n\t%s", ex[i].nome);
                printf("\t%d", ex[i].face_id);
                printf("\t%f", ex[i].valor);
            }

            // Calculo das correntes
            calculaCorrente(ex_in);

            char split[3][BUFSIZ] = {""};
        
            for(i=0; i<PHASES; i++)
            {
                strcpy(buffer, ex_in[i].nome);
                strcpy(buffer, toLower(buffer));
                
                token = strtok(buffer, "_");
                j = 0;
                while (token != NULL)
                {
                    strcpy(split[j], token);
                    token = strtok(NULL, "_");
                    j++;
                }
                
                sprintf(buffer, "%s_out_%s", split[0], split[2]);
                for(j=0; j<PHASES; j++)
                {
                    strcpy(tmp, ex_out[j].nome);
                    if (strstr(toLower(tmp), buffer))
                        ex_out[j].valor = ex_in[j].valor;
                }
            }

            for (i=0; i<n_linhas_in_current; i++)
            {
                for(j=0; j < PHASES; j++)
                {
                    if (!strcmp(ex[i].nome, ex_in[j].nome))
                        ex[i].valor = ex_in[j].valor;
                    else if (!strcmp(ex[i].nome, ex_out[j].nome))
                        ex[i].valor = ex_out[j].valor;
                }
            }

            // Escreve no arquivo .current
            FILE *log_file = fopen(LOG_FILE_NAME, "a");
            static char sLog[BUFSIZ];

            arquivo_current = fopen(path_current, "w+");
            fprintf(arquivo_current, "%d\n", n_linhas_in_current);
            
            printf("\n\n\tsetup1.current NOVO:");
            printf("\n\t%d", n_linhas_in_current);
            
            sprintf(sLog, "%f", CURRENT_TIME);
            
            for (i=0; i < n_linhas_in_current; i++)
            {	
                fprintf(arquivo_current, "%s%s%d%s%f\n", ex[i].nome, DELIMITER, ex[i].face_id, DELIMITER, ex[i].valor);
                
                sprintf(sLog, "%s\t%f", sLog, ex[i].valor);

                printf("\n\t%s\t%d\t%f", ex[i].nome, ex[i].face_id, ex[i].valor);
            }
            sprintf(sLog, "%s\n", sLog);
            fprintf(log_file, sLog);
            
            fclose(arquivo_current);
            
            printf("\n\nTime: %f\n", CURRENT_TIME);
        }
        else
            printf("\nNão foi possível abrir o arquivo %s", path_current);   
    }
    else
        printf("\nNão foi possível ler o arquivo %s.", INPUT_FILE_NAME);
#endif
}