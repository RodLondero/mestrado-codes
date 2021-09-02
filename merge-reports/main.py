import os
import pathlib
import pandas as pd

class Mesclar:
    def __init__(self):
        self.path = os.path.dirname(pathlib.Path(__file__).absolute())
        self.destinationFolder = "teste"
        self.destinationPath = os.path.join(self.path, self.destinationFolder)
        self.file_list = []
        self.base_files_name = []

        self.__getFiles()
        
        self.selectedFiles = self.__choseFiles()

        self.dfs = self.__readFluentReportFiles()

    def __choseFiles(self):
        print("============================================")
        print(" Quais arquivos deseja mesclar: ")
        print("============================================")
        names = []

        optionSelected = -1
        while optionSelected != 0:
            optionNumber = 0
            
            for name in self.base_files_name:
                optionNumber += 1
                print(f" {'*' if name in names else '' :<2} {optionNumber} - {name}")
            print("0 - Fim")
            
            optionSelected = input("> ")
            
            if not optionSelected or int(optionSelected) == 0:
                break
            
            optionSelected = int(optionSelected)

            if optionSelected in range(1, len(self.base_files_name) + 1):
                names.append(self.base_files_name[optionSelected - 1])
        
        return names
                
    def __getFiles(self):
        for f in os.listdir(self.path):
            if f.endswith(".out"):
                self.file_list.append(os.path.join(self.path, f))
                self.base_files_name.append(f.split('.')[0])

        for f in os.scandir(self.path):
            if f.is_dir():
                for arquivo in os.listdir(f.path):
                    if arquivo.endswith(".out"):
                        self.file_list.append(os.path.join(self.path, f.name + "\\" + arquivo))

    def __readFluentReportFiles(self):        
        df_list = []
        
        for file in self.file_list:
            title = file.split(".")[0].split("\\")[-1]

            if title in self.selectedFiles:
                print(f"Reading {file} ...")
                with open(file, 'r') as f:
                    content = f.read().splitlines()

                    # Get title
                    # title = content[0].strip('"')

                    # Remove the second line of the file
                    content.pop(1)

                    # Get columns
                    columns = content[1].strip("()\n").split('"')
                    for i, val in enumerate(columns):
                        if val.strip() == '':
                            columns.pop(i)

                    # Format values to Float
                    for i in range(0, len(content[2:])):
                        line = content[2:][i].strip('\n').split(' ')
                        line = [float(item) for item in line]

                        content[i + 2] = line

                dataframe = pd.DataFrame(content[2:], columns=columns)
                # dataframe = dataframe.set_index('Time Step')
                dataframe.name = title
                df_list.append(dataframe)

        return df_list

    def mergeFiles(self):
        data = pd.DataFrame()
        
        print("")
        for file_name in self.selectedFiles: 
            print(f"Merging {file_name} ...")
            count = 0
            for df in self.dfs: 
                if df.name == file_name: 
                    if count == 0:
                        data = df.copy()
                    else:
                        data = pd.concat([data, df], ignore_index=True)
                    count += 1

            data.sort_values(by=['Time Step'], inplace=True)
            data.drop_duplicates(subset=['Time Step'], keep='first', inplace=True)
            data.name = file_name
            data.reset_index(drop=True, inplace=True)
            data.index = data.index + 1

            if not os.path.exists(self.destinationPath):
                os.makedirs(self.destinationPath)

            data.to_csv(os.path.join(self.destinationPath, file_name + '.csv'), sep=';', decimal=",", index=False)
                    



if __name__ == '__main__':
    mesclar = Mesclar()
    mesclar.mergeFiles()