from ssproc.utility.handle_files import load_ecomapper_log_files
import os
import logging
import pickle
import config as cc
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

if not os.path.exists(cc.nav_df_path):
    lf = load_ecomapper_log_files(cc.nav_path)
    pickle.dump(lf, open(cc.nav_df_path, 'wb'))
else:
    lf = pickle.load(open(cc.nav_df_path, 'rb'))
plt.figure()

