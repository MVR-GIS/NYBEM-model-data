"""Create the folder structure for a new model scenario.

Each model scenario has a standard folder structure. Models expect prescribed
folders to exist to read and write data from.

Args:
    path_to_alt:    string; Path to the alternative in which the prescribed
                    folder structure will be created.

Returns:
    A prescribed folder structure is written to the path provided.
"""
import os
import arcpy

def main():
    model_names = ["est_int", "est_sub", "est_sub_hard",
                   "est_sub_soft_clam", "est_sub_soft_sav",
                   "fresh_tid", "mar_deep", "mar_int", "mar_sub"]
    model_components = ["hsi", "predictors", "siv"]

    for model_name in model_names:
        os.makedirs(os.path.join(path_to_alt, model_name),
                    exist_ok=True)
        for model_component in model_components:
            os.makedirs(os.path.join(path_to_alt, model_name, model_component),
                        exist_ok=True)

if __name__ == "__main__":
    # Get input parameters
    path_to_alt = arcpy.GetParameterAsText(0)

    main()