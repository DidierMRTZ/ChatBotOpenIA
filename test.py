import pandas as pd
tb_claim_checklist_responses=pd.read_csv('data/tb_claim_checklist_responses.csv',sep=",")
tb_claim_checklist_tasks=pd.read_csv('data/tb_claim_checklist_tasks.csv',sep=",")
tb_claim=pd.read_csv('data/tb_claim.csv',sep=",")
tb_holdingcompanies=pd.read_csv('data/tb_holdingcompanies.csv',sep=",")
tb_policies=pd.read_csv('data/tb_policies.csv',sep=",")
tb_poriskadditionalfloodinfos=pd.read_csv('data/tb_poriskadditionalfloodinfos.csv',sep=",")
tb_users=pd.read_csv('data/tb_users.csv',sep=",")

print(tb_poriskadditionalfloodinfos.dtypes)