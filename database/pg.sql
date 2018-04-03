create schema zsk;
/* 基本资料表 */
create table stocka(code text primary key,  name text,   company text,   plate text,  market text, industry text,
        area text,  capital text,  profile text,  business text,  founddate date,   ipodate date, updatedate date);
/* 日复权数据分区表 */
create table daydatafq(tdate date not null, code text not null, open float not null, high float not null,
        close float not null, low float not null,  volume bigint not null,  amount bigint not null,
        factor float not null, turnoverratio float) partition by range(tdate);
/* 日复权数据各分区 */
create table y2008_y2011 partition of daydatafq  for values from ('2008-01-01') to ('2011-12-31');
create table y2012_y2014 partition of daydatafq  for values from ('2012-01-01') to ('2014-12-31');
create table y2015_y2017 partition of daydatafq  for values from ('2015-01-01') to ('2017-12-31');
create table y2018_y2020 partition of daydatafq  for values from ('2018-01-01') to ('2020-12-31');
/* 股本结构表 */
create table SS(code text primary key,  changedate date,  changelog text, totalqt bigint,ltaqt bigint, limita bigint,
        ltbqt bigint, limitb bigint,lthqt bigint, updatedate date );
/* 板块分类资料表 */
create table catalog(node text primary key, name text,  catalog text, updatedate date );
/* 板块股票表 */
create table code2catalog(node text references catalog (node), code text references stocka (code), updatedate date,
        primary key (node,code) );
/* 深市成交明细表 */
create table sz_detail( tdatetime timestamp, code text,   price float,  volume int, amount int,  bs text)
        partition by range(tdatetime);

create table sz_ym201803 partition of sz_detail for values from ('2018-03-01') to ('2018-03-31');
create table sz_ym201804 partition of sz_detail for values from ('2018-04-01') to ('2018-04-30');

/* 沪市成交明细表 */
create table sh_detail(tdatetime timestamp,  code text,  price float, volume int, amount int,bs text)
        partition by range(tdatetime);

create table sh_ym201803 partition of sh_detail  for values from ('2018-03-01') to ('2018-03-31');
create table sh_ym201804 partition of sh_detail  for values from ('2018-04-01') to ('2018-04-30');