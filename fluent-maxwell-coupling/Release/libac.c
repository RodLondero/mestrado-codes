#include "udf.h"
#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "math.h"
#include "ctype.h"

#define DEFLEN 10
#define BUFSIZ 512
#define PI 3.14159265358979323846
#define FREQ 60

static char DELIMITER[]                 = {"    "};
static char EXTENSAO[]                  = {".current"};
static char INPUT_FILE_NAME[]           = {"input.txt"};
static char EXCITACOES_IN_FILE_NAME[]   = {"_excitacoes.in"};
static char EXCITACOES_OUT_FILE_NAME[]  = {"_excitacoes.out"};
static char LOG_FILE_NAME[]             = {"logs/_log_current.txt"};

// static double CURRENT_TIME = 8.333e-5;
double i_max[3] = {0, 0, 0};
double angulo[3] = {0, 0, 0};
int PHASES = 3;

typedef struct
{
	char nome[BUFSIZ];
	int face_id;
	double valor;
} Excitacoes;

void removeChar(char *str, char garbage) 
{
    char *src, *dst;
    for (src = dst = str; *src != '\0'; src++) 
    {
        *dst = *src;
        if (*dst != garbage) dst++;
    }
    *dst = '\0';
}

char* getPath()
{
    static char path[BUFSIZ];
    char linha[BUFSIZ];
    char conteudo[10][BUFSIZ];
    int i, j;

    Message("\nBuscando o caminho do arquivo .current em %s", INPUT_FILE_NAME);

    FILE* arquivo = fopen(INPUT_FILE_NAME, "r");
    
    if(arquivo == NULL)
        return 0;   

    i = 0; j = 0;
    while(fgets(linha, sizeof(linha), arquivo) != NULL) {
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

    // Imprime o conteúdo do input.txt
    // for(i=0; i < sizeof(conteudo)/sizeof(conteudo[0]); i++)
    //     printf("%d - %s\n", i, conteudo[i]);

    // Concatenação do caminho do arquivo .current
    strcpy(path, conteudo[3]);  // Caminho do arquivo da pasta de acoplamento
    strcat(path, conteudo[4]);  // Nome do Setup
    strcat(path, EXTENSAO);     // Extensão .current

    // Número de fases
    removeChar(conteudo[5], ' ');
    if (strlen(conteudo[5]) > 0)
        PHASES = atoi(conteudo[5]);
    else
        PHASES = 1;

    for(i=0; i<PHASES; i++)
    {
        char delim[] = " ";
        char * token = strtok(conteudo[6+i], delim);
        i_max[i] = atof(token);
        token = strtok(NULL, delim);
        angulo[i] = atof(token);
    }

    for(i=0; i<PHASES; i++)
        printf("Imax[%d] = %f |_ %f\n", i, i_max[i], angulo[i]);
    printf("\nPhases: %d\n", PHASES);

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
    char nome[BUFSIZ] = {""}, *token;

    printf("\n\nCalculando as novas correntes...");

	excitacao[0].valor = i_max[0] * cos(wt + angulo[0] * PI/180);

    if (PHASES == 2)
         excitacao[1].valor = i_max[1] * cos(wt + angulo[1] * PI/180);
    if (PHASES == 3)
    {
        excitacao[1].valor = i_max[1] * cos(wt + angulo[1] * PI/180);
		excitacao[2].valor = i_max[2] * cos(wt + angulo[2] * PI/180);

        // Correção para a soma das correntes ser igual a zero
        char n1[40], n2[40], n3[40];

        double soma = excitacao[0].valor + excitacao[1].valor + excitacao[2].valor;

        sprintf(n1, "%.4f", excitacao[0].valor - soma/3);
        sprintf(n2, "%.4f", excitacao[1].valor - soma/3);
        sprintf(n3, "%.4f", excitacao[2].valor - soma/3);

        excitacao[0].valor = atof(n1);
        excitacao[1].valor = atof(n2);
        excitacao[2].valor = atof(n3);

        printf("\nSoma: %f", excitacao[0].valor + excitacao[1].valor + excitacao[2].valor);
    }
}

char* toLower(char* s) {
    for(char *p=s; *p; p++) *p=tolower(*p);
    return s;
}

void setCorrente()
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
        Excitacoes *ex_in  = (Excitacoes *)malloc(PHASES * sizeof(Excitacoes));
        Excitacoes *ex_out = (Excitacoes *)malloc(PHASES * sizeof(Excitacoes));
        Excitacoes *ex     = (Excitacoes *)malloc(PHASES * sizeof(Excitacoes));

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
                strcpy(buffer, ex_in[i].nome);      // Copia o nome para um buffer
                strcpy(buffer, toLower(buffer));    // Converte para minúsculas
                
                token = strtok(buffer, "_");        // Split "_"
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

            // Escreve o tempo no arquivo de log
            sprintf(sLog, "%f", CURRENT_TIME);
            
            for (i=0; i < n_linhas_in_current; i++)
            {	
                // Salva as correntes no arquivo .current
                fprintf(arquivo_current, "%s%s%d%s%f\n", ex[i].nome, DELIMITER, ex[i].face_id, DELIMITER, ex[i].valor);
                
                // Salva as correntes no log
                sprintf(sLog, "%s\t%.4f", sLog, ex[i].valor);
                
                // Imprime na tela as correntes
                printf("\n\t%s\t%d\t%f", ex[i].nome, ex[i].face_id, ex[i].valor);
            }
            
            // Adidiona quebra de linha no final da linha do log
            sprintf(sLog, "%s\n", sLog);
            // Grava o arquivo de log
            fprintf(log_file, sLog);
            
            // Fecha os arquivos
            fclose(log_file);
            fclose(arquivo_current);
            
            printf("\n\nLog salvo em: ./%s", LOG_FILE_NAME);
            printf("\n\nTime: %f\n", CURRENT_TIME);
        }
        else
            printf("\nNão foi possível abrir o arquivo %s", path_current);   
    }
    else
        printf("\nNão foi possível ler o arquivo %s.", INPUT_FILE_NAME);
#endif
}

DEFINE_ON_DEMAND(ler_current_atual)
{
#if !RP_NODE
    char* path_current = getPath();
    char linha[BUFSIZ] = {""}, conteudo_in_current[DEFLEN][BUFSIZ] = {""};
    char *token;

    Message("\nAbrindo o arquivo %s", path_current);
    FILE* arquivo_current = fopen(path_current, "r");

    if (arquivo_current != NULL)
    {
        Message("\nLendo o arquivo %s", path_current);
        Message("\n setup1.current ATUAL:\n");

        while( fgets(linha, BUFSIZ, arquivo_current) != NULL )
            Message("\t%s", linha);

        fclose(arquivo_current);
    }    
    else
        Message("\nNão foi possível abrir o arquivo %s", path_current);
#endif
}

DEFINE_ON_DEMAND(Atualiza_corrente_Demand)
{
    setCorrente();
}

DEFINE_EXECUTE_AT_END(Atualiza_corrente_Fim)
{
    setCorrente();
}

DEFINE_INIT(start_log_current, d)
{
    FILE *log_file = fopen(LOG_FILE_NAME, "w");
    fprintf(log_file, "Início do log de correntes\n\n");
    fclose(log_file);
}