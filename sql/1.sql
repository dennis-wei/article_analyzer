drop table if exists articles;
create table article_meta (
  row SERIAL PRIMARY KEY,
  raw_url text,
  flask_url text
);

create table article_content (
  row SERIAL PRIMARY KEY,
  date_scraped date,
  content text
);

create table article_vectors (
  row SERIAL PRIMARY KEY,
  base_vector int[],
  recent_vector int[]
);

create table word_index_jsons (
  index_type text,
  date_fetched date,
  index json,
)
