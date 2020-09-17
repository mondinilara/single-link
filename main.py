import pandas as pd
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-inputFile',
        default='input.data',
        type=str,
        help='name of file that will be worked')
    parser.add_argument(
        '-sep',
        default=',',
        help='column identifier')
    parser.add_argument(
        '-dec',
        default='.',
        help='decimal identifier')
    parser.add_argument(
        '-outputFile',
        default='output.txt',
        type=str,
        help='name of result file')

    return parser.parse_args()


def abs(x):
    if x < 0:
        return x * (-1)
    return x


def minkowski_distance(x, y, r):
    exp = 0.0
    tam = len(y) if (len(x) > len(y)) else len(x)
    for i in range(tam):
        exp += abs((x[i] - y[i])) ** r
    return exp ** (1 / r)


def euclidean_distance(x, y):
    return minkowski_distance(x, y, 2)


def distance_matrix(df):
    columns_array = create_column(len(df.values))

    # calcula distâncias
    calculated_distance = []
    for i in range(len(df.values)):
        j = 0
        array = []
        while j < len(df.values):
            # zera os valores de distância já calculada e a matriz principal
            while j <= i:
                array.append(0.0)
                j += 1

            if j < len(df.values):
                array.append(euclidean_distance(df.values[i], df.values[j]))
            j += 1
        calculated_distance.append(array)

    return pd.DataFrame(calculated_distance, columns=columns_array)


# cria colunas do dataframe
def create_column(tam):
    cont = 0
    columns_array = []
    while tam > 0:
        columns_array.append('{' + str(cont) + '}')
        cont += 1
        tam -= 1
    return columns_array


def remove_X_values(array):
    new = []
    for i in array:
        if i != 'X':
            new.append(i)

    return new


def update_matrix(df, f):
    # inicializa com valor alto de distância
    min = 99999999999999999999.99
    key_x = key_y = ''

    # encontra menor valor e suas posições do DF
    for i in range(len(df.values)):
        if df.columns[i] == 'X':
            continue
        j = i + 1
        # acima da diagonal principal
        while j < len(df.values[i]):
            value = df.values[i][j]

            if value < min and df.columns[j] != 'X':
                key_x = df.columns[i]
                key_y = df.columns[j]
                min = df.values[i][j]
            j += 1

    column1 = df[key_x]
    column2 = df[key_y]

    # encontra menor valor das colunas selecionadas
    merge_column = []
    for i in range(len(df.values)):
        if column1[i] < column2[i]:
            merge_column.append(column1[i])
        else:
            merge_column.append(column2[i])

    # substitui a coluna 1 pela união de 1 e 2
    min_distance_column = pd.DataFrame(merge_column, columns=[df.columns.array])
    df[key_x] = min_distance_column

    new_name = '{' + str(key_x).replace('{', '').replace('}', '') + ', ' + str(key_y).replace('{', '').replace('}',
                                                                                                               '') + '}'
    # renomeia colunas. X para aquelas que já foram eliminadas
    df = df.rename(columns={str(key_x): str(new_name), str(key_y): 'X'})
    f.write(str(remove_X_values(df.columns.array)).replace('\'', '').replace('[', '').replace(']', '') + '\n')

    # faz chamada recursiva até que um unico grupo seja obtido
    if len(remove_X_values(df.columns.array)) > 1:
        update_matrix(df, f)


def single_link(df, file):
    with open(file, 'w+') as f:
        matrix = distance_matrix(df)
        f.write(str(remove_X_values(matrix.columns.array)).replace('\'', '').replace('[', '').replace(']', '') + '\n')
        update_matrix(matrix, f)
    f.close()


args = get_args()
df = pd.read_csv(args.inputFile, sep=args.sep, decimal=args.dec,
                 header=None)
single_link(df, args.outputFile)
