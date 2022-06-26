from typing import List

import pandas as pd

def writeEquilibrationTimes(equilibrationTimes: List[int]):
    data = {'Eq Times': equilibrationTimes}
    pd.DataFrame.from_dict(data).to_csv('GameOfLifeData.csv', index=False)
