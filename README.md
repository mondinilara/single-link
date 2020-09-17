# SingleLink
Executa o SingleLink em uma base de dados com valores numéricos. Imprimi passo a passo executado no singleLink.

Exemplo de arquivo de entrada:

```sh
5.1,3.5,1.4,0.2
4.9,3.0,1.4,0.2
4.7,3.2,1.3,0.2
```

Arquivo de saída:
```sh
{0}, {1}, {2}
{0}, {1, 2}
{0, 1, 2}
```

Para executar o código é necessário informar os argumentos de acordo com a lista abaixo:
 - -inputFile - arquivo que será processado. É importante que ele não tenha espaços no nome, pois o código entenderá como um novo argumento e dará erro. Além disso, o arquivo deve conter apenas valores decimais
 - -sep - identificador de nova coluna
 - -dec - identificador de casa decimal
 - -outputFile - arquivo de saída


Exemplo de chamada do código no prompt:

```sh
$ python main.py -inputFile input.data -sep , -dec . -outputFile output.txt
```

É necessário que tenha as bibliotecas pandas e argparse instaladas no ambiente, caso não tenha, instalar utilizando os seguintes comandos no prompt:

```sh
$ pip install argparse
$ pip install pandas
```
