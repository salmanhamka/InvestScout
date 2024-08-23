CREATE TABLE finalproject (
	"Gender" VARCHAR(50),
	"Age" VARCHAR(10),
	"Allowance" INT,
	"Q1" INT,
	"Q2" INT,
	"Q3" INT,
	"Q4" INT,
	"Q5" INT,
	"Q6" INT,
	"Q7" INT,
	"Q8" INT,
	"Q9" INT,
	"Q10" INT,
	"Q11" INT,
	"Q12" INT,
	"Q13" INT,
	"Q14" INT,
	"Q15" INT,
	"Q16" INT,
	"Q17" INT,
	"Q18" INT,
	"Q19" INT,
	"Q20" INT,
	"Q21" INT,
	"Q22" INT,
	"Q23" INT,
	"Q24" INT,
	"Q25" INT,
	"Q26" INT,
	"Q27" INT,
	"Q28" INT,
	"Q29" INT,
	"Q30" INT
);
COMMENT ON COLUMN finalproject."Q1" IS 'I have a better understanding of how to invest my money';
COMMENT ON COLUMN finalproject."Q2" IS 'I have a better understanding of how to manage my credit use';
COMMENT ON COLUMN finalproject."Q3" IS 'I have the ability to maintain financial records for my income and expenditure';
COMMENT ON COLUMN finalproject."Q4" IS 'I can manage my money easily';
COMMENT ON COLUMN finalproject."Q5" IS 'I have better understanding of financial instruments (e.g. Bonds, stock, T-bill, time value of money, future contract, option and ets)';
COMMENT ON COLUMN finalproject."Q6" IS 'I have the ability to prepare my own budget weekly and monthly';
COMMENT ON COLUMN finalproject."Q7" IS 'I don’t save, because I think it is too hard';
COMMENT ON COLUMN finalproject."Q8" IS 'I enjoy spending money on things that arent practical';
COMMENT ON COLUMN finalproject."Q9" IS 'When I get money, I always spend it immediately within 1 or 2 days';
COMMENT ON COLUMN finalproject."Q10" IS 'I see it, I like it, I buy it describes me';
COMMENT ON COLUMN finalproject."Q11" IS 'Just do it describes the way I buy things';
COMMENT ON COLUMN finalproject."Q12" IS 'Buy now, think about it later describes me';
COMMENT ON COLUMN finalproject."Q13" IS 'I always failed to control myself from spending money';
COMMENT ON COLUMN finalproject."Q14" IS 'I am more concerned with what happens to me in short run than in long run';
COMMENT ON COLUMN finalproject."Q15" IS 'When I set having goals for myself, I rarely achieve them.';
COMMENT ON COLUMN finalproject."Q16" IS 'As far I know, some of my friends regularly do save with a saving account';
COMMENT ON COLUMN finalproject."Q17" IS 'I always discuss financial management issue (saving) with my friends';
COMMENT ON COLUMN finalproject."Q18" IS 'I always discuss financial management issue (investment) with my friends';
COMMENT ON COLUMN finalproject."Q19" IS 'I always spend my leisure time with my friends';
COMMENT ON COLUMN finalproject."Q20" IS 'I always involve in money spending activities with my friends';
COMMENT ON COLUMN finalproject."Q21" IS 'I always follow the information about investment growth';
COMMENT ON COLUMN finalproject."Q22" IS 'I put money aside on a regular basis for the future';
COMMENT ON COLUMN finalproject."Q23" IS 'In order to invest, I often compare prices before I make purchase';
COMMENT ON COLUMN finalproject."Q24" IS 'In order to invest, I often consider whether the stock prices are valuable when I sell it';
COMMENT ON COLUMN finalproject."Q25" IS 'In order to invest, I often understanding the fundamental analysis';
COMMENT ON COLUMN finalproject."Q26" IS 'I always have money available in the event of my failed investment';
COMMENT ON COLUMN finalproject."Q27" IS 'In rder to invest, I plan to manage my expenses';
COMMENT ON COLUMN finalproject."Q28" IS 'I save my money in order to do investment';
COMMENT ON COLUMN finalproject."Q29" IS 'I invest to achieve certain goals';
COMMENT ON COLUMN finalproject."Q30" IS 'I have some investment account in money market and also capital market';

	
COPY finalproject(
    "Gender",
    "Age",
    "Allowance",
    "Q1",
    "Q2",
    "Q3",
    "Q4",
    "Q5",
    "Q6",
    "Q7",
    "Q8",
    "Q9",
    "Q10",
    "Q11",
    "Q12",
    "Q13",
    "Q14",
    "Q15",
    "Q16",
    "Q17",
    "Q18",
    "Q19",
    "Q20",
    "Q21",
    "Q22",
    "Q23",
    "Q24",
    "Q25",
    "Q26",
    "Q27",
    "Q28",
    "Q29",
    "Q30"
)
FROM 'E:\hacktiv8\phase2\FINAL PROJECT\finance.csv'
DELIMITER ','
CSV HEADER


SELECT * FROM finalproject;

