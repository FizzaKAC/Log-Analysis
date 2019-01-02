#!/usr/bin/env python3
import psycopg2

DBNAME = "news"


def post_questions():
    print "Q1-What are the most popular three articles of all time?"
    get_answer(1)
    print"Q2-Who are the most popular article authors of all time?"
    get_answer(2)
    print"Q3-On which days did more than 1% of requests lead to errors?"
    get_answer(3)


def get_answer(num):
    if num == 1:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute("select articles.title as name,count(*) as num "
                  "from log,articles where SUBSTRING(path,10,100)="
                  "articles.slug"
                  " and path !='/' and status like '200%' group by name "
                  "order by num desc limit 3")
        articles = c.fetchall()
        db.close()
        for x in articles:
            print "*Article name='"+str(x[0])+"' and views="+str(x[1])+"\n"
    elif num == 2:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute("select author_articles.name,count(*) as num_articles,"
                  "SUM(num) as views "
                  "from author_articles join log_article_count"
                  " on author_articles.slug=log_article_count.sub"
                  " group by author_articles.name order by views desc;")
        authors = c.fetchall()
        db.close()
        for x in authors:
            print ("*Author "+x[0]+" wrote "+str(x[1])+" article(s) "
                   "and has "+str(x[2])+" views on it/them \n")
    elif num == 3:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute("select date(time) as date,"
                  " sum(case when status like '4%' then 1 else 0 end) "
                  "*100.0/count(*) "
                  "as percentage from log group by date having "
                  "sum(case when status like '4%' then 1 else 0 end) "
                  "*100.0/count(*)>1.0;")
        percentages = c.fetchall()
        db.close()
        for x in percentages:
            print "*Date="+str(x[0])+" and percentage={0:.1%}".format(x[1]/100)


if __name__ == '__main__':
    post_questions()
