import pandas as pd
import numpy as np

# Load the data from the pickle files
developer_patches = pd.read_pickle('cleaned-developer-patches.pkl')
tool_patches = pd.read_pickle('cleaned-tool-patches.pkl')

# Add a new column 'expert_label' and set it to NaN for all rows
print(len(developer_patches))
print(len(tool_patches))
developer_patches['expert_label'] = np.nan
tool_patches['expert_label'] = np.nan

# Save the modified dataframes back to the pickle files
developer_patches.to_pickle('cleaned-developer-patches.pkl')
tool_patches.to_pickle('cleaned-tool-patches.pkl')