# README
Hi! My name is fizza and this is the read me for my **log analysis** project. The log analysis code is a reporting tool that will use information from the news database to discover what kind of articles the site's readers like. 

## Install
Firstly, to start on this project, you'll need database software ([PostgresSQL](http://www.postgresqltutorial.com/install-postgresql/)) and the data to analyze.

Next, [download the data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) here. You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the directory which is shared with your virtual machine, if using one.

Create a new database named **News**. Connect to the database server using the `psql` command and  firstly run 
```
-f newsdata.sql
```
Then, create two views by running the following code
```
create view log_article_count as
select path,SUBSTRING(path,10,100) as sub,count(*) as num
from log
where path !='/' and status like '200%'
group by path
order by num desc;
```
And
```
create view author_articles as
select authors.name,articles.slug
from articles join authors
on articles.author=authors.id
order by authors.name;
```
Now disconenct from the server and run the Python file _'log_analysis_fizza_u.py'_ on your command line

```
python log_analysis_fizza_u.py
```


