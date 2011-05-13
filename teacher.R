# R script to analyze teacher salary data
dataAvg <- read.csv("../tmp/output_avg.txt", header=TRUE)
dataIndiv <- read.csv("../tmp/output_indiv.txt", header=TRUE)

# Plot salary vs. score
pdf("../tmp/salary_v_score_avg.pdf")
plot(dataAvg[,3], dataAvg[,5],
     #main="Avg. Score vs. Avg. Teacher Salary",
     xlab="Avg. Teacher Salary",
     ylab="Avg. Score")
dev.off()

pdf("../tmp/salary_v_score_indiv.pdf")
plot(dataIndiv[,3], dataIndiv[,5],
     #main="Avg. Score vs. Individual Teacher Salary",
     xlab="Indiv. Teacher Salary",
     ylab="Avg. Score")
dev.off()

# Perform regression analysis of salary vs. score
regressAvg <- lm(dataAvg[,5] ~ dataAvg[,3])

sink("../tmp/regress_salary_avg.txt")
summary(regressAvg)
sink()

regressIndiv <- lm(dataIndiv[,5] ~ dataIndiv[,3])

sink("../tmp/regress_salary_indiv.txt")
summary(regressIndiv)
sink()

# Plot experience vs. score
pdf("../tmp/experience_v_score_avg.pdf")
plot(dataAvg[,4:5],
     #main="Avg. Score vs. Avg. Teacher Experience",
     xlab="Avg. Teacher Experience",
     ylab="Avg. Score")
dev.off()

pdf("../tmp/experience_v_score_indiv.pdf")
plot(dataIndiv[,4:5],
     #main="Avg. Score vs. Individual Teacher Experience",
     xlab="Indiv. Teacher Experience",
     ylab="Avg. Score")
dev.off()

# Bin the salaries in groups of 5,000 dollars
# 25,000.01--30,000
dataAvg2530 <- dataAvg[dataAvg[,3] > 25000.01,]
dataAvg2530 <- dataAvg2530[dataAvg2530[,3] < 30000,]

dataIndiv2530 <- dataIndiv[dataIndiv[,3] > 25000.01,]
dataIndiv2530 <- dataIndiv2530[dataIndiv2530[,3] < 30000,]

# 30,000.01--35,000
dataAvg3035 <- dataAvg[dataAvg[,3] > 30000.01,]
dataAvg3035 <- dataAvg3035[dataAvg3035[,3] < 35000,]

dataIndiv3035 <- dataIndiv[dataIndiv[,3] > 30000.01,]
dataIndiv3035 <- dataIndiv3035[dataIndiv3035[,3] < 35000,]

# 35,000.01--40,000
dataAvg3540 <- dataAvg[dataAvg[,3] > 35000.01,]
dataAvg3540 <- dataAvg3540[dataAvg3540[,3] < 40000,]

dataIndiv3540 <- dataIndiv[dataIndiv[,3] > 35000.01,]
dataIndiv3540 <- dataIndiv3540[dataIndiv3540[,3] < 40000,]

# 40,000.01--45,000
dataAvg4045 <- dataAvg[dataAvg[,3] > 40000.01,]
dataAvg4045 <- dataAvg4045[dataAvg4045[,3] < 45000,]

dataIndiv4045 <- dataIndiv[dataIndiv[,3] > 40000.01,]
dataIndiv4045 <- dataIndiv4045[dataIndiv4045[,3] < 45000,]

# 45,000.01--50,000
dataAvg4550 <- dataAvg[dataAvg[,3] > 45000.01,]
dataAvg4550 <- dataAvg4550[dataAvg4550[,3] < 50000,]

dataIndiv4550 <- dataIndiv[dataIndiv[,3] > 45000.01,]
dataIndiv4550 <- dataIndiv4550[dataIndiv4550[,3] < 50000,]

# 50,000.01--55,000
dataAvg5055 <- dataAvg[dataAvg[,3] > 50000.01,]
dataAvg5055 <- dataAvg5055[dataAvg5055[,3] < 55000,]

dataIndiv5055 <- dataIndiv[dataIndiv[,3] > 50000.01,]
dataIndiv5055 <- dataIndiv5055[dataIndiv5055[,3] < 55000,]

# 55,000.01--60,000
dataAvg5560 <- dataAvg[dataAvg[,3] > 55000.01,]
dataAvg5560 <- dataAvg5560[dataAvg5560[,3] < 60000,]

dataIndiv5560 <- dataIndiv[dataIndiv[,3] > 55000.01,]
dataIndiv5560 <- dataIndiv5560[dataIndiv5560[,3] < 60000,]

# Plot histograms
pdf("../tmp/scores_35_40_avg.pdf")
hist(dataAvg3540[,5],
     main="Avg. Scores for Avg. Salary Range $35,000-$40,000",
     xlab="Avg. Scores")
dev.off()

pdf("../tmp/scores_35_40_indiv.pdf")
hist(dataIndiv3540[,5],
     main="Avg. Scores for Indiv. Salary Range $35,000-$40,000",
     xlab="Avg. Scores")
dev.off()

# Plot histograms
pdf("../tmp/scores_50_55_avg.pdf")
hist(dataAvg5055[,5],
     main="Avg. Scores for Avg. Salary Range $50,000-$55,000",
     xlab="Avg. Scores")
dev.off()

pdf("../tmp/scores_50_55_indiv.pdf")
hist(dataIndiv5055[,5],
     main="Avg. Scores for Indiv. Salary Range $50,000-$55,000",
     xlab="Avg. Scores")
dev.off()

# Plot histogram of district codes
pdf("../tmp/district_codes_indiv.pdf")
plot(as.factor(c(dataIndiv[,2])),
     #main="District codes contained in indiv. data",
     xlab="School Region",
     ylab="Frequency")
dev.off()

sink("../tmp/district_codes_levels.txt", append=FALSE, split=FALSE)
levels(dataIndiv[,2])
sink()
