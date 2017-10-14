import os
import numpy as np
import pandas as pd

path = '/Users/luyangchen/Dropbox/Datathon_Material'
gtex_tissue = pd.read_csv(os.path.join(path, 'gtex_tissue.csv'))

organ = ['Breast', 'HeadAndNeck', 'Kidney', 'Brain', 'Lung', 'Prostate', 'Thyroid', 'Uterus']
tissue2organ = dict()
for i in range(gtex_tissue.shape[0]):
	if gtex_tissue['organ'][i] in organ:
		tissue2organ[gtex_tissue['name'][i]] = gtex_tissue['organ'][i]

gtex_sample_expression = pd.read_csv(os.path.join(path, 'gtex_sample_expression.csv'))
rpkm = gtex_sample_expression.pivot(index='sample_id', columns='gene_id', values='rpkm_expression')
rpkm = rpkm.assign(sample_id=rpkm.index)
sample_id_tissue_pair = gtex_sample_expression.groupby(['sample_id','tissue']).size().reset_index().rename(columns={0:'count'})
sample_id_tissue_pair = sample_id_tissue_pair.assign(organ=[tissue2organ[t] if t in tissue2organ else '<Missing>' for t in sample_id_tissue_pair['tissue']])
merged = pd.merge(rpkm, sample_id_tissue_pair, on='sample_id')
cleaned = merged[merged['organ'] != '<Missing>']
df = dict()
for o in organ:
	temp = cleaned[cleaned['organ'] == o]
	df[o] = temp[temp.columns.values[:5000]]