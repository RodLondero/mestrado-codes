import os
import time
import pandas as pd
import plotly.express as px
import re


def main(path, file_name, salvar_html: bool = False, salvar_csv: bool = False, path_to_save: str = ""):
    
    filename, extension = os.path.splitext(file_name)
    
    pattern_data = re.compile(
        "^(\s+(([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?\s+)+)(([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?(:([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?)+)\s+[0-9]+$")
    pattern_title = re.compile(
        "^(\s+([a-zA-Z]+\s+)+)[a-zA-Z]-[a-zA-Z]+\s+[a-zA-Z]-[a-zA-Z]+\s+[a-zA-Z]-[a-zA-Z]+\s+[a-zA-Z]+\s+k\s+[a-zA-Z]+\s+[a-zA-Z]+([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?\s+p1\s+[a-zA-Z]+/[a-zA-Z]+$")

    columns = []
    lines = []

    start_time = time.time()
    
    for i, line in enumerate(open(path + file_name)):
        if not columns:
            for match in re.finditer(pattern_title, line):
                print("Getting titles...")
                columns = get_titles(match.group())

        for match in re.finditer(pattern_data, line):
            result = match.group().strip().split()
            
            if (int(result[0]) % 1000 == 0) and int(result[-1]) != 0:
                print("Getting iteration: " + result[0])
                
            lines.append(result)

    # Create a DataFrame and convert data to float
    df = pd.DataFrame(data=lines, columns=columns)
    df.set_index("iter")

    del (df['time'])
    # for t in columns:
    #     if t != 'time':
    #         df[t] = df[t].astype(float)

    # Plot
    plot(df[-100000:].copy(), filename=file_name, save_file=salvar_html, path_to_save=path_to_save)  # df[-500:] pega as 500 últimas iterações
    # plot(df[:500].copy())   # df[:500] pega as primeiras 500 iterações
    # plot(df[500:1000].copy())   # df[500:1000] pega entre 500 e 1000 iterações

    if salvar_csv:
        df.to_csv(f"{path_to_save}\\{filename}.csv", index=False)

    print("--- %s seconds ---" % (time.time() - start_time))
    print("Fim")


def get_titles(line: str):
    titles_list = line.replace("/", " ").strip().split(" ")
    titles_list[-1] = 'iteration'

    titles = []
    for title in titles_list:
        if title != "":
            titles.append(title)

    return titles.copy()


def plot(df_plot: pd.DataFrame, save_file: bool = True, filename: str = "", path_to_save: str = None):
    remove_to_plot = ['iter', 'time', 'iteration']
    columns_to_plot = []

    for x in df_plot.columns:
        if x not in remove_to_plot:
            columns_to_plot.append(x)

    fig = px.line(df_plot, y=columns_to_plot, log_y=True)
    fig.update_layout(
        yaxis=dict(
            showexponent='all',
            exponentformat='power',
            title='Resíduos',
        ),
        xaxis=dict(
            exponentformat='none',
            title="Iterações"
        ),
        separators=',.'
    )
    
    if save_file:
        fig.write_html(f"{path_to_save}\\{filename}.html")

    fig.show()