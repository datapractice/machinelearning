library(cluster)
gw = read.csv('data/gwas_catalog_v1.0-downloaded_2015-04-27.tsv', sep='\t')
head(gw)
head(gw,1)
table(gw$FIRST.AUTHOR)
head(gw,1)
head(gw,1)
head(gw,1)
table(gw$DISEASE.TRAIT)
sort(table(gw$DISEASE.TRAIT))
head(gw,1)
sort(table(gw$REGION))
sort(table(gw$REGION))
head(gw,1)
table(gw$PLATFORM..SNPS.PASSING.QC.)
sort(table(gw$PLATFORM..SNPS.PASSING.QC.))
head(gw,1)
sort(table(gw$MAPPED_GENE))
head(gw,1)
sort(table(gw$INITIAL.SAMPLE.DESCRIPTION))
sort(table(gw$CONTEXT)
)
colnames(gw)
c(8,9,11,21,25,27,33)
sort(table(gw$REPORTED.GENE.S.))
c(8,9,11,21,25,27,33)
colnames(gw)
gw_sub = gw[,c(8,9,11,21,25,27,33,14)]
dim(gw_sub)
dist = daisy(gw_sub[1:1000,], metric='gower')
dist = daisy(gw_sub[1:10000,], metric='gower')
dist = daisy(gw_sub, metric='gower')
plot(hclust(dist))
plot(hclust(dist), label=gw$DISEASE.TRAIT)
sorted(table(gw$DISEASE.TRAIT))
sort(table(gw$DISEASE.TRAIT))
tail(sort(table(gw$DISEASE.TRAIT)),50)
top_traits = tail(sort(table(gw$DISEASE.TRAIT)),50)
top_traits
names(top_traits)
top_traits = names(top_traits)
colnames(gw_sub)
gw_sub$DISEASE.TRAIT %in% top_traits
sum(gw_sub$DISEASE.TRAIT %in% top_traits)
gw_top_diseases = gw_sub[gw_sub$DISEASE.TRAIT %in% top_traits,]
dim(gw_top_diseases)
dist_top = daisy(gw_top_sub, metric='gower')
dist_top = daisy(gw_top_diseases, metric='gower')
plot(hclust(dist_top), label=gw_top_diseases$DISEASE.TRAIT)
plot(hclust(dist_top), label=gw_top_diseases$DISEASE.TRAIT, cex=.7)
plot(hclust(dist_top), cex=.7)
plot(hclust(dist_top, method='single'), cex=.7)
plot(hclust(sample(dist_top,1000)), cex=.7)
dist_top = daisy(sample(gw_top_diseases,1000), metric='gower')
sample(x=gw_top_diseases, 500)
dim(gw_top_diseases)
dist_top = daisy(gw_top_diseases[sample(nrow(gw_top_diseases),1000),], metric='gower')
plot(hclust(sample(dist_top,1000)), cex=.7)
dist_top
plot(hclust(dist_top, method='single'), cex=.7)
plot(hclust(dist_top, method='average'), cex=.7, label=gw_top_diseases$DISEASE.TRAIT)
plot(hclust(dist_top), cex=.7, label=gw_top_diseases$DISEASE.TRAIT)
plot(hclust(dist_top),  label=gw_top_diseases$DISEASE.TRAIT)
plot(hclust(dist_top))
?plot
?cluster::clusplot
?daisy
?pltree
plot(hclust(dist_top),  labels=gw_top_diseases$DISEASE.TRAIT)
plot(hclust(dist_top), horiz=TRUE)
plot(hclust(dist_top), horiz=TRUE)
gw_sample = gw_top_diseases[sample(nrow(gw_top_diseases),1000),]
dist_top = daisy(gw_top_diseases[sample(nrow(gw_top_diseases),1000),], metric='gower'
dist_top = daisy(gw_sample)
plot(hclust(dist_top), horiz=TRUE)
plot(hclust(dist_top),labels = gw_sample$DISEASE.TRAIT)
plot(hclust(dist_top),labels = gw_sample$DISEASE.TRAIT, cex=0.6)
table(gw_sample$DISEASE.TRAIT)
sort(table(gw_sample$DISEASE.TRAIT))
as.dendrogram(hclust(dist_top))
plot(as.dendrogram(hclust(dist_top)))
savehistory('gwas_clustering.r')
