__author__ = "Mohsen Moarefdoost"
__copyright__ = ""
__license__ = ""
__version__ = ""
__doc__ = ""

import glob
import optimization
import logging

logging.basicConfig(format=' %(asctime)s  %(name)-12s %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__ + " : ")

dl = optimization.DataLoader(input_files=glob.glob("./data/*.csv"))
data = optimization.Data(dl)
optimizer = optimization.Optimizer(data)

status = optimizer.optimize(WriteLpFlag=True)

if status == 1:
    output_df_dict = data.get_output_reports(optimizer)
    for key, df in output_df_dict.items():
        out_name = 'optimizer_' + key
        df.to_csv(''.join(["./data/", out_name, '.csv']), index=False)
        logger.info("wrote {0} records of {1}".format(len(df), out_name))
