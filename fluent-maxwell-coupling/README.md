
# Ansys-Fluent-Coupling-Maxwell
Esse repositório é destinado à elaboração dos códigos necessários para realizar o acoplamento entre os softwares Ansys Fluent e Ansys Electronics

## 1. Dependências

##### Biblioteca `libudf` fornecida pela Ansys
##### Arquivos:
- `excitacoes.in`
- `excitacoes.out`

## 2. Como utilizar

#### 1. Configurar as excitações no Ansys Electronics cuidando a seguinte formatação:

| Nome  | Orientação  | ID  |
| :------------: | :------------: | :------------: |
| Nome da excitação como Current ou Voltage  | **\_In\_** ou **\_Out\_**  | Identificador |

Ex.: 
- Current_In_a
- Current_Out_a

#### 2. Inserir o nome das excitações nos arquivos `excitacoes.in` e `excitacoes.in`
- O arquivo `excitacoes.in` deve conter as excitações com a orientação `in`
- O arquivo `excitacoes.out` deve conter as excitações com a orientação `out`

#### 3. Observações
- É possível ter uma excitação de entrada sem uma excitação de saída.
- Para compilar para uso no Fluent deve-se
	- Descomentar a linha `#include "udf.h`
	- Substituir `void  lerCurrentAtual()` por `DEFINE_ON_DEMAND(lerCurrentAtual)`
	- Substituir `int main()`por
		- `DEFINE_ON_DEMAND(Atualiza_corrente)` ou
		- `DEFINE_EXECUTE_AT_END(Atualiza_corrente)`
