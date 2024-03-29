import pandas as pd
import numpy as np

drug_responses = pd.read_csv("data/DrugResponses.csv")
inhibitors_list = drug_responses.inhibitor.unique()
del drug_responses['ic50']
pivot_drug_response = pd.pivot_table(drug_responses, index='lab_id', columns='inhibitor', aggfunc=np.max,  fill_value=0)
# Remove NA values
pivot_drug_response = pivot_drug_response[np.isfinite(pivot_drug_response)]

gene_counts = pd.read_csv("data/RNAseq.csv", encoding="ISO-8859-1", dtype={'lab_id': str})
gene_counts.set_index('lab_id', inplace=True)
gene_counts_transpose = gene_counts.transpose()
gene_count_ids = gene_counts_transpose.index

drugs_list = [22, 28, 43, 46, 82, 91, 109, 120]
for drug_num in drugs_list:
    sort_by_drug = pivot_drug_response.reindex(
        pivot_drug_response['auc'].sort_values(by=inhibitors_list[drug_num], ascending=False).index)
    sort_by_drug = sort_by_drug[sort_by_drug > 0]
    drug_response = sort_by_drug['auc'][inhibitors_list[drug_num]]
    drug_response = drug_response.dropna()
    drug_response_ids = drug_response.index
    combined_ids = list(set(gene_count_ids) & set(drug_response_ids))
    drug_response = drug_response.loc[combined_ids]
    Y = drug_response.sort_index()
    Y.columns = ['', 'auc']
    print(Y.columns)
    Y.to_csv('./data_outputs/Y_data/Y_' + inhibitors_list[drug_num] + '.csv', header=True)


