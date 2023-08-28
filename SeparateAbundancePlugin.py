# Objective:
#   To separate "Users" vs "Non-Users"
import pandas as pd


import PyPluMA
import PyIO

class SeparateAbundancePlugin:
   def input(self, inputfile):
      self.parameters = PyIO.readParameters(inputfile)
      self.abundance_file = PyPluMA.prefix()+"/"+self.parameters["abundance_file"]
      self.metadata_file = PyPluMA.prefix()+"/"+self.parameters["metadata_file"]

   def run(Self):
       pass

   def output(self, outputfile):
      #abundance_file = "abundance-genus.csv"
      #metadata_file = "metadata.txt"

      out_users = outputfile+"_users.csv"#"abundance_users.csv"
      out_NonUsers = outputfile+"_non_users.csv"#"abundance_non_users.csv"

      metadata_df = pd.read_csv(self.metadata_file, sep="\t")
      #metadata_df["group"] = metadata_df["COCAINE USE"].apply(lambda x: 1 if x=="Non-User" else 2)
      metadata_df["group"] = metadata_df["COCAINE USE"]

      metadata_df["ClientID"] = metadata_df["CLIENT IDENTIFIER"]
      metadata_df = metadata_df[["group", "ClientID"]]

      df = pd.read_csv(self.abundance_file, index_col=0)


      df["ClientID"] = df.index
      # transform sample to match metadata
      df["ClientID"] = df["ClientID"].apply(lambda x: x.split("_")[0].replace(".", "/"))

      df = df.merge(metadata_df, how="left", on="ClientID")
      df.index = df["ClientID"]

      df_users = df[df["group"]=="User"]
      del df_users["group"]
      del df_users["ClientID"]
      df_users.index.names = [""]
      df_users.to_csv(out_users)

      df_non_users = df[df["group"]=="Non-User"]
      del df_non_users["group"]
      del df_non_users["ClientID"]
      df_non_users.index.names = [""]
      df_non_users.to_csv(out_NonUsers)
