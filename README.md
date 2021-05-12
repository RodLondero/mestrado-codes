# Mestrado-codes

Esse espaço está sendo utilizado para controlar os cálculos e algortimos utilizados ao longo do mestrado

---

- [Mestrado-codes](#mestrado-codes)
  - [Plot dos resultados](#plot-dos-resultados)
  - [Cálculos](#cálculos)
  - [Propriedades do Ar](#propriedades-do-ar)
  - [Acoplamento Fluent-Maxwell](#acoplamento-fluent-maxwell)

---

## [Plot dos resultados](https://github.com/RodLondero/Mestrado/tree/main/Codigos/Plot%20dos%20Resultados)

Código em Python para plotar os resultados obtidos do [Ansys Fluent](https://www.ansys.com/products/fluids/ansys-fluent).

## [Cálculos](https://github.com/RodLondero/Mestrado/tree/main/Codigos/Calculos)

Calculos gerais utilizados para as simulações

## [Propriedades do Ar](https://github.com/RodLondero/Mestrado/tree/main/Codigos/Propriedades%20do%20Ar)

Essa pasta contém os códigos utilizados para realizar o plot das seguintes propriedades do ar:

- Densidade
- Calor Específico
- Viscosidade
- Condutividade Térmica
- Condutividade Elétrica

*Para visualizar, acesse o arquivo [Propriedades do Ar/Propriedades_do_Ar.ipynb](https://github.com/RodLondero/Mestrado/blob/main/Codigos/Propriedades%20do%20Ar/Propriedades_do_Ar.ipynb)*

## [Acoplamento Fluent-Maxwell](https://github.com/RodLondero/Mestrado/tree/main/Codigos/Acoplamento%20Fluent-Maxwell)

Projeto em [C](https://pt.wikipedia.org/wiki/C_%28linguagem_de_programa%C3%A7%C3%A3o%29) para realizar o acoplamento entre Fluent-Maxwell utilizando corrente alternada (CA). Em resumo, é uma UDF (do inglês, *User-Defined Function*) que calcula e atualiza o arquivo de excitações que o Maxwell lê cada vez que é chamado pelo Fluent.